import numpy as np


class Connect4:
    def __init__(self, rows, columns):
        self.board = np.zeros((rows, columns), dtype=str)

    def get_available_moves(self) -> np.ndarray:
        available_moves = []

        for i in range(self.board.shape[1]):
            if self.board[self.board.shape[0] - 1][i] == '':
                available_moves.append(i)

        return np.array(available_moves)

    def undo_move(self, column):
        for row in range(self.board.shape[0] - 1, -1, -1):
            if self.board[row][column] != '':
                self.board[row][column] = ''
                break

    def print_board(self) -> None:
        columns = self.board.shape[1]

        column_headers = ' '.join([str(i).center(3) + '  ' for i in range(columns)])
        print("   " + column_headers)

        for i in range(self.board.shape[0] - 1, -1, -1):
            row = self.board[i]
            print(" | " + ' | '.join(str(x).center(3) for x in row) + " |")

    def make_move(self, column: int, mark: str) -> bool:
        if column < 0 or column >= self.board.shape[1]:
            print("Neispravan stupac")
            return False

        if self.board[self.board.shape[0] - 1][column] != '':
            print("Stupac je vec pun")
            return False

        for row in range(0, self.board.shape[0]):
            if self.board[row][column] == '':
                self.board[row][column] = mark
                return True

        return False

    def check_game_status(self, column) -> str:
        if self.has_winner(column):
            return 'win'

        if np.all(self.board != ''):
            return 'draw'

        return 'not finished'

    def has_winner(self, column: int) -> bool:
        last_move_row = self.find_last_move_row(column)
        player_mark = self.board[last_move_row][column]

        # Vertical check
        if last_move_row - 3 >= 0:
            if self.board[last_move_row - 1][column] == self.board[last_move_row - 2][column] == \
                    self.board[last_move_row - 3][column] == player_mark:
                return True

        # Horizontal check
        horizontal_count = 1
        for d in [-1, 1]:
            i = 1
            while 0 <= column + d * i < self.board.shape[1] and self.board[last_move_row][
                column + d * i] == player_mark:
                horizontal_count += 1
                i += 1
                if horizontal_count >= 4:
                    return True

        # Main diagonal (/)
        count = 1
        for i in range(1, 4):
            if 0 <= last_move_row + i < self.board.shape[0] and 0 <= column + i < self.board.shape[1] and \
                    self.board[last_move_row + i][column + i] == player_mark:
                count += 1
            else:
                break

        for i in range(1, 4):
            if 0 <= last_move_row - i < self.board.shape[0] and 0 <= column - i < self.board.shape[1] and \
                    self.board[last_move_row - i][column - i] == player_mark:
                count += 1
            else:
                break

        if count >= 4:
            return True

        # Secondary diagonal (\)
        count = 1
        for i in range(1, 4):
            if 0 <= last_move_row + i < self.board.shape[0] and 0 <= column - i < self.board.shape[1] and \
                    self.board[last_move_row + i][column - i] == player_mark:
                count += 1
            else:
                break

        for i in range(1, 4):
            if 0 <= last_move_row - i < self.board.shape[0] and 0 <= column + i < self.board.shape[1] and \
                    self.board[last_move_row - i][column + i] == player_mark:
                count += 1
            else:
                break

        return count >= 4

    def find_last_move_row(self, column: int) -> int | None:
        for row in range(self.board.shape[0] - 1, -1, -1):
            if self.board[row][column] != '':
                return row
        return None
