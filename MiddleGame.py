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
                ufcoord_white = Goban.Board.name_to_coord(move)
                x_white = ufcoord_white[0]
                y_white = ufcoord_white[1]
                dist = territory.distance(ufcoord, ufcoord_white)
                if dist <= 2:
                    if territory.in_SE(x, y) and (territory.south_east_territory()[2]):
                        if shape._is_tobi(x, y, (x_white, y_white)):
                            black = black + 1000

        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            # print("last black goban ", [Goban.Board.coord_to_name(self._board.unflatten(c)) for c in self._black_goban] )
            # print("last white goban ", [Goban.Board.coord_to_name(self._board.unflatten(c)) for c in self._white_goban] )
            if (self._white_goban != []):
                last_white = self._board.unflatten(self._white_goban[-1])
                if territory.distance(last_white, (x, y)) <= 2:
                    print("Distance entre ", Goban.Board.coord_to_name(last_white), " et ", Goban.Board.coord_to_name(
                        (x, y)), " : ", territory.distance(last_white, (x, y)))
                    for move in self._white_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_white = ufcoord[0]
                        y_white = ufcoord[1]
                        # print(" last white : ",  Goban.Board.coord_to_name(last_white))
                        # print(" last black : ",  Goban.Board.coord_to_name(last_black))
                        if territory.in_SE(last_white[0], last_white[1]) and territory.in_S(x_white, y_white):
                            if shape._is_tobi(x_white, y_white, last_white):
                                white = white + 6000

            # for move in self._black_moves:
            #     ufcoord = Goban.Board.name_to_coord(move)
            #     x_black = ufcoord[0]
            #     y_black = ufcoord[1]
            #     if territory.distance((x, y), (x_black, y_black)) <= 2:
            #         print("Distance entre ", Goban.Board.coord_to_name((x, y)), " et ", Goban.Board.coord_to_name(
            #             (x_black, y_black)), " : ", territory.distance((x, y), (x_black, y_black)))
            #         if territory.in_SO(x, y) and (not territory.south_west_territory()[2]):
            #             if (self._white_goban != []):
            #                 last_white = self._board.unflatten(
            #                     self._white_goban[-1])
            #                 # ufcoord_last_white = Goban.Board.name_to_coord(last_white)
            #                 if shape._is_tobi(x, y, last_white):
            #                     # print("MY PIECE ", Goban.Board.coord_to_name((x, y)))
            #                     # print("LAST WHITE ", Goban.Board.coord_to_name(last_white))

            #                     white = white + 2000

        if self._mycolor == Goban.Board._BLACK:
            res = black - white
        else:
            res = white - black

        return res
