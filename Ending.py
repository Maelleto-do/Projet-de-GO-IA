import Territory
import Goban
import Shape


class Ending:

    def __init__(self, board, mycolor, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._mycolor = mycolor

    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])

    

    def evaluate_ending(self):

  