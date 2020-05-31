import Goban


class MiddleGame:

    def __init__(self, board, black_moves, white_moves, black_goban, white_goban, friend, enemy):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._friend = friend
        self._enemy = enemy

    def evaluation(self):
        res = 0
        # On évalue la position des pions NOIRS sur le plateau
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]

            # Les pions ne doivent pas être eparpillés sur le plateau
            # On favorise deux pions côte à côte
            neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            neighbors = [
                c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
            for n in neighbors:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    res = res + self._friend*400

            # Les pions alignés doivent former une diagonale
            diag_coord = (x+1, y+1)
            if self._board._isOnBoard(diag_coord[0], diag_coord[1]):
                if self._board[Goban.Board.flatten((diag_coord[0], diag_coord[1]))] == self._board._BLACK:
                    res = res + self._friend*100

        # On évalue la position des pions BLANCS sur le plateau
        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]

            # Les pions ne doivent pas être eparpillés sur le plateau
            # On favorise deux pions côte à côte
            neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            neighbors = [
                c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
            for n in neighbors:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
                    res = res + self._enemy*400

            # Les pions alignés doivent former une diagonale
            diag_coord = (x+1, y+1)
            if self._board._isOnBoard(diag_coord[0], diag_coord[1]):
                if self._board[Goban.Board.flatten((diag_coord[0], diag_coord[1]))] == self._board._WHITE:
                    res = res + self._enemy*100

        return res
