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


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):

        max = -1000000
        alpha = -1000000
        beta = +1000000
        depth = 2

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

        best_move = 0

        for move in self._board.legal_moves():
            self._board.push(move)
            val = self.alphabeta(alpha, beta, False, depth-1)
            self._board.pop()
            if val > alpha:
                alpha = val
                best_move = move

        self._board.push(best_move)
        return Goban.Board.flat_to_name(best_move)

    def alphabeta(self, alpha, beta, maximizePlayer, depth):

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
                return -50
            if res == "0-1":
                return 50
            else:
                return 0

        if depth == 0:
            res = self.evaluate(moves)
            return res

        # AMI
        if maximizePlayer:
            for move in self._board.legal_moves():
                self._board.push(move)
                alpha = max(alpha, self.alphabeta(
                    alpha, beta, False, depth - 1))
                self._board.pop()
                if alpha >= beta:
                    return beta
            return alpha
        # ENNEMI
        else:
            for move in self._board.legal_moves():
                self._board.push(move)
                beta = min(beta, self.alphabeta(
                    alpha, beta, True, depth - 1))
                self._board.pop()
                if alpha >= beta:
                    return alpha
            return beta

    def evaluate(self, moves):

        black_moves = []
        res = 0
        for move in moves:
            # move_str = Goban.Board.flat_to_name(move)
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]
            if self._board[Goban.Board.flatten((x, y))] == self._board._BLACK:
                black_moves.append(move)

        print("BLACK MOOOOOOVES : ", black_moves)
        for move in black_moves:
            # move_str = Goban.Board.flat_to_name(move)
            ufcoord = Goban.Board.name_to_coord(move)
            x = ufcoord[0]
            y = ufcoord[1]

            neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            neighbors = [
                c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
            for n in neighbors:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    res = res + 200

            diag_coord = (x+1, y+1)
            if self._board._isOnBoard(diag_coord[0], diag_coord[1]):
                if self._board[Goban.Board.flatten((diag_coord[0], diag_coord[1]))] == self._board._BLACK:
                    res = res + 1000

        return res

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
