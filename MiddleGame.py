import Goban
import Territory
import Shape


class MiddleGame:

    def __init__(self, board, mycolor, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._mycolor = mycolor


    def evaluation(self):

        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)
        black = 0
        white = 0

        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            for move in self._white_moves:
                ufcoord = Goban.Board.name_to_coord(move)
                x_white = ufcoord[0]
                y_white = ufcoord[1]
                if territory.dist((x, y), (x_white, y_white)) <= 2:
                    if territory.in_SE(self, x, y) and (territory.south_east_territory(self)[2]):
                        if shape._is_tobi(self, x, y, (x_white, y_white)):
                            black = black + 1000

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            for move in self._black_moves:
                ufcoord = Goban.Board.name_to_coord(move)
                x_black = ufcoord[0]
                y_black = ufcoord[1]
                if territory.dist((x, y), (x_black, y_black)) <= 2:
                    if territory.in_S0(self, x, y) and (not territory.south_west_territory(self)[2]):
                        if shape._is_tobi(self, x, y, (x_black, y_black)):
                            white = white + 1000


        if self._mycolor == Goban.Board._BLACK:
            res = black - white
        else:
            res = white - black

        return res
