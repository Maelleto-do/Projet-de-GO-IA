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

    def get_last(self, color):
        if self._board._historyMoveNames != []:
            if color == "BLACK":
                return self._board._historyMoveNames[self._count * 2]
            else:
                return self._board._historyMoveNames[(self._count * 2) - 1]

    def liberties(self, coord):
        lib = 0
        liberties = []
        x = coord[0]
        y = coord[1]

        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        for n in neighbors:
            if (self._board[Goban.Board.flatten((n[0], n[1]))] == 0) or not self._board._isOnBoard(n[0], n[1]):
                lib = lib + 1
            else:
                liberties.append(n)
        return lib, liberties

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
            res = res + self.liberties(Goban.Board.name_to_coord(move))[0]
        return res

    def liberties_black(self):
        res = 0
        for move in self._black_moves:
            res = res + self.liberties(Goban.Board.name_to_coord(move))[0]
        return res

    def evaluation(self):

        # print("BLACK MOOOOOOOOOOOOOVES ", self._black_moves)



        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)
        black = 0
        white = 0

        # Heuristique pour Noir
        if (self._black_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last("BLACK"))
            # if territory.distance(last_white, last_black) <= 2:
            #     for move in self._black_moves:
            #         ufcoord = Goban.Board.name_to_coord(move)
            #         x_black = ufcoord[0]
            #         y_black = ufcoord[1]
            #         if shape._is_tobi(x_black, y_black, last_black) or shape._is_nobi(x_black, y_black, last_black):
            #             black = black + 3000
            # for move in self._board.legal_moves():
            #     print("LIVIIIIIIIIIIIIIIIIIIING")
            #     if shape._living_group_black(move): black += 6000

            for move in self._white_moves:
                if shape._is_atari_white(Goban.Board.name_to_coord(move)):
                    black += 100000

            # Un coup joué par Noir se retrouve en atari
            for move in self._black_goban:  
                black_coord = Goban.Board.unflatten(move)   
                if shape._is_atari_black(black_coord):
                    # print("Le coup ", self._board.flat_to_name(move))
                    for move in self._black_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_black = ufcoord[0]
                        y_black = ufcoord[1]
                        if ufcoord in self.liberties(black_coord)[1] and self.liberties(black_coord)[0] >= 2 : # On fait un Nobi pour augmenter les libertés
                            print("ATARIIIIIIIIIIIIIIIIII")
                            black = black + 300000

        # Heuristique pour Blanc
        if (self._white_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last("BLACK"))
            for move in self._black_moves:
                if shape._is_atari_black(Goban.Board.name_to_coord(move)):
                    white += 100000

            # Un coup joué par Blanc se retrouve en atari
            for move in self._white_goban:  
                white_coord = Goban.Board.unflatten(move)   
                if shape._is_atari_white(white_coord):
                    # print("Le coup ", self._board.flat_to_name(move))
                    for move in self._white_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_white = ufcoord[0]
                        y_white = ufcoord[1]
                        if ufcoord in self.liberties(white_coord)[1] and self.liberties(white_coord)[0] >= 2: # On fait un Nobi pour augmenter les libertés
                            print("ATARIIIIIIIIIIIIIIIIII")
                            white = white + 300000

        black = black + self.liberties_black() + self._board._capturedWHITE + \
            600000*(shape._diamond("BLACK"))

        # Objectif : minimiser les libertés de l'adversaire
        white = white + self.liberties_white() + self._board._capturedBLACK + \
            600000*(shape._diamond("WHITE"))

        if self._mycolor == Goban.Board._BLACK:
            res = black - white
        else:
            res = white - black

        return res
