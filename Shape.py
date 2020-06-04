import Goban


class Shape:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves

#     def _living_group_black(self, move):
#         res = False
#         first_block = 0
#         second_block = 0
#         first_eye = Goban.Board.unflatten(move)
#         x = first_eye[0]
#         y = first_eye[1]
#         neighbors_first_eye = [(x+1, y), (x-1, y), (x, y+1), (x, y-1),
#                                (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]

#         for n in neighbors_first_eye:
#             if not self._board._isOnBoard(n[0], n[1]):
#                 first_block += 1
#             elif (self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK):
#                 first_block += 1
#         # On regarde s'il y a un autre oeil
#         possible_eyes = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
#         for n in possible_eyes:
#             x = n[0]
#             y = n[1]
#             neighbors_second_eye = [(x+1, y), (x-1, y), (x, y+1), (x, y-1),
#                                     (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
#             for n in neighbors_second_eye:
#                 if not self._board._isOnBoard(n[0], n[1]):
#                     second_block += 1
#                 elif (self._board[Goban.Board.flatten((n[0], n[1]))] == 1):
#                     second_block += 1
#         if first_block + second_block == 16:
#             res = True
#         return res

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
                        print("OUIIIIIIIIIIIIIIIIIIIIIIIIIIII")
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
                        print("OUIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                        return True
      
        return False



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

    # S'étendre et fermer territoire
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

    # Attaquer
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

    # Attaquer ou agrandir territoire
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
