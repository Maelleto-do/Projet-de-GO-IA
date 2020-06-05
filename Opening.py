import Territory
import Goban
import Shape



class Opening:

    def __init__(self, board, mycolor, black_moves, white_moves, black_goban, white_goban):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._mycolor = mycolor

    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])


    """
        Fuseki (Ouverture)

        On cherche à atteindre le maximum de territoires sur le plateau (au nord, à l'est, etc)
        et à placer des coups sur la deuxième ligne.
                
    """
    def evaluate_opening(self):


        res = 0
        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)


        black = 0
        white = 0
        for move in self._black_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]

            if (1 <= x <= 7) and (1 <= y <= 7):  # pierres sur la deuxième ligne pour l'ouverture
                black = black + 3000


        for move in self._white_moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]

            if (1 <= x <= 7) and (1 <= y <= 7): # pierres sur la deuxième ligne pour l'ouverture
                white = white + 3000

        # On maximise le nombre de territoires conquéris
        black = black + territory.count_territories_black()
        white = white + territory.count_territories_white()

        
        if self._mycolor == Goban.Board._BLACK:
            res = black - white
        else:
            res = white - black

        return res
