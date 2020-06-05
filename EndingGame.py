import Territory
import Goban
import Shape


class EndingGame:
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

    def liberties(self, coord):
        lib = 0
        liberties = []
        x = coord[0]
        y = coord[1]

        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        for n in neighbors:
            if (self._board[Goban.Board.flatten((n[0], n[1]))] == 0) and self._board._isOnBoard(n[0], n[1]):
                lib = lib + 1
            else:
                liberties.append(n)
        return lib, liberties

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
    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])

    

    def evaluate_ending(self):

        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)
        black = 0
        white = 0


        """""""""""""""""""""""""""""
        Heuristique pour Noir
        """""""""""""""""""""""""""""

        if (self._black_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last("BLACK"))

            for move in self._white_moves:
                if shape._is_atari_white(Goban.Board.name_to_coord(move)):
                    black += 900

            for move in self._black_moves:
                for white_move in self._white_goban:
                    # Si elle n'a plus qu'une seule liberté, il faut la capturer pour capturer des pièces
                    if ((self.liberties(Goban.Board.name_to_coord(white_move))[0] == 1)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        black += 900

    
                    # Un coup joué par Noir se retrouve en atari
            for move in self._black_goban:
                black_coord = Goban.Board.unflatten(move)
                if shape._is_atari_black(black_coord):
                    # print("Le coup ", self._board.flat_to_name(move))
                    for move in self._black_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_black = ufcoord[0]
                        y_black = ufcoord[1]
                        # On fait un Nobi pour augmenter les libertés, tout en faisant attention à ne pas 
                        # se remettre Atari
                        if ufcoord in self.liberties(black_coord)[1] and self.liberties(black_coord)[0] >= 2:
                            black = black + 2000


        """""""""""""""""""""""""""""
        Heuristique pour Blanc
        """""""""""""""""""""""""""""

        if (self._white_goban != []):
            last_white = Goban.Board.name_to_coord(
                self.get_last("WHITE"))
            last_black = Goban.Board.name_to_coord(
                self.get_last("BLACK"))


            for move in self._black_moves:
                if shape._is_atari_black(Goban.Board.name_to_coord(move)):
                    white += 900

            for move in self._white_moves:
                # Une pièce noire a trop de libertés, il faut l'encercler
                for black_move in self._black_goban:
                    if ((self.liberties(Goban.Board.name_to_coord(black_move))[0] >= 2)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        white += 900

            # Un coup joué par Blanc se retrouve en atari
            for move in self._white_goban:
                white_coord = Goban.Board.unflatten(move)
                if shape._is_atari_white(white_coord):
                    # print("Le coup ", self._board.flat_to_name(move))
                    for move in self._white_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_white = ufcoord[0]
                        y_white = ufcoord[1]
                        # On fait un Nobi pour augmenter les libertés
                        if ufcoord in self.liberties(white_coord)[1] and self.liberties(white_coord)[0] >= 2:
                            white = white + 2000


        black = black + 2000*self.liberties_black()
        white = white + 2000*self.liberties_white()

        if self._mycolor == Goban.Board._BLACK:
            res = black
        else:
            res = white

        return res


  