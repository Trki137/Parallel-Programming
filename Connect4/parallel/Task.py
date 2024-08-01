from dataclasses import dataclass

from parallel.Node import Node


@dataclass
class Task:
    node: Node
    is_max_player_turn: bool
    max_player_sign: str
    min_player_sign: str
    remaining_depth: int

    def __init__(self, node: Node, is_max_player_turn: bool, max_player_sign: str, min_player_sign: str, remaining_depth: int):
        self.node = node
        self.is_max_player_turn = is_max_player_turn
        self.max_player_sign = max_player_sign
        self.min_player_sign = min_player_sign
        self.remaining_depth = remaining_depth
