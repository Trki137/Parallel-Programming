from abc import ABC, abstractmethod

from game.Connect4 import Connect4


class Player(ABC):
    def __init__(self, player_mark):
        self.player_mark = player_mark

    @abstractmethod
    def make_move(self, game: Connect4) -> str:
        pass