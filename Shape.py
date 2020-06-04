import Goban


class Shape:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves

    def _living_group_black(self, move):
        res = False
        first_block = 0
        second_block = 0
        first_eye = Goban.Board.unflatten(move)
        x = first_eye[0]
        y = first_eye[1]
        neighbors_first_eye = [(x+1, y), (x-1, y), (x, y+1), (x, y-1),
                               (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]

        for n in neighbors_first_eye:
            if not self._board._isOnBoard(n[0], n[1]):
                first_block += 1
            elif (self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK):
                first_block += 1
        # On regarde s'il y a un autre oeil
        possible_eyes = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
        for n in possible_eyes:
            x = n[0]
            y = n[1]
            neighbors_second_eye = [(x+1, y), (x-1, y), (x, y+1), (x, y-1),
                                    (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
            for n in neighbors_second_eye:
                if not self._board._isOnBoard(n[0], n[1]):
                    second_block += 1
                elif (self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK):
                    second_block += 1
        if first_block + second_block == 16:
            res = True
        return res

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

    def _diamond(self, color):
        moves = []
        if color == "BLACK":
            moves = self._black_moves
        else:
            moves = self._white_moves

        res = False
        count = 0
        checked = []

        for move in moves:
            coord = Goban.Board.name_to_coord(move)
            x = coord[0]
            y = coord[1]
            neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            neighbors = [
                c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]

            for n in neighbors:
                if color == "BLACK":
                    if (self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK) and (n not in checked):
                        res = True
                else:
                    if (self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE) and (n not in checked):
                        res = True
            if res:
                count += 1
                checked.append(coord)
                for n in neighbors:
                    checked.append(n)
        return count

    # Fermer territoire

    def _is_nobi(self, x, y, last_move):
        res = False
        if(((x == last_move[0] + 1) or (x == last_move[0] - 1)) and (y == last_move[1])):
            res = True
        elif (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0])):
            res = True
        return res

    # S'étendre et fermer territoire
    def _is_tobi(self, x, y, last_move):
        res = False
        if (((x == last_move[0] + 2) or (x == last_move[0] - 2)) and (y == last_move[1])):
            res = True
        elif ((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0]):
            res = True
        return res

    # Attaquer
    def _is_kosumi(self, x, y, last_move):
        res = False
        if (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0] + 1)):
            res = True
        elif (((y == last_move[1] + 1) or (y == last_move[1] - 1)) and (x == last_move[0] - 1)):
            res = True
        return res

    # Attaquer ou agrandir territoire
    def _is_keima(self, x, y, last_move):
        res = False
        if (((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0] + 1)):
            res = True
        elif (((y == last_move[1] + 2) or (y == last_move[1] - 2)) and (x == last_move[0] - 1)):
            res = True
        return res
