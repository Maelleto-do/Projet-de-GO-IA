# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import timeit
import Goban
from random import choice
from playerInterface import *
import Territory
import Opening
import json
import Shape
import MiddleGame


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._black_goban = []
        self._white_goban = []
        self._count = 0

    def getPlayerName(self):
        return "Random Player"

    # def in_N(self, x, y):
    #     return (3 <= x <= 5) and (6 <= y <=8)
    # def in_E(self, x, y):
    #     return (6 <= x <= 8) and (3 <= y <= 5)
    # def in_O(self, x, y):
    #     return (0 <= x <= 2) and (3 <= y <= 5)
    # def in_S(self, x, y):
    #     return (3 <= x <= 5) and (0 <= y <= 2)

    # def in_NE(self, x, y):
    #     return (6 <= x <=8) and (6 <= y <=8)
    # def in_NO(self, x, y):
    #     return (0 <= x <= 2) and (6 <= y <= 8)
    # def in_SO(self, x, y):
    #     return (0 <= x <= 2) and (0 <= y <= 2)
    # def in_SE(self, x, y):
    #     return (6 <= x <= 8) and (0 <= y <= 2)

    # # Return True si le territoire appartient à Noir, False sinon
    # # Ainsi que le nombre de pièces dans chaque territoire
    # def north_territory(self, x, y, black_moves, white_moves):
    #     b = 0
    #     w = 0
    #     for move in black_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_N(x, y):
    #             b = b + 1

    #     for move in white_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_N(x, y):
    #             w = w + 1
    #     return b, w, b > w

    # # Return True si le territoire appartient à Noir, False sinon
    # def east_territory(self, x, y, black_moves, white_moves):
    #     b = 0
    #     w = 0
    #     for move in black_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_E(x, y):
    #             b = b + 1

    #     for move in white_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_E(x, y):
    #             w = w + 1
    #     return b, w, b > w

    # # Return True si le territoire appartient à Noir, False sinon
    # def south_territory(self, x, y, black_moves, white_moves):
    #     b = 0
    #     w = 0
    #     for move in black_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_S(x, y):
    #             b = b + 1

    #     for move in white_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_S(x, y):
    #             w = w + 1
    #     return b, w, b > w

    # # Return True si le territoire appartient à Noir, False sinon
    # def west_territory(self, x, y, black_moves, white_moves):
    #     b = 0
    #     w = 0
    #     for move in black_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_O(x, y):
    #             b = b + 1

    #     for move in white_moves:
    #         ufcoord = Goban.Board.name_to_coord(move)
    #         x = ufcoord[0]
    #         y = ufcoord[1]
    #         if self.in_O(x, y):
    #             w = w + 1
    #     return b, w, b > w

    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])

    def getPlayerMove(self):

        max = -100000000
        alpha = -100000000
        beta = +100000000
        depth = 7
        best_move = 0
        start = 0
        first_black = self._board.name_to_coord('G7')
        flatt_first_black = self._board.flatten(first_black)

        second_black = self._board.name_to_coord('F3')
        flatt_second_black = self._board.flatten(second_black)

        first_white = self._board.name_to_coord('C4')
        flatt_first_white = self._board.flatten(first_white)

        second_white = self._board.name_to_coord('C7')
        flatt_second_white = self._board.flatten(second_white)

        moves = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'A2', 'B2',
                 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'A3', 'B3', 'C3', 'D3',
                 'E3', 'F3', 'G3', 'H3', 'J3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4',
                 'G4', 'H4', 'J4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
                 'J5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6', 'A7',
                 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7', 'A8', 'B8', 'C8',
                 'D8', 'E8', 'F8', 'G8', 'H8', 'J8', 'A9', 'B9', 'C9', 'D9', 'E9',
                 'F9', 'G9', 'H9', 'J9', 'PASS']

        # for move in moves:
        #     ufcoord = Goban.Board.name_to_coord(move)
        #     x = ufcoord[0]
        #     y = ufcoord[1]
        #     if (self._board[Goban.Board.flatten((x, y))] == self._board._BLACK) or (self._board[Goban.Board.flatten((x, y))] == self._board._WHITE):
        #         count = count + 1

        # if count == 0:
        #     self._board.push(flatt_first_black)
        #     return self._board.flat_to_name(flatt_first_black)
        # if count == 1:
        #     self._board.push(flatt_first_white)
        #     return self._board.flat_to_name(flatt_first_white)
        # if count == 2:
        #     self._board.push(flatt_second_black)
        #     return self._board.flat_to_name(flatt_second_black)
        # if count == 3:
        #     self._board.push(flatt_second_white)
        #     return self._board.flat_to_name(flatt_second_white)

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            res = self._board.result()
            if res == "1-0":
                print("White wins")
            if res == "0-1":
                print("Black wins")
            else:
                print("equal")
            return "PASS"

        for move in self._board.legal_moves():
            self._board.push(move)
            val = self.alphabeta(alpha, beta, False, depth-1, move, start)
            self._board.pop()
            if val > alpha:
                alpha = val
                best_move = move

        self._board.push(best_move)
        self._count = self._count + 1

        if self._board.next_player() == self._board._WHITE:
            self._black_goban.append(best_move)
        else:
            self._white_goban.append(best_move)
        return Goban.Board.flat_to_name(best_move)

    def alphabeta(self, alpha, beta, maximizePlayer, depth, move, start):

        moves = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'A2', 'B2',
                 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'A3', 'B3', 'C3', 'D3',
                 'E3', 'F3', 'G3', 'H3', 'J3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4',
                 'G4', 'H4', 'J4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
                 'J5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6', 'A7',
                 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7', 'A8', 'B8', 'C8',
                 'D8', 'E8', 'F8', 'G8', 'H8', 'J8', 'A9', 'B9', 'C9', 'D9', 'E9',
                 'F9', 'G9', 'H9', 'J9', 'PASS']

        if self._board.is_game_over():
            res = self._board.result()
            if res == "1-0":
                return -500
            if res == "0-1":
                return 500
            else:
                return 0

        if depth == 0:
            res = self.evaluate(moves, maximizePlayer, move)
            # print("REEEEEEEEEEES ", res)
            return res

        # AMI
        if maximizePlayer == True:
            for move in self._board.legal_moves():
                end = timeit.default_timer()
                self._board.push(move)
                alpha = max(alpha, self.alphabeta(
                    alpha, beta, False, depth - 1, move, start))
                self._board.pop()
                if alpha >= beta:
                    return beta
                return alpha

        # ENNEMI
        elif maximizePlayer == False:
            for move in self._board.legal_moves():
                end = timeit.default_timer()
                self._board.push(move)
                beta = min(beta, self.alphabeta(
                    alpha, beta, True, depth - 1, move, start))
                self._board.pop()
                if alpha >= beta:
                    return alpha
                return beta

    def evaluate(self, moves, maximizePlayer, move):

        black_moves = []
        white_moves = []
        last_move = move
        res = 0

        # if self._board.next_player() == self._board._BLACK:
        #     next_player = "BLACK"
        # else:
        #     next_player = "WHITE"

        # print("LAST MOVE ", self._board.flat_to_name(last_move))
        # La fonction d'évaluation doit etre symétrique
        # if maximizePlayer:

        # else:
        #     ami = -1
        #     ennemi = 1
        ami = 1
        ennemi = -1
        # On remplit les tableau de noirs et de blancs présents sur le plateau
        for move in moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self._board[Goban.Board.flatten((x, y))] == self._board._BLACK:
                black_moves.append(move)
        for move in moves:
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self._board[Goban.Board.flatten((x, y))] == self._board._WHITE:
                white_moves.append(move)

        # with open("games.json", 'r') as json_data:
        #     data_opening = json.load(json_data)
        #     print(data_opening[0]['moves'])

        # last_black_move = self._black_goban[-1]
        # for i in range(0, 509):
        #     for w_move in white_moves:
        #         if (data_opening[i]['moves'][0 + 2*k] == last_black_move) and (data_opening[i]['moves'][0 + 3*k] == w_move):
        #             res = res + 1000
        #             k = k+1
        #         else:
        #             break
        #     return res

        if self._count < 2:  # Evaluation Fuseki pour les premiers coups
            opening = Opening.Opening(
                self._board, self._mycolor, black_moves, white_moves, self._black_goban, self._white_goban)
            res = opening.evaluate_opening()
            return res
        else:
            middle = MiddleGame.MiddleGame(
                self._board, self._mycolor, black_moves, white_moves, self._black_goban, self._white_goban)
            res = middle.evaluation()
            return res
        # # On évalue la position des pions NOIRS sur le plateau
        # for move in black_moves:
        #     ufcoord = Goban.Board.name_to_coord(move)
        #     x = ufcoord[0]
        #     y = ufcoord[1]

        #     # Les pions ne doivent pas être eparpillés sur le plateau
        #     # On favorise deux pions côte à côte
        #     neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        #     neighbors = [
        #         c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        #     for n in neighbors:
        #         if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
        #             res = res + ami*400

        #     # Les pions alignés doivent former une diagonale
        #     diag_coord = (x+1, y+1)
        #     if self._board._isOnBoard(diag_coord[0], diag_coord[1]):
        #         if self._board[Goban.Board.flatten((diag_coord[0], diag_coord[1]))] == self._board._BLACK:
        #             res = res + ami*100

        # # On évalue la position des pions BLANCS sur le plateau
        # for move in white_moves:
        #     ufcoord = Goban.Board.name_to_coord(move)
        #     x = ufcoord[0]
        #     y = ufcoord[1]

        #     # Les pions ne doivent pas être eparpillés sur le plateau
        #     # On favorise deux pions côte à côte
        #     neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        #     neighbors = [
        #         c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        #     for n in neighbors:
        #         if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._WHITE:
        #             res = res + ennemi*400

        #     # Les pions alignés doivent former une diagonale
        #     diag_coord = (x+1, y+1)
        #     if self._board._isOnBoard(diag_coord[0], diag_coord[1]):
        #         if self._board[Goban.Board.flatten((diag_coord[0], diag_coord[1]))] == self._board._WHITE:
        #             res = res + ennemi*100

        return res

    # # Fuseki
    # def evaluate_opening(self, moves, black_moves, white_moves, move):

    #     # On cherche à atteindre les coins et les bords
    #     # et à placer des coups sur la deuxième ligne
    #     res = 0

    #     if self._board.next_player() == self._board._BLACK:
    #         ami = 1
    #         ennemi = 1
    #     else:
    #         ami = 1
    #         ennemi = 1

    #     b = 0

    #     territory = Territory.Territory(self._board, black_moves, white_moves)

    #     if self._board.next_player() == self._board._BLACK:
    #         for move in black_moves:
    #             ufcoord = Goban.Board.name_to_coord(move)
    #             x = ufcoord[0]
    #             y = ufcoord[1]
    #             if self._black_goban != []:
    #                 ufcoord_last = self.get_last_black()
    #                 x_last = ufcoord_last[0]
    #                 y_last = ufcoord_last[1]
    #                 if ( abs(y_last - y) > 4):
    #                     res = res + ami*1000
    #                 if self._is_tobi(x, y, ufcoord_last):
    #                     res = res + ami*1000
    #             if (1 <= x <= 7) and (1 <= y <= 7): # se situe sur le deuxième ligne
    #                 res = res + ami*1000
    #             if ( ((1 <= x <= 2) or (6 <= x <= 7)) and ((1 <= y <= 2) or (6 <= y <= 7))): # dans un coin
    #                 res = res + ami*1000
    #             if ( territory.in_N(x, y) or territory.in_S(x, y) or territory.in_NE(x, y) or territory.in_SE(x, y) ):
    #                 res = res + ami*1000

    #             if ( (territory.north_territory(x, y)[0] == 1)
    #             or (territory.south_territory(x, y)[0] == 1)
    #             or (territory.east_territory(x, y)[0] == 1)
    #             or (territory.west_territory(x, y)[0] == 1) ):
    #                 res = res + ami*2000
    #     else:
    #         for move in white_moves:
    #             ufcoord = Goban.Board.name_to_coord(move)
    #             x = ufcoord[0]
    #             y = ufcoord[1]
    #             if (1 <= x <= 7) and (1 <= y <= 7): # se situe sur le deuxième ligne
    #                 res = res + ennemi*1000
    #             if ( ((1 <= x <= 2) or (6 <= x <= 7)) and ((1 <= y <= 2) or (6 <= y <= 7))): # dans un coin
    #                 res = res + ennemi*1000
    #             if ( territory.in_N(x, y) or territory.in_S(x, y) or territory.in_NE(x, y) or territory.in_SE(x, y) ):
    #                 res = res + ennemi*1000
    #             if ( (territory.north_territory(x, y)[1] == 1)
    #                 or (territory.south_territory(x, y)[1] == 1)
    #                 or (territory.east_territory(x, y)[1] == 1)
    #                 or (territory.west_territory(x, y)[1] == 1) ):
    #                 res = res + ennemi*2000

    #     return res

    def playOpponentMove(self, move):
        print("Opponent played ", move)  # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
