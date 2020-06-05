# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import timeit
import Goban
from random import choice, randint
from playerInterface import *
import Territory
import Opening
import json
import Shape
import Game
import EndingGame


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
        self._last_best_move = 0
        self._start = 0
        self._end = 0

    def getPlayerName(self):
        return "Random Player"

    def get_last_black(self):
        if (self._black_goban != []):
            return self._board.unflatten(self._black_goban[-1])

    def get_last_white(self):
        if (self._white_goban != []):
            return self._board.unflatten(self._white_goban[-1])

    def get_last_enemy(self, color):
        if self._count == 0:
            return self._board._historyMoveNames[0]
        if self._count == 1:
            return self._board._historyMoveNames[1]

        if self._board._historyMoveNames != []:
            if self._board._nextPlayer == self._board._WHITE:
                if color == "BLACK":
                    return Goban.Board.coord_to_name(Goban.Board.unflatten(self._black_goban[-1]))
                else:
                    return self._board._historyMoveNames[(self._count * 2) - 1]
            else:
                if color == "BLACK":
                    return self._board._historyMoveNames[self._count * 2]
                else:
                    return Goban.Board.coord_to_name(Goban.Board.unflatten(self._white_goban[-1]))

    def getPlayerMove(self):

        max = -100000000000
        alpha = -100000000000
        beta = +100000000000
        depth = 10
        best_move = 0
        iterative_deepening_max_time = 3 
    

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




        # BIBLIOTHEQUE D'OUVERTURE

        with open("games.json", 'r') as json_data:
            data_opening = json.load(json_data)

        if self._count == 0 and self._mycolor == Goban.Board._BLACK:  # Premier coup à jouer pour noir
            for l in range(0, 510):
                i = randint(0, 510)
                if data_opening[i]['winner'] == "B":
                    best_move = data_opening[i]['moves'][0]
                    self._board.push(Goban.Board.flatten(
                        Goban.Board.name_to_coord(best_move)))
                    self._count = self._count + 1
                    self._black_goban.append(Goban.Board.flatten(
                        Goban.Board.name_to_coord(best_move)))
                    return best_move

        if self._count == 0 and self._mycolor == Goban.Board._WHITE:  # Premier coup à jouer pour blanc
            for i in range(0, 510):
                if data_opening[i]['moves'][0] == self.get_last_enemy("BLACK"):
                    best_move = data_opening[i]['moves'][1]
                    self._board.push(Goban.Board.flatten(
                        Goban.Board.name_to_coord(data_opening[i]['moves'][1])))
                    self._count = self._count + 1
                    self._white_goban.append(Goban.Board.flatten(
                        Goban.Board.name_to_coord(best_move)))
                    return best_move

        elif self._count == 1 and self._mycolor == Goban.Board._BLACK:  # Deuxième coup à jouer pour black
            for i in range(0, 510):
                if data_opening[i]['moves'][1] == self.get_last_enemy("WHITE"):
                    best_move = data_opening[i]['moves'][2]
                    self._board.push(Goban.Board.flatten(
                        Goban.Board.name_to_coord(data_opening[i]['moves'][2])))
                    self._count = self._count + 1
                    self._black_goban.append(Goban.Board.flatten(
                        Goban.Board.name_to_coord(best_move)))
                    return best_move


        # ITERATIVE DEEPENING
        last_val = 0
        self._start = timeit.default_timer()
        while (self._end - self._start) <= iterative_deepening_max_time:
            for move in self._board.legal_moves():
                self._board.push(move)
                val = self.alphabeta(
                    alpha, beta, False, depth-1)
                self._board.pop()
                self._end = timeit.default_timer()
                if val > alpha:
                    alpha = val
                    self._last_best_move = move
            depth += 1

        best_move = self._last_best_move

        if self._mycolor == Goban.Board._BLACK:
            self._black_goban.append(best_move)
        else:
            self._white_goban.append(best_move)

        self._board.push(best_move)
        self._count = self._count + 1

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
                return -900
            if res == "0-1":
                return 900
            else:
                return self.evaluate(moves)

        if depth == 0:
            res = self.evaluate(moves)
            return res

        # AMI
        if maximizePlayer == True:
            for move in self._board.legal_moves():
                self._board.push(move)
                alpha = max(alpha, self.alphabeta(
                    alpha, beta, False, depth - 1))
                self._board.pop()
                if alpha >= beta:
                    return beta
                return alpha

        # ENNEMI
        elif maximizePlayer == False:
            for move in self._board.legal_moves():
                self._board.push(move)
                beta = min(beta, self.alphabeta(
                    alpha, beta, True, depth - 1))
                self._board.pop()
                self._end = timeit.default_timer()
                if alpha >= beta:
                    return alpha
                return beta



    def evaluate(self, moves):

        black_moves = []
        white_moves = []
        res = 0

        # On remplit les tableau de noirs et de blancs présents sur le plateau lors de l'appel de l'heuristique
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

        if self._count <= 4:  # Evaluation Fuseki (début de jeu) pour les premiers coups, on cherche à prendre le maximum de territoires
            opening = Opening.Opening(
                self._board, self._mycolor, black_moves, white_moves, self._black_goban, self._white_goban)
            res = opening.evaluate_opening()
            return res

        else: # Appel de l'heuristique pour Chuban (milieu de jeu)
            game = Game.Game(
                self._board, self._mycolor, self._count, black_moves, white_moves, self._black_goban, self._white_goban )
            res = game.evaluation()
            return res
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
