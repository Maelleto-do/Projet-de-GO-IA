class Shape:


    def __init__(self, board, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._black_moves = black_moves
        self._white_moves = white_moves


    def _is_nobi(self, x, y, last_move):
        res = False
        if( (x == last_move[0] + 1) or ( x == last_move[0] - 1) ):
            if ( y == last_move[1] ):
                res = True
        elif ( (y == last_move[1] + 1) or ( y == last_move[1] - 1) ):
            if ( x == last_move[1] ):
                res = True
        return res

    def _is_tobi(self, x, y, last_move):
        res = False
        if( (x == last_move[0] + 2) or ( x == last_move[0] - 2) ) and ( y == last_move[1] ):
                res = True
        elif ( (y == last_move[1] + 2) or ( y == last_move[1] - 2) ) and ( x == last_move[1] ):
                res = True
        return res
