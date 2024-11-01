from const import *

class Square:
    
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        
    def __str__(self):
        return f'({self.row}, {self.col})'
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    # -------------
    # Other methods
    # -------------
    
    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return self.piece == None
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg >= ROWS:
                return False
        return True