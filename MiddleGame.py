import Goban
import Territory
import Shape


class MiddleGame:

    def __init__(self, board, mycolor, count, black_moves, white_moves, black_goban, white_goban ):
        self._board = board
        self._black_goban = black_goban
        self._white_goban = white_goban
        self._black_moves = black_moves
        self._white_moves = white_moves
        self._mycolor = mycolor
        self._count = count

    # Renvoie le dernier coup joué par color
    def get_last(self, color):
        if self._board._historyMoveNames != []:
            if color == "BLACK":
                return self._board._historyMoveNames[self._count * 2]
            else:
                return self._board._historyMoveNames[(self._count * 2) - 1]

    # Renvoie l'ensemble des libertés et le nombre de libertés d'une pierre de coordonées coord
    def liberties(self, coord):
        lib = 0
        liberties = []
        x = coord[0]
        y = coord[1]
        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        for n in neighbors:
            if (self._board[Goban.Board.flatten((n[0], n[1]))] == 0) and self._board._isOnBoard(n[0], n[1]):
                lib = lib + 1
            else:
                liberties.append(n)
        return lib, liberties

    # Total du nombre de libertés des Blancs
    def liberties_white(self):
        res = 0
        for move in self._white_moves:
            res = res + self.liberties(Goban.Board.name_to_coord(move))[0]
        return res

    # Total du nombre de libertés des Noirs
    def liberties_black(self):
        res = 0
        for move in self._black_moves:
            res = res + self.liberties(Goban.Board.name_to_coord(move))[0]
        return res

    # Nombre des pierres Noires sur le plateau
    def nb_black(self):
        res = 0
        for n in self._black_moves:
            res = res + 1
        return res

    # Nombre des pierres Blanches sur le plateau
    def nb_white(self):
        res = 0
        for n in self._white_moves:
            res = res + 1
        return res

    """
    Chuban (Milieu de Jeu)

    On cherche à:
    - composer des formes en diamant
    - attaquer et capturer les pierres adverses
    - mettre les pierres adverses en Atari et éviter sois-même d'être Atari
    - garder le maximum d'intersections pour notre couleur
    - éviter les coups sur les bords du plateau

    """

    def evaluation(self):

        # Gestion des territoires
        territory = Territory.Territory(
            self._board, self._black_moves, self._white_moves, self._black_goban, self._white_goban)
        
        # Gestion des formes
        shape = Shape.Shape(self._board, self._black_moves,
                            self._white_moves, self._black_goban, self._white_goban)
        black = 0
        white = 0


        """""""""""""""""""""""""""""
        Heuristique pour Noir
        """""""""""""""""""""""""""""

        if (self._black_goban != []):

            # Mise un d'une pierre de l'adversaire en Atari
            for move in self._white_moves:
                if shape._is_atari_white(Goban.Board.name_to_coord(move)):
                    black += 900

            # On parcourt l'ensemble des coups joués par Noir
            for move in self._black_moves:

                # La forme en diamant est plutôt avantagée, dans le cas où elle ne fait pas baisser les libertés
                if shape._diamond(move, "BLACK") and self.liberties(Goban.Board.name_to_coord(move))[0] >= 2:
                    black += 400

                for white_move in self._white_goban:
                    # Une pièce blanche a trop de libertés, il faut l'encercler
                    if ((self.liberties(Goban.Board.name_to_coord(white_move))[0] >= 2)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        black += 900
                    # Si elle n'a plus qu'une seule liberté, il faut la capturer pour capturer des pierres blanches
                    if ((self.liberties(Goban.Board.name_to_coord(white_move))[0] == 1)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        black += 900
                    
                # On évite que les pierres soient placés près des bords
                if not territory._in_border(move):
                    black += 400
                
            # Si coup joué par Noir se retrouve en atari, on augmente ses libertés en ajoutant une pierre
            for move in self._black_goban:
                black_coord = Goban.Board.unflatten(move)
                if shape._is_atari_black(black_coord):
                    for move in self._black_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_black = ufcoord[0]
                        y_black = ufcoord[1]
                        # On fait un Nobi pour augmenter les libertés, tout en faisant attention à ne pas 
                        # se remettre Atari
                        if ufcoord in self.liberties(black_coord)[1] and self.liberties(black_coord)[0] >= 2:
                            black = black + 1000

        """""""""""""""""""""""""""""
        Heuristique pour Blanc
        """""""""""""""""""""""""""""
        if (self._white_goban != []):

            # Mise un d'une pierre de l'adversaire en Atari
            for move in self._black_moves:
                if shape._is_atari_black(Goban.Board.name_to_coord(move)):
                    white += 900

            # On parcourt l'ensemble des coups joués par Blanc
            for move in self._white_moves:
                
                # La forme en diamant est plutôt avantagée, dans le cas où elle ne fait pas baisser les libertés
                if shape._diamond(move, "WHITE") and self.liberties(Goban.Board.name_to_coord(move))[0] >= 2:
                    white += 400

                # Une pièce Noir a trop de libertés, il faut l'encercler
                for black_move in self._black_goban:
                    if ((self.liberties(Goban.Board.name_to_coord(black_move))[0] >= 2)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        white += 900
                    # Si elle n'a plus qu'une seule liberté, il faut la capturer pour capturer des pierres noires
                    if ((self.liberties(Goban.Board.name_to_coord(black_move))[0] == 1)
                            and (move in self.liberties(Goban.Board.name_to_coord(move))[1])):
                        white += 900
                    
                # On évite que les pierres soient placés près des bords
                if not territory._in_border(move):
                    white += 400

            # Si coup joué par Blanc se retrouve en atari, on augmente ses libertés en ajoutant une pierre
            for move in self._white_goban:
                white_coord = Goban.Board.unflatten(move)
                if shape._is_atari_white(white_coord):
                    for move in self._white_moves:
                        ufcoord = Goban.Board.name_to_coord(move)
                        x_white = ufcoord[0]
                        y_white = ufcoord[1]
                        # On fait un Nobi pour augmenter les libertés tout en faisant attention à ne pas 
                        # se remettre Atari
                        if ufcoord in self.liberties(white_coord)[1] and self.liberties(white_coord)[0] >= 2:
                            white = white + 1000


        """""""""""""""""""""""""""""
        Calcul des pondérations
        """""""""""""""""""""""""""""
        black = black + 2000*self.liberties_black() + 1000*territory._count_controled_intersection_black()

        white = white + 2000*self.liberties_white() + 1000*territory._count_controled_intersection_white()


        if self._mycolor == Goban.Board._BLACK:
            return black - white
        else:
            return white - black

