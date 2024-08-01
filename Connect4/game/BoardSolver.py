from random import random

from game.Connect4 import Connect4
from parallel.Node import Node
from parallel.Task import Task


def evaluate(game: Connect4, is_maximizing_player: bool, last_column_idx: int, depth: int, max_player_mark: str,
             min_player_mark: str) -> float:
    if game.check_game_status(last_column_idx) == 'win':
        if is_maximizing_player:
            return 1
        else:
            return -1

    if game.check_game_status(last_column_idx) == 'draw':
        return 0

    if depth == 0:
        return 0

    is_maximizing_player = not is_maximizing_player
    player_mark = max_player_mark if is_maximizing_player else min_player_mark
    depth -= 1

    total = 0
    num_of_moves = 0

    is_all_lose = True
    is_all_win = True

    for column in game.get_available_moves():
        num_of_moves += 1

        game.make_move(column, player_mark)
        result = evaluate(game, is_maximizing_player, column, depth, max_player_mark, min_player_mark)
        game.undo_move(column)

        if result > -1:
            is_all_lose = False
        if result != 1:
            is_all_win = False

        if result == 1 and is_maximizing_player:
            return 1
        if result == -1 and not is_maximizing_player:
            return -1

        total += result

    if is_all_win:
        return 1
    if is_all_lose:
        return -1

    return total / num_of_moves


def solve_task(task: Task):
    node = task.node
    game = node.game
    depth = task.remaining_depth
    best_move_value = -1
    best_column_idx = -1

    while depth > 0 and best_move_value == -1:
        for column in game.get_available_moves():
            if best_column_idx == -1:
                best_column_idx = column

            game.make_move(column, task.max_player_sign if task.is_max_player_turn else task.min_player_sign)
            result = evaluate(game, not task.is_max_player_turn, column, depth,
                              task.max_player_sign,
                              task.min_player_sign)
            game.undo_move(column)

            if result > best_move_value or (result == best_move_value and random() % 2 == 0):
                best_move_value = result
                best_column_idx = column
        depth = depth // 2
    return best_move_value


def resolve_node_score(node: Node, is_max_player_turn) -> float:
    is_all_win = True
    is_all_loss = True
    total_score = 0.0

    for node_child in node.children:
        is_all_win = is_all_win and node_child.score == 1
        is_all_loss = is_all_loss and node_child.score == -1

        if node_child.score == 1 and is_max_player_turn:
            return 1.0
        if node_child.score == -1 and not is_max_player_turn:
            return -1.0

        total_score += node_child.score

    if is_all_win:
        return 1.0
    if is_all_loss:
        return -1.0

    return total_score / len(node.children)
