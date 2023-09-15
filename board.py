import random
import itertools
import numpy as np

BOARD_SIZE = 3
BOARD_DIMENSIONS = (BOARD_SIZE, BOARD_SIZE)

CELL_X = 1
CELL_O = -1
CELL_EMPTY = 0

RESULT_X_WINS = 1
RESULT_O_WINS = -1
RESULT_DRAW = 0
RESULT_NOT_OVER = 2

new_board = np.array([CELL_EMPTY] * BOARD_SIZE ** 2)


def play_game(x_strategy, o_strategy):
    board = Board()
    player_strategies = itertools.cycle([x_strategy, o_strategy])

    while not board.is_game_over():
        play = next(player_strategies)
        board = play(board)
        print(board.get_board_as_string())

    return board


def play_games(total_games, x_strategy, o_strategy, play_single_game=play_game):
    results = {
        RESULT_X_WINS: 0,
        RESULT_O_WINS: 0,
        RESULT_DRAW: 0
    }

    for game_no in range(total_games):
        end_of_game = (play_single_game(x_strategy, o_strategy))
        result = end_of_game.get_game_result()
        results[result] += 1

    x_wins_percent = results[RESULT_X_WINS] / total_games * 100
    o_wins_percent = results[RESULT_O_WINS] / total_games * 100
    draw_percent = results[RESULT_DRAW] / total_games * 100

    print(f"x wins: {x_wins_percent:.2f}%")
    print(f"o wins: {o_wins_percent:.2f}%")
    print(f"draw  : {draw_percent:.2f}%")


def play_random_move(board):
    move = board.get_random_valid_move_index()
    return board.play_move(move)


def is_even(value):
    return value % 2 == 0


def get_symbol(cell):
    if cell == CELL_X:
        return 'X'
    if cell == CELL_O:
        return 'O'
    return '-'


def get_sum_of_rows_cols_diagonals(board):
    sums = np.concatenate([np.sum(board, axis=0),  # Column sums
                           np.sum(board, axis=1),  # Row sums
                           [np.trace(board),        # Main diagonal sum
                            np.trace(np.fliplr(board))]])  # Other diagonal sum

    return sums


class Board:
    def __init__(self, board=None, illegal_move=None):
        self.board = board
        if board is None:
            self.board = np.copy(new_board)

        self.illegal_move = illegal_move

        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)

    def get_game_result(self):
        if self.illegal_move is not None:
            return RESULT_O_WINS if self.get_turn() == CELL_X else RESULT_X_WINS

        sum_of_rows_cols_diagonals = get_sum_of_rows_cols_diagonals(self.board_2d)


        if BOARD_SIZE in sum_of_rows_cols_diagonals:
            return RESULT_X_WINS

        if -BOARD_SIZE in sum_of_rows_cols_diagonals:
            return RESULT_O_WINS

        if CELL_EMPTY not in self.board_2d:
            return RESULT_DRAW

        return RESULT_NOT_OVER

    def is_game_over(self):
        return self.get_game_result() != RESULT_NOT_OVER

    def is_in_illegal_state(self):
        return self.illegal_move is not None

    def play_move(self, move_index):
        print(f"Move position: {move_index + 1}")
        board_copy = np.copy(self.board)

        if move_index not in self.get_valid_move_indexes():
            return Board(board_copy, illegal_move=move_index)

        board_copy[move_index] = self.get_turn()
        return Board(board_copy)

    def get_turn(self):
        non_zero = np.count_nonzero(self.board)
        return CELL_X if is_even(non_zero) else CELL_O

    def get_valid_move_indexes(self):
        return ([i for i in range(self.board.size)
                 if self.board[i] == CELL_EMPTY])

    def get_illegal_move_indexes(self):
        return ([i for i in range(self.board.size)
                 if self.board[i] != CELL_EMPTY])

    def get_random_valid_move_index(self):
        return random.choice(self.get_valid_move_indexes())

    def print_board(self):
        print(self.get_board_as_string())

    def get_board_as_string(self):
        rows, cols = self.board_2d.shape
        board_as_string = "-------\n"
        for r in range(rows):
            board_as_string += "|"
            for c in range(cols):
                move = get_symbol(self.board_2d[r, c])
                board_as_string += f"{move}|"
            board_as_string += "\n"
        board_as_string += "-------\n"

        return board_as_string
