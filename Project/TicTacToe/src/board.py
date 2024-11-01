from const import *
from square import Square

class Board:
    
    def __init__(self):
        self.squares = []
        self._create()
        self.last_click = None
        self.win_line = None
        self.winner = None
        
    def __str__(self):
        s = '\n'
        for row in range(ROWS):
            s += '[ '
            for col in range(COLS):
                sqr = self.squares[row][col]
                s += '[ ]' if sqr.is_empty() else f'[{str(sqr.piece)}]'
                s += ' '
            s += ']\n'
        return s
    
    # ------------
    # INIT METHODS
    # ------------
    
    def _create(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        
    def _check_line(self, *positions):
        pieces = [self.squares[row][col].piece for row, col in positions]
        return all(piece is not None and piece.name == pieces[0].name for piece in pieces)
    
    # -------------
    # Other methods
    # -------------
    
    def add_piece(self, row, col, piece):
        self.squares[row][col].piece = piece
        self.last_click = self.squares[row][col]
        
    def valid_add(self, row, col):
        return self.squares[row][col].is_empty() and 0 <= row < ROWS and 0 <= col < COLS
    
    def is_full(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].is_empty():
                    return False
        return True
    
    def is_there_a_winner(self):
        winning_positions = [
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            [(0, 0), (1, 0), (2, 0)],  # First column
            [(0, 1), (1, 1), (2, 1)],  # Second column
            [(0, 2), (1, 2), (2, 2)],  # Third column
            [(0, 0), (1, 1), (2, 2)],  # Right diagonal
            [(0, 2), (1, 1), (2, 0)],  # Left diagonal
        ]

        for positions in winning_positions:
            if self._check_line(*positions):
                self.winner = self.squares[positions[0][0]][positions[0][1]].piece.name
                self.win_line = positions
                return True
        return False
    
    def is_the_board_filled(self):
        if self.is_full() and not self.is_there_a_winner():
            return True
        return False
    
    def game_over(self):
        if self.is_there_a_winner():
            return f'{self.winner.upper()} win'
        elif self.is_the_board_filled():
            return 'Draw'
        return 'NotOver'