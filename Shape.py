import Goban


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Cette classe permet de gérer les formes dessinées par les pierres sur le plateau
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Shape:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves


    """
    Définit la forme d'un groupe vivant (groupe avec deux yeux ne pouvant être capturé)
    """
    def living_group(self, move, color):
        count = 0
        coord = Goban.Board.name_to_coord(move)  # pierre au milieu
        x = coord[0]
        y = coord[1]
        if color == "BLACK":
            for i in range(-2, 3):
                if (not self._board._isOnBoard(x+1, y+i)):
                    count += 1
                elif (self._board[Goban.Board.flatten((x+1, y+i))] == 1):
                    count += 1
                if not self._board._isOnBoard(x-1, y+i):
                    count += 1
                elif (self._board[Goban.Board.flatten((x-1, y+i))] == 1):
                    count += 1
            for i in range(-2, 3, 2):
                if self._board._isOnBoard(x, y+i):
                    if self._board[Goban.Board.flatten((x, y+i))] == 1:
                        count += 1
            if self._board._isOnBoard(x, y+1) and self._board._isOnBoard(x, y-1):
                if (self._board[Goban.Board.flatten((x, y+1))] == 0
                        and self._board[Goban.Board.flatten((x, y-1))] == 0):
                    count += 1
            if count == 15:
                return True

        else:
            for i in range(-2, 3):
                if (not self._board._isOnBoard(x+1, y+i)):
                    count += 1
                elif (self._board[Goban.Board.flatten((x+1, y+i))] == 2):
                    count += 1
                if not self._board._isOnBoard(x-1, y+i):
                    count += 1
                elif (self._board[Goban.Board.flatten((x-1, y+i))] == 2):
                    count += 1
            for i in range(-2, 3, 2):
                if self._board._isOnBoard(x, y+i):
                    if self._board[Goban.Board.flatten((x, y+i))] == 2:
                        count += 1
            if self._board._isOnBoard(x, y+1) and self._board._isOnBoard(x, y-1):
                if (self._board[Goban.Board.flatten((x, y+1))] == 0
                        and self._board[Goban.Board.flatten((x, y-1))] == 0):
                    count += 1
            if count == 15:
                return True
        return False

    """
    Créer un groupe vivant (avec deux yeux) dans un coin 
    """
    def create_living_territory_corner(self, move, color):
        count = 0
        if self.in_NE(move[0], move[1]):
            if (move == (8, 8)):
                if (self._board.__getitem__(Goban.Board.flatten((7, 8))) == 0) and (self._board.__getitem__(Goban.Board.flatten((8, 7))) == 0):
                    if color == "BLACK":
                        if ((self._board.__getitem__(Goban.Board.flatten((6, 8))) == 1) and (self._board.__getitem__(Goban.Board.flatten((7, 7))) == 1)
                                and (self._board.__getitem__(Goban.Board.flatten((8, 6))) == 1)):
                            count += 1
                    else:
                        if ((self._board.__getitem__(Goban.Board.flatten((6, 8))) == 2) and (self._board.__getitem__(Goban.Board.flatten((7, 7))) == 2)
                                and (self._board.__getitem__(Goban.Board.flatten((8, 6))) == 2)):
                            count += 1
        elif self.in_SO(move[0], move[1]):
            if (move == (0, 0)):
                if (self._board.__getitem__(Goban.Board.flatten((1, 0))) == 0) and (self._board.__getitem__(Goban.Board.flatten((0, 1))) == 0):
                    if color == "BLACK":
                        if ((self._board.__getitem__(Goban.Board.flatten((2, 0))) == 1) and (self._board.__getitem__(Goban.Board.flatten((1, 1))) == 1)
                                and (self._board.__getitem__(Goban.Board.flatten((0, 2))) == 1)):
                            count += 1
                    else:
                        if ((self._board.__getitem__(Goban.Board.flatten((2, 0))) == 2) and (self._board.__getitem__(Goban.Board.flatten((1, 1))) == 2)
                                and (self._board.__getitem__(Goban.Board.flatten((0, 2))) == 2)):
                            count += 1
        return count


    """
    Les formes compactes en carré sont à proscrire.
    Renvoie vraie si la forme est un carré plein, faux sinon.
    """
    def _bad_shape(self, color):
        if color == "BLACK":
            for move in self._black_moves:
                coord = self._board.name_to_coord(move)
                x = coord[0]
                y = coord[1]
                if (self._board._isOnBoard(x, y) and self._board._isOnBoard(x, y-1)
                        and self._board._isOnBoard(x+1, y) and self._board._isOnBoard(x+1, y-1)):
                    if (
                            self._board[Goban.Board.flatten((x, y))] == 1
                            and self._board[Goban.Board.flatten((x+1, y))] == 1
                            and self._board[Goban.Board.flatten((x+1, y-1))] == 1
                            and self._board[Goban.Board.flatten((x, y-1))] == 1
                    ):
                        return True
        else:
            for move in self._white_moves:
                coord = self._board.name_to_coord(move)
                x = coord[0]
                y = coord[1]
                if (self._board._isOnBoard(x, y) and self._board._isOnBoard(x, y-1)
                        and self._board._isOnBoard(x+1, y) and self._board._isOnBoard(x+1, y-1)):
                    if (
                            self._board[Goban.Board.flatten((x, y))] == 2
                            and self._board[Goban.Board.flatten((x+1, y))] == 2
                            and self._board[Goban.Board.flatten((x+1, y-1))] == 2
                            and self._board[Goban.Board.flatten((x, y-1))] == 2
                    ):
                        return True
        return False


    """
    Mise en Atari d'une pierre Blanche
    """
    def _is_atari_white(self, white_coord):

        x = white_coord[0]
        y = white_coord[1]
        res = 0

        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]

        for n in neighbors:
            if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                res = res + 1

        return res >= 3

    """
    Mise en Atari d'une pierre Noire
    """
    def _is_atari_black(self, black_coord):

        x = black_coord[0]
        y = black_coord[1]
        res = 0

        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]

        for n in neighbors:
            if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                res = res + 1

        return res >= 3

    
    """
    Définit la forme du diamant
    """
    def _diamond(self, move, color):
        res = False

        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]

        south = ((x, y+2), (x+1, y+1), (x-1, y+1))
        neighbors_1 = [
            c for c in south if self._board._isOnBoard(c[0], c[1])]

        north = ((x, y-2), (x+1, y-1), (x-1, y-1))
        neighbors_2 = [
            c for c in north if self._board._isOnBoard(c[0], c[1])]

        east = ((x-2, y), (x-1, y+1), (x-1, y-1))
        neighbors_3 = [
            c for c in east if self._board._isOnBoard(c[0], c[1])]

        west = ((x+2, y), (x+1, y+1), (x+1, y-1))
        neighbors_4 = [
            c for c in west if self._board._isOnBoard(c[0], c[1])]

        if color == "BLACK":
            # move ferme le diamant au sud
            count_n = 0
            for n in neighbors_1:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    count_n += 1
            if count_n == 3:
                return True
                # move ferme le diamant au nord
            count_s = 0
            for n in neighbors_2:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    count_s += 1
            if count_s == 3:
                return True
                # move ferme le diamant à l'est
            count_e = 0
            for n in neighbors_3:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    count_e += 1
            if count_e == 3:
                return True
                # move ferme le diamant à l'ouest
            count_w = 0
            for n in neighbors_4:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    count_w += 1
            if count_w == 3:
                return True
        else:
            # move ferme le diamant au sud
            count_n = 0
            for n in neighbors_1:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                    count_n += 1
            if count_n == 3:
                return True
                # move ferme le diamant au nord
            count_s = 0
            for n in neighbors_2:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                    count_s += 1
            if count_s == 3:
                return True
                # move ferme le diamant à l'est
            count_e = 0
            for n in neighbors_3:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                    count_e += 1
            if count_e == 3:
                return True
                # move ferme le diamant à l'ouest
            count_w = 0
            for n in neighbors_4:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                    count_w += 1
            if count_w == 3:
                return True

        return res

    """
    Coup Nobi (pierres côte à côte)
    """
    def _is_nobi(self, move, last_move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        res = False
        if(((x == last_move[0] + 1) or (x == last_move[0] - 1)) and (y == last_move[1])):
            res = True
        elif (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0])):
            res = True
        return res

  
    """
    Coup Tobi (saut en ligne droite)
    Sert à s'étendre et fermer territoire
    """  
    def _is_tobi(self, move, last_move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        res = False
        if (((x == last_move[0] + 2) or (x == last_move[0] - 2)) and (y == last_move[1])):
            res = True
        elif ((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0]):
            res = True
        return res

    """
    Coup Kosumi (petit pas en diagonle)
    Sert à attaquer
    """ 
    def _is_kosumi(self, move, last_move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        res = False
        if (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0] + 1)):
            res = True
        elif (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0] - 1)):
            res = True
        return res

    """
    Coup Keima (saut en diagonale)
    Sert à attaquer ou agrandir territoire
    """ 
    def _is_keima(self, move, last_move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        res = False
        if (((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0] + 1)):
            res = True
        elif (((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0] - 1)):
            res = True
        return res
