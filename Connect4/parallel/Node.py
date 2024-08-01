import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from game.Connect4 import Connect4


@dataclass
class Node:
    game: Connect4
    node_id: str
    children: List['Node'] = field(default_factory=list)
    score: float = 0.0
    next_move: int = -1
    is_finished: bool = False

    def __init__(self, game: Connect4, node_id: str, children: Optional[List['Node']] = None,
                 score: float = 0.0, next_move: int = -1, is_finished:bool = False):
        self.game = game
        self.node_id = node_id
        self.children = children if children is not None else []
        self.score = score
        self.next_move = next_move
        self.is_finished = is_finished
