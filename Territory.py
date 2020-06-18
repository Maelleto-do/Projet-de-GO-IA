# -*- coding: utf-8 -*-


import Goban
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Cette classe permet de gérer les territoires et la répartition des pierres sur le Goban.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Territory:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves

    """
    Distance entre deux pierres
    """
    def distance(self, A, B):
        dist = np.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        return dist


    """
    Renvoie vrai si la pierre se trouve sur les bords, faux sinon
    """
    def _in_border(self, move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        res = False
        if (0 <= x <= 7) and ((y == 0) or (y == 7)):
            res = True
        elif (0 <= y <= 7) and ((y == 0) or (y == 7)):
            res = True
        return res

    """
    Renvoie le nombre d'intersections contrôlées par Noir
    """
    def _count_controled_intersection_black(self):
        controled_intersection = 0
        for move in self._black_moves:
            coord = Goban.Board.name_to_coord(move)
            x = coord[0]
            y = coord[1] 
            count_black = 0
            count_empty = 0
            count_boundaries = 0
            
            checked = []

            for i in range(x-1, y+2):
                for j in range(x-1, y+2):
                    if not (i, j) in checked:
                        if self._board._isOnBoard(i, j):
                            if (self._board[Goban.Board.flatten((i, j))] == 1):
                                count_black += 1
                            elif (self._board[Goban.Board.flatten((i, j))] == 0):
                                count_empty += 1
                            elif (self._board[Goban.Board.flatten((i, j))] == 2):
                                return 0
                        else:
                            count_boundaries += 1
                        if (count_black + count_empty + count_boundaries == 6) and count_black >= 1:
                            controled_intersection += 1
                            checked.append((i, j))
    
        return controled_intersection
                    

    """
    Renvoie le nombre d'intersections contrôlées par Blanc
    """
    def _count_controled_intersection_white(self):
        controled_intersection = 0
        for move in self._white_moves:
            coord = Goban.Board.name_to_coord(move)
            x = coord[0]
            y = coord[1] 
            count_white = 0
            count_empty = 0
            count_boundaries = 0
            
            checked = []

            for i in range(x-1, y+2):
                for j in range(x-1, y+2):
                    if not (i, j) in checked:
                        if self._board._isOnBoard(i, j):
                            if (self._board[Goban.Board.flatten((i, j))] == 2):
                                count_white += 1
                            elif (self._board[Goban.Board.flatten((i, j))] == 0):
                                count_empty += 1
                            elif (self._board[Goban.Board.flatten((i, j))] == 1):
                                return 0
                        else:
                            count_boundaries += 1
                        if (count_white + count_empty + count_boundaries == 6) and count_white >= 1:
                            controled_intersection += 1
                            checked.append((i, j))
    
        return controled_intersection


    """
    Retourne vrai si un groupe de pierres Noires délimite un territoire dans un coin    
    """
    def _territory_black(self, move):
        coord = Goban.Board.name_to_coord(move)
        x = coord[0]
        y = coord[1]
        ymin = 0
        ymax = 0
        res = True

        # Le pierre se situe à droite
        if (5 <= x <= 6) and (self._board[Goban.Board.flatten((x, y))] == 1):
            for i in range(y+1, 9):
                # On s'arrête à la fin de la chaîne
                if self._board[Goban.Board.flatten((x, i))] != 1:
                    ymax = i-1
                # La chaîne va jusqu'en haut
                elif self._board[Goban.Board.flatten((x, 8))] == 1:
                    ymax = 8
            for i in range(y, -1, -1):
                if self._board[Goban.Board.flatten((x, i))] != 1:
                    ymin = i+1
                elif self._board[Goban.Board.flatten((x, 0))] == 1:
                    ymin = 0

        for i in range(x+1, 9):
            if not (((self._board[Goban.Board.flatten((i, ymax))] == 1) and (self._board[Goban.Board.flatten((i, ymin))] != 1))):
                res = False
        for i in range(x+1, 9):
            for j in range(ymin+1, ymax):
                if not (self._board[Goban.Board.flatten((i, j))] == 0):
                    res = False   
        return res

    """
    Afin de simplifier la gestion des territoires (en particulier dans Opening.py)
    le plateau est découpé en 8 parties    
    """          
    def in_N(self, x, y):
        return (3 <= x <= 5) and (6 <= y <= 8)

    def in_E(self, x, y):
        return (6 <= x <= 8) and (3 <= y <= 5)

    def in_O(self, x, y):
        return (0 <= x <= 2) and (3 <= y <= 5)

    def in_S(self, x, y):
        return (3 <= x <= 5) and (0 <= y <= 2)

    def in_NE(self, x, y):
        return (6 <= x <= 8) and (6 <= y <= 8)

    def in_NO(self, x, y):
        return (0 <= x <= 2) and (6 <= y <= 8)

    def in_SO(self, x, y):
        return (0 <= x <= 2) and (0 <= y <= 2)

    def in_SE(self, x, y):
        return (6 <= x <= 8) and (0 <= y <= 2)


    """
    Nombre de territoires cardinaux détenus par Noir 
    """
    def count_territories_black(self):
        count = 0
        if self.north_territory()[0] >= 1:
            count = count + 1
        if self.south_territory()[0] >= 1:
            count = count + 1
        if self.east_territory()[0] >= 1:
            count = count + 1
        if self.west_territory()[0] >= 1:
            count = count + 1
        if self.north_east_territory()[0] >= 1:
            count = count + 1
        if self.north_west_territory()[0] >= 1:
            count = count + 1
        if self.south_east_territory()[0] >= 1:
            count = count + 1
        if self.south_west_territory()[0] >= 1:
            count = count + 1
        return count

    """
    Nombre de territoires cardinaux détenus par Blanc
    """
    def count_territories_white(self):
        count = 0
        if self.north_territory()[1] >= 1:
            count = count + 1
        if self.south_territory()[1] >= 1:
            count = count + 1
        if self.east_territory()[1] >= 1:
            count = count + 1
        if self.west_territory()[1] >= 1:
            count = count + 1
        if self.north_east_territory()[1] >= 1:
            count = count + 1
        if self.north_west_territory()[1] >= 1:
            count = count + 1
        if self.south_east_territory()[1] >= 1:
            count = count + 1
        if self.south_west_territory()[1] >= 1:
            count = count + 1
        return count


    """
    Fonctions permettant de définir si un territoire est contrôlé par 
    les Blancs ou par les Noirs    
    """
    def north_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_N(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_N(x, y):
                w = w + 1
        return b, w, b >= w

    def north_east_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_NE(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_NE(x, y):
                w = w + 1
        return b, w, b >= w

    def north_west_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_NO(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_NO(x, y):
                w = w + 1
        return b, w, b >= w

    def east_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_E(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_E(x, y):
                w = w + 1
        return b, w, b >= w

    def south_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_S(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_S(x, y):
                w = w + 1
        return b, w, b >= w

    def south_east_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_SE(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_SE(x, y):
                w = w + 1
        return b, w, b >= w

    def south_west_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_SO(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_SO(x, y):
                w = w + 1
        return b, w, b >= w

    def west_territory(self):
        b = 0
        w = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_O(x, y):
                b = b + 1

        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self.in_O(x, y):
                w = w + 1
        return b, w, b >= w



