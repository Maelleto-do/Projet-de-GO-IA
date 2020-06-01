# -*- coding: utf-8 -*-


import Goban


class Territory:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves

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
            if not self.north_territory[2]:
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
        return b, w, b > w

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
        return b, w, b > w
    
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
        return b, w, b > w
    
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
        return b, w, b > w
    
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
        return b, w, b > w
    
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
        return b, w, b > w

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
        return b, w, b > w
    
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
        return b, w, b > w
