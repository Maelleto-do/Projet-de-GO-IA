import Territory
import Goban
import Shape
import json


class Opening:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves

    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])

    # Fuseki

    def evaluate_opening(self):

        # On cherche à atteindre les coins et les bords
        # et à placer des coups sur la deuxième ligne
        # Les coups doivent être répartis sur le plateau (au nord, à l'est etc)
        # afin d'agrandir au maximum le territoire

        res = 0
        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)

        # json_file = open('game.json.', 'r', encoding="utf-8")  

        # data_opening = json.load(json_file)
        # print(data_opening[0].moves)
        


        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self._black_goban != []:
                ufcoord_last = self.get_last_black()
                x_last = ufcoord_last[0]
                y_last = ufcoord_last[1]
                if (abs(y_last - y) > 4):
                    res = res + 1000
                if (shape._is_keima(x, y, ufcoord_last)) or (shape._is_tobi(x, y, ufcoord_last)) :
                    res = res + 5000
            if (1 <= x <= 7) and (1 <= y <= 7):  # se situe sur le deuxième ligne
                res = res + 3000
            if territory.in_N(x, y) or territory.in_NE(x, y) or territory.in_NO(x, y) or territory.in_SE(x, y):
                res = res + 4000
            if ((territory.north_east_territory()[0] == 1)
                and ((territory.south_territory()[0] == 1)
                    or (territory.east_territory()[0] == 1)
                    or (territory.west_territory()[0] == 1))):
                res = res + 2000

        # for move in self._white_moves:
        #     ufcoord = Goban.Board.name_to_coord(move)
        #     x = ufcoord[0]
        #     y = ufcoord[1]
        #     if self._white_goban != []:
        #         ufcoord_last = self.get_last_white()
        #         x_last = ufcoord_last[0]
        #         y_last = ufcoord_last[1]
        #         if (abs(y_last - y) > 4):
        #             res = res - 1000
        #         if (shape._is_keima(x, y, ufcoord_last)) or (shape._is_tobi(x, y, ufcoord_last)) :
        #             res = res - 1000
        #     # se situe sur la deuxième ligne
        #     if (1 <= x <= 7) and (1 <= y <= 7):
        #         res = res - 6000
        #     if territory.in_S(x, y) or territory.in_N(x, y):
        #         res = res - 2000
        #     # se situe près d'un coin
        #     # if (territory.in_NE(x, y) or territory.in_SE(x, y) or territory.in_NO(x, y) or territory.in_SO(x, y)):
        #     #     res = res - 1000
        #     # if ((territory.north_territory()[1] == 1)
        #     #     or (territory.south_territory()[1] == 1)
        #     #     or (territory.east_territory()[1] == 1)
        #     #         or (territory.west_territory()[1] == 1)):
        #     #     res = res - 2000

        return res
