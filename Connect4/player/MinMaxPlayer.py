import copy
import csv
import os
import time
import uuid
import pickle

import mpi4py
import queue
from random import random
from abc import ABC

from parallel.Node import Node
from parallel.Task import Task
from player.Player import Player
from game.BoardSolver import evaluate, solve_task, resolve_node_score
from game.Connect4 import Connect4


def add_child_to_parent(calc_node: Node, parent_nodes: list[Node]):
    for node in parent_nodes:
        if node.node_id == calc_node.node_id:
            node.score = calc_node.score


class MinMaxPlayer(Player, ABC):
    def __init__(self, player_mark, other_mark, comm: mpi4py.MPI.COMM_WORLD, depth: int = 6, task_depth: int = 2):
        super().__init__(player_mark)
        self.depth = depth
        self.task_depth = task_depth
        self.comm: mpi4py.MPI.COMM_WORLD = comm
        self.comm_size = comm.Get_size()
        self.other_mark = other_mark
        self.wrote_in_file = False

    def make_node(self, copy_of_game: Connect4, is_max_player_turn: bool, column_move: int) -> Node:
        copy_of_game.make_move(column=column_move, mark=self.player_mark if is_max_player_turn else self.other_mark)
        current_game_status = copy_of_game.check_game_status(column=column_move)
        new_node = Node(game=copy_of_game, node_id=str(uuid.uuid4()), children=[], next_move=column_move,
                        is_finished=current_game_status != 'not finished', score=0.0)

        if current_game_status == 'not finished' or current_game_status == 'draw':
            return new_node

        new_node.score = 1.0 if is_max_player_turn else -1.0
        return new_node

    def make_move(self, game: Connect4) -> str:
        if self.comm_size < 2:
            column = self.sequential(game)
        else:
            column = self.parallel(game)

        print(f"MinMax player makes move: {column}")
        game.make_move(column, self.player_mark)
        return game.check_game_status(column)

    def parallel(self, game: Connect4) -> int:
        root_node = Node(game=game, node_id=str(uuid.uuid4()), children=[])
        tree = {0: [root_node]}
        node_tree_search = {}
        job_queue = queue.Queue()
        workers_destinations = queue.Queue()

        for i in range(1, self.comm_size):
            workers_destinations.put(i)

        is_max_player_turn = False
        start_time = time.time()
        for search_depth in range(1, self.task_depth + 1):
            is_max_player_turn = not is_max_player_turn
            if search_depth not in tree:
                tree[search_depth] = []

            all_parent_nodes = tree[search_depth - 1]
            for parent in all_parent_nodes:
                if parent.is_finished:
                    continue

                for column_move in parent.game.get_available_moves():
                    copy_of_game = copy.deepcopy(parent.game)
                    new_node: Node = self.make_node(copy_of_game, is_max_player_turn, column_move)
                    tree[search_depth].append(new_node)
                    parent.children.append(new_node)

                    if search_depth == self.task_depth and not new_node.is_finished:
                        node_tree_search[new_node.node_id] = new_node
                        task = Task(node=new_node, is_max_player_turn=not is_max_player_turn,
                                    max_player_sign=self.player_mark, min_player_sign=self.other_mark,
                                    remaining_depth=self.depth - self.task_depth)
                        job_queue.put(task)

        num_of_workers_not_done = 0
        while not job_queue.empty():
            if not workers_destinations.empty():
                self.send_job(job=job_queue.get(), dest=workers_destinations.get(), tag=1)
                num_of_workers_not_done += 1
            else:
                task_result, worker = self.check_and_receive(tag=1)
                if task_result is None:
                    task = job_queue.get()
                    best_value = solve_task(task=task)
                    node_tree_search[task.node.node_id].score = best_value
                else:
                    node_tree_search[task_result.node_id].score = task_result.score
                    self.send_job(job=job_queue.get(), dest=worker, tag=1)

        for i in range(num_of_workers_not_done):
            task_result = self.comm.recv(source=mpi4py.MPI.ANY_SOURCE, tag=1)
            task_result = pickle.loads(task_result)
            node_tree_search[task_result.node_id].score = task_result.score

        if self.task_depth != 1:
            for i in range(self.task_depth - 1, 0, -1):
                depth_nodes = tree[i]
                for node in depth_nodes:
                    node.score = resolve_node_score(node=node, is_max_player_turn=i % 2 == 0)

        best_column = 0
        best_score = float('-inf')
        for child in root_node.children:
            if child.score > best_score:
                best_column = child.next_move
                best_score = child.score

        end_time = time.time()
        if not self.wrote_in_file:
            self.wrote_in_file = True
            self.write_in_file(end_time - start_time)
        return best_column

    def sequential(self, game: Connect4):
        depth = self.depth
        best_move_value = -1
        best_column_idx = -1
        start_time = time.time()
        while depth > 0 and best_move_value == -1:
            for column in game.get_available_moves():
                if best_column_idx == -1:
                    best_column_idx = column

                game.make_move(column, self.player_mark)
                result = evaluate(game, True, column, depth, self.player_mark, self.other_mark)
                game.undo_move(column)

                if result > best_move_value or (result == best_move_value and random() % 2 == 0):
                    best_move_value = result
                    best_column_idx = column

            depth = depth / 2

        end_time = time.time()
        if not self.wrote_in_file:
            self.wrote_in_file = True
            self.write_in_file(end_time - start_time)
        return best_column_idx

    def write_in_file(self, seconds):
        file_exists = os.path.isfile('results.csv')
        column_headers = ['P', 'Depth', 'Task Depth', 'Execution Time (seconds)']
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(column_headers)

            writer.writerow([self.comm_size, self.depth, self.task_depth, seconds])
        pass

    def send_job(self, job: Task, dest: int, tag: int):
        self.comm.send(pickle.dumps(job), dest=dest, tag=tag)

    def check_and_receive(self, tag: int):
        status = mpi4py.MPI.Status()
        msg_exists = self.comm.Iprobe(source=mpi4py.MPI.ANY_SOURCE, tag=tag, status=status)
        if not msg_exists:
            return None, None

        worker = status.source
        task_result = self.comm.recv(source=status.source, tag=status.tag)
        return pickle.loads(task_result), worker
