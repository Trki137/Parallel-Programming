from abc import ABC


from game.Connect4 import Connect4
from player.Player import Player


class HumanPlayer(Player, ABC):
    def __init__(self, player_mark):
        super().__init__(player_mark)

    def make_move(self, game: Connect4):
        while True:
            try:
                column = int(input("Unesite sljedeci stupac: "))
            except:
                print("Neispravan unos")
                game.print_board()
                continue

            is_valid = game.make_move(column, self.player_mark)
            if is_valid:
                break

        return game.check_game_status(column)
