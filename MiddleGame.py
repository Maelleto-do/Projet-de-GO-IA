import Goban
import Territory
import Shape


class MiddleGame:

    def __init__(self, board, mycolor, count, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._mycolor = mycolor
        self._count = count

    # def get_last_enemy(self, color):
    #     if self._board._historyMoveNames != []:
    #         if self._board._nextPlayer == self._board._WHITE:
    #             if color == "BLACK":
    #                 return Goban.Board.coord_to_name(Goban.Board.unflatten(self._black_goban[-1]))
    #             else:
    #                 return self._board._historyMoveNames[(self._count * 2) - 1]
    #         else:
    #             if color == "BLACK":
    #                 return self._board._historyMoveNames[self._count * 2]
    #             else:
    #                 return Goban.Board.coord_to_name(Goban.Board.unflatten(self._white_goban[-1]))

    def get_last_enemy(self, color):
        if self._board._historyMoveNames != []:
            if color == "BLACK":
                return self._board._historyMoveNames[self._count * 2]
            else:
                return self._board._historyMoveNames[(self._count * 2) - 1]


    def liberties(self, coord):
        lib = 0
        x = coord[0]
        y = coord[1]

        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        for n in neighbors:
            if self._board[Goban.Board.flatten((n[0], n[1]))] == 0:
                lib = lib + 1
        return lib

    def nb_black(self):
        res = 0
        for n in self._black_moves:
            res = res + 1
        return res

    def nb_white(self):
        res = 0
        for n in self._white_moves:
            res = res + 1
        return res

    def liberties_white(self):
        res = 0
        for move in self._white_moves:
            res = res + self.liberties(Goban.Board.name_to_coord(move))
        return res

    def liberties_black(self):
        res = 0
        for move in self._black_moves:
            res = res + self.liberties(Goban.Board.name_to_coord(move))
        return res

    def evaluation(self):

        self.get_last_enemy("BLACK")
        self.get_last_enemy("WHITE")

        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)
        black = 0
        white = 0

        if (self._black_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last_enemy("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last_enemy("BLACK"))
            if territory.distance(last_white, last_black) <= 2:
                for move in self._black_moves:
                    ufcoord = Goban.Board.name_to_coord(move)
                    x_black = ufcoord[0]
                    y_black = ufcoord[1]
                    if shape._is_tobi(x_black, y_black, last_black) or shape._is_nobi(x_black, y_black, last_black):
                        black = black + 3000

        if (self._white_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last_enemy("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last_enemy("BLACK"))
            if territory.distance(last_white, last_black) <= 2:
                for move in self._white_moves:
                    ufcoord = Goban.Board.name_to_coord(move)
                    x_white = ufcoord[0]
                    y_white = ufcoord[1]
                    if shape._is_tobi(x_white, y_white, last_white) or shape._is_nobi(x_white, y_white, last_white):
                        white = white + 3000

        # Objectif : minimiser les libertés de l'adversaire
        white = white + self.liberties_white() + self.nb_white()
        black = black + self.liberties_black() + self.nb_black()

        if self._mycolor == Goban.Board._BLACK:
            res = black - white
        else:
            res = white - black

        return res
