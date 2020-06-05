# -*- coding: utf-8 -*-


import Goban
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Cette classe permet de gérer les territoires et la répartition des pierres sur le Goban.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Territory:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves

    """
    Distance entre deux pierres
    """
    def distance(self, A, B):
        dist = np.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        return dist

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
    Revoie vrai si la pierre se trouve sur les bords, faux sinon.
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
    Renvoie le nombre d'intersections contrôlés par Noir
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
                    

        


    # Retourne vrai si un groupe de pierre délimite un territoire dans un coin
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

    # True si attaque sur le territoire des Noirs
    def adversary_attack_black(self, territory):
        res = False
        if territory == "N":
            if self.north_territory[2]:
                res = True
        if territory == "S":
            if not self.south_territory[2]:
                res = True
        if territory == "E":
            if not self.east_territory[2]:
                res = True
        if territory == "O":
            if not self.west_territory[2]:
                res = True
        if territory == "NE":
            if not self.north_east_territory[2]:
                res = True
        if territory == "NO":
            if not self.north_west_territory[2]:
                res = True
        if territory == "SE":
            if not self.south_east_territory[2]:
                res = True
        if territory == "SO":
            if not self.south_west_territory[2]:
                res = True
        return res


# Return True si le territoire appartient à Noir, False sinon
# Ainsi que le nombre de pièces dans chaque territoire

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

    # Return True si le territoire appartient à Noir, False sinon
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

    # Return True si le territoire appartient à Noir, False sinon
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

    # Return True si le territoire appartient à Noir, False sinon
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
