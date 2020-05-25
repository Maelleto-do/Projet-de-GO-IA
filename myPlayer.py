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

    def getPlayerMove(self):

        max = -100
        alpha = -100
        beta = +100
        depth = 3

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

            # best_move_str = Goban.Board.flat_to_name(best_move)
            # coord = Goban.Board.name_to_coord(best_move_str)
            # x = coord[0]
            # y = coord[1]
            # neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            # res_neighbors = [
            #     c for c in neighbors if self._board._isOnBoard(c[0], c[1])]
            # print("MES COORDONNEES " + str(x) + "," + str(y))
            # print("VOISINNNNS  " + str(res_neighbors))

            # if (Goban.Board[self._board.flatten((coord[0],coord[1]))] == 0):
            #     print("BLAAAACK")
            # print("BEST MOVE " + Goban.Board.flat_to_name(best_move)
            #     + " " + str(self._board[Goban.Board.flatten((coord[0],coord[1]))]) + " " + str(self._board._BLACK) )
            # if (Goban.Board[Goban.Board.flatten((coord[0],coord[1]))] == Goban.Board._WHITE):
            #     print("WHIIIITE")
            #     print("BEST MOVE " + Goban.Board.flat_to_name(best_move))
            # if self._board._nextPlayer == self._board._WHITE:
            #     print("WHIIIITE")

            # else:
            #     print("BLAAAACK")
            # best_move_str = Goban.Board.flat_to_name(best_move)
            # print("COORDONEES ", Goban.Board.name_to_coord(best_move_str))
            # print("BEST MOVE " + Goban.Board.flat_to_name(best_move))
        self._board.push(best_move)
        return Goban.Board.flat_to_name(best_move)

    def alphabeta(self, alpha, beta, maximizePlayer, depth):
        my_move = 0
        if self._board.is_game_over() or depth == 0:
            res = self._board.result()
            if res == "1-0":
                return -60
            if res == "0-1":
                return 60
            else:
                return self.evaluate(my_move)

            
        # AMI
        if maximizePlayer:
            for move in self._board.legal_moves():
                self._board.push(move)
                my_move = move
                # print("FRIEND MOVE " + Goban.Board.flat_to_name(my_move))
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
                # my_move = move
                beta = min(beta, self.alphabeta(alpha, beta, True, depth - 1))
                self._board.pop()
                if alpha >= beta:
                    return alpha
            return beta

    def evaluate(self, move):
        move_str = Goban.Board.flat_to_name(move)
        ufcoord = Goban.Board.name_to_coord(move_str)
        # print("MOUVE " + move_str)
        x = ufcoord[0]
        y = ufcoord[1]
        neighbors_coord = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        neighbors = [
            c for c in neighbors_coord if self._board._isOnBoard(c[0], c[1])]
        res = 0
        for n in neighbors:
            if self._board[Goban.Board.flatten((n[0], n[1]))] == self._board._BLACK:
                res = res + 200
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
