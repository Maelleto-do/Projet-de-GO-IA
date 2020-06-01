class Shape:


    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves

    # Fermer territoire
    def _is_nobi(self, x, y, last_move):
        res = False
        if( ((x == last_move[0] + 1) or ( x == last_move[0] - 1)) and (y == last_move[1]) ):
                res = True
        elif ( ((y == last_move[1] + 1) or ( y == last_move[1] - 1)) and (x == last_move[0]) ):
                res = True
        return res

    # S'étendre et fermer territoire
    def _is_tobi(self, x, y, last_move):
        res = False
        if ( ((x == last_move[0] + 2) or ( x == last_move[0] - 2)) and (y == last_move[1]) ):
                res = True
        elif ( (y == last_move[1] + 2) or ( y == last_move[1] - 2) ) and ( x == last_move[0] ):
                res = True
        return res

    # Attaquer
    def _is_kosumi(self, x, y, last_move):
        res = False
        if ( ((y == last_move[1] + 1) or ( y == last_move[1] - 1))  and ( x == last_move[0] + 1 ) ):
                res = True
        elif ( ((y == last_move[1] + 1) or ( y == last_move[1] - 1))  and ( x == last_move[0] - 1 ) ):
                res = True
        return res

    # Attaquer ou agrandir territoire
    def _is_keima(self, x, y, last_move):
        res = False
        if ( ((y == last_move[1] + 2) or ( y == last_move[1] - 2))  and ( x == last_move[0] + 1 ) ):
                res = True
        elif ( ((y == last_move[1] + 2) or ( y == last_move[1] - 2))  and ( x == last_move[0] - 1 ) ):
                res = True
        return res

