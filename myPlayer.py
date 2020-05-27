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

        max = -10000
        alpha = -10000
        beta = +10000
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
        if self._board.is_game_over() or depth == 0:
            res = self._board.result()
            if res == "1-0":
                return -50
            if res == "0-1":
                return 50
            else:
                res = self.evaluate()
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
                beta = min(beta, self.alphabeta(alpha, beta, True, depth - 1))
                self._board.pop()
                if alpha >= beta:
                    return alpha
            return beta



    def evaluate(self):
        black_moves = []
        res = 0
        for move in self._board.legal_moves():
            move_str = Goban.Board.flat_to_name(move)
            ufcoord = Goban.Board.name_to_coord(move_str)
            x = ufcoord[0]
            y = ufcoord[1]
            if self._board[Goban.Board.flatten((x, y))] == self._board._BLACK:
                black_moves.append(move)

        start = timeit.timeit()

        for move in black_moves:
            move_str = Goban.Board.flat_to_name(move)
            ufcoord = Goban.Board.name_to_coord(move_str)
            x = ufcoord[0]
            y = ufcoord[1]
            neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            neighbors = [
                c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
            for n in neighbors:
                if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                    res = res + 200
        end = timeit.timeit()
        if (start < end):
            print("TEMPS ECOULE pour evaluation  " + str(end - start))


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
