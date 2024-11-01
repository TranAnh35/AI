import copy, math, time

from const import *
from piece import *
from board import *

class AI:
        
    def pickSpot(self, board):
        best_score = -math.inf
        best_move = None
        
        print('\nFinding best move...')
        start_time = time.time()
        
        for row in range(ROWS):
            for col in range(COLS):
                if not board.squares[row][col].piece:
                    board.squares[row][col].piece = O()
                    score = self._minimax(board, 0, False, -math.inf, math.inf)
                    board.squares[row][col].piece = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        end_time = time.time()
        print(f'Time taken to find best move: {end_time - start_time:.2f} seconds')
                        
        return best_move
        
    def _minimax(self, board, depth, maximizing, alpha, beta):
        result = board.game_over()
        if result == 'X win':
            return -10
        elif result == 'O win':
            return 10
        elif result == 'Draw':
            return 0
        
        if maximizing:
            best_score = -math.inf
            prune = False
            for row in range(ROWS):
                if prune:
                    break
                for col in range(COLS):
                    if not board.squares[row][col].piece:
                        board.squares[row][col].piece = O()
                        score = self._minimax(board, depth + 1, False, alpha, beta)
                        best_score = max(best_score, score)
                        alpha = max(alpha, score)
                        board.squares[row][col].piece = None
                        if beta <= alpha:
                            prune = True
                            break
            return best_score
        else:
            best_score = math.inf
            prune = False
            for row in range(ROWS):
                if prune:
                    break
                for col in range(COLS):
                    if not board.squares[row][col].piece:
                        board.squares[row][col].piece = X()
                        score = self._minimax(board, depth + 1, True, alpha, beta)
                        best_score = min(best_score, score)
                        beta = min(beta, score)
                        board.squares[row][col].piece = None
                        if beta <= alpha:
                            prune = True
                            break
            return best_score