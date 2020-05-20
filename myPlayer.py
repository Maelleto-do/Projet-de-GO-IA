# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
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

    def getPlayerMove(self, move):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        max = -123456
        alpha = -1234567
        beta = +1234567

        for move in self._board.legal_moves():
            self._board.push(move)
            print("I am playing ", self._board.move_to_str(move))
            print("My current board :")
            self._board.prettyPrint()
            val = self.alphabeta(alpha, beta, True)
            self._board.pop()
            if val > alpha:
                alpha = val
                best_move = move
        return Goban.Board.flat_to_name(best_move)

    def alphabeta(self, alpha, beta, maximizePlayer):
        # AMI
        if maximizePlayer:
            for move in self._board.legal_moves():
                self._board.push(move)
                alpha = max(alpha, self.alphabeta(alpha, beta, False))
                self._board.pop()
                if alpha >= beta:
                    return beta
            return alpha
        # ENNEMI
        else:
            for move in self._board.legal_moves():
                self._board.push(move)
                beta = min(beta, self.alphabeta(alpha, beta, True))
                self._board.pop()
                if alpha >= beta:
                    return alpha
            return beta

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
