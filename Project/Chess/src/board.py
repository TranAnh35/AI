from const import *
from piece import *
from move import Move
from square import Square

class Board:

    def __init__(self):
        self.squares = []
        self.move_history = []
        self.max_history = 10
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def __str__(self):
        s = '\n'
        for row in range(ROWS):
            s += '[ '
            for col in range(COLS):
                sqr = self.squares[row][col]
                s += '[ ]' if sqr.isempty() else str(sqr.piece)
                s += ' '
            s += ']\n'
        return s

    # ------------
    # MOVE METHODS
    # ------------

    def move(self, piece, move):
        self.save_state()
        
        initial = move.initial
        final = move.final
        # console squares update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # castling ?
        if piece.name == 'king':
            row = 0 if piece.color == 'black' else 7 
            diff = initial.col - final.col
            if diff == 2:
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    # erase king prev moves
                    piece.moved = True
                    piece.moves = []
                    # move left rook
                    piece2 = self.squares[row][0].piece
                    initial = Square(row, 0)
                    final = Square(row, 3)
                    move2 = Move(initial, final)
                    self.move(piece2, move2)
            elif diff == -2:
                # erase king prev moves
                piece.moved = True
                piece.moves = []
                # move right rook
                piece2 = self.squares[row][7].piece
                initial = Square(row, 7)
                final = Square(row, 5)
                move2 = Move(initial, final)
                self.move(piece2, move2)

        # promoting ?
        if piece.name == 'pawn':
            self.check_promotion(piece, final)

        piece.moved = True
        piece.moves = []

        self.last_move = move

    def check_promotion(self, piece, final):
        promote_row = 0 if piece.color == 'white' else 7

        if final.row == promote_row:
            # promote
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def valid_move(self, piece, move):
        return move in piece.moves

    def generate_moves(self, piece, row, col):

        def pawn():
            piece = self.squares[row][col].piece
            if piece.color == 'black':
                if row != 1: piece.moved = True
            if piece.color == 'white':
                if row != 6: piece.moved = True
            # steps
            steps = 1 if piece.moved else 2

            # vertical move
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, col, self.squares[move_row][col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            # diagonal
            move_cols = [col - 1, col + 1]
            move_row = row + piece.dir
            for move_col in move_cols:
                if Square.in_range(move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def knight():
            # possible moves
            possible_moves = [
            (row - 2, col + 1),
            (row - 1, col + 2),
            (row + 1, col + 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row + 1, col - 2),
            (row - 1, col - 2),
            (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline(incrs):
            for incr in incrs:
                row_inc, col_inc = incr
                move_row = row + row_inc
                move_col = col + col_inc
                while True:
                    if Square.in_range(move_row, move_col):
                        # move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        # empty
                        if self.squares[move_row][move_col].isempty():
                            # new move
                            piece.add_move(move)
                        # piece
                        else: 
                            if self.squares[move_row][move_col].has_rival_piece(piece.color):
                                # new move and stop
                                piece.add_move(move)
                            break
                    else: # not in range
                        break
                
                    # incr
                    move_row, move_col = move_row + row_inc, move_col + col_inc

        def king():
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]

            # normal moves
            for adj in adjs:
                move_row, move_col = adj
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                
            # castling
            if not piece.moved:
                # queenside castling
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    if not lRook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): break
                            if c == 3:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                # kingside castling
                rRook = self.squares[row][7].piece
                if isinstance(rRook, Rook):
                    if not rRook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): break
                            if c == 6:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

        if piece.name == 'pawn': 
            pawn()

        elif piece.name == 'knight': 
            knight()

        elif piece.name == 'bishop': 
            straightline([(-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'rook': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif piece.name == 'queen': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'king': 
            king()

    def save_state(self):
        state = [[self.squares[row][col].piece for col in range(COLS)] for row in range(ROWS)], self.last_move
        self.move_history.append(state)

        if len(self.move_history) > self.max_history:
            self.move_history.pop(0)
  
    def rollback(self):
        if self.move_history:
            state, last_move = self.move_history.pop()
            self.last_move = last_move
            for row in range(ROWS):
                for col in range(COLS):
                    self.squares[row][col].piece = state[row][col]
              
    def is_king_in_check(self, color):
        king_position = None
        # Find the king's position
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.name == 'king' and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            return False  # No king found, avoid further checks

        king_row, king_col = king_position
        opponent_color = 'black' if color == 'white' else 'white'

        # Directional checks for threats from rooks, queens, and bishops
        directions = {
            "rook": [(1, 0), (0, 1), (-1, 0), (0, -1)],  # vertical and horizontal
            "bishop": [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # diagonal
            "queen": [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],  # both
        }

        # Check rook and queen threats along vertical/horizontal lines
        for direction in directions["rook"]:
            for step in range(1, max(ROWS, COLS)):
                row = king_row + direction[0] * step
                col = king_col + direction[1] * step
                if not Square.in_range(row, col):
                    break
                square_piece = self.squares[row][col].piece
                if square_piece:
                    if square_piece.color == opponent_color and square_piece.name == 'rook':
                        return True  # Rook or queen putting the king in check
                    break

        # Check bishop and queen threats along diagonal lines
        for direction in directions["bishop"]:
            for step in range(1, max(ROWS, COLS)):
                row = king_row + direction[0] * step
                col = king_col + direction[1] * step
                if not Square.in_range(row, col):
                    break
                square_piece = self.squares[row][col].piece
                if square_piece:
                    if square_piece.color == opponent_color and square_piece.name == 'bishop':
                        return True  # Bishop or queen putting the king in check
                    break
                
        for direction in directions["queen"]:
            for step in range(1, max(ROWS, COLS)):
                row = king_row + direction[0] * step
                col = king_col + direction[1] * step
                if not Square.in_range(row, col):
                    break
                square_piece = self.squares[row][col].piece
                if square_piece:
                    if square_piece.color == opponent_color and square_piece.name == 'queen':
                        return True  # Bishop or queen putting the king in check
                    break

        # Check knight threats
        knight_moves = [
            (king_row - 2, king_col + 1), (king_row - 1, king_col + 2),
            (king_row + 1, king_col + 2), (king_row + 2, king_col + 1),
            (king_row + 2, king_col - 1), (king_row + 1, king_col - 2),
            (king_row - 1, king_col - 2), (king_row - 2, king_col - 1),
        ]
        for move in knight_moves:
            row, col = move
            if Square.in_range(row, col):
                square_piece = self.squares[row][col].piece
                if square_piece and square_piece.color == opponent_color and square_piece.name == 'knight':
                    return True  # Knight putting the king in check

        # Check pawn threats
        pawn_row = king_row + (1 if color == 'white' else -1)
        for pawn_col in [king_col - 1, king_col + 1]:
            if Square.in_range(pawn_row, pawn_col):
                square_piece = self.squares[pawn_row][pawn_col].piece
                if square_piece and square_piece.color == opponent_color and square_piece.name == 'pawn':
                    return True  # Pawn putting the king in check

        return False  # No threats detected; king is not in check
    
    def calc_moves(self, piece, row, col):
        # Calculate all possible moves for the piece
        self.generate_moves(piece, row, col)

        # If the current player's king is in check, we need to validate each move
        if self.is_king_in_check(piece.color):
            original_moves = piece.moves.copy()
            valid_moves = []

            for move in original_moves:
                # Simulate the move
                initial_piece = self.squares[move.initial.row][move.initial.col].piece
                captured_piece = self.squares[move.final.row][move.final.col].piece
                self.squares[move.initial.row][move.initial.col].piece = None
                self.squares[move.final.row][move.final.col].piece = initial_piece

                # Check if the move resolves the check
                if not self.is_king_in_check(piece.color):
                    valid_moves.append(move)

                # Undo the move
                self.squares[move.final.row][move.final.col].piece = captured_piece
                self.squares[move.initial.row][move.initial.col].piece = initial_piece

            # Set the valid moves only
            piece.moves = valid_moves

    def remove_all_moves(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.moves:
                    piece.remove_moves()
                    
    def get_king_pos(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.name == 'king' and piece.color == color:
                    return self.squares[row][col]  
                
    def is_game_over(self):
        white_king_pos = self.get_king_pos('white')
        black_king_pos = self.get_king_pos('black')
        
        if white_king_pos is not None and black_king_pos is not None:
            return False
        return True
    
    def winner(self):
        white_king_pos = self.get_king_pos('white')
        black_king_pos = self.get_king_pos('black')
        
        if white_king_pos is not None and black_king_pos is None:
            return 'white'
        if black_king_pos is not None and white_king_pos is None:
            return 'black'
        return None
       
    # ------------
    # INIT METHODS
    # ------------

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # KNIGHTS
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # BISHOPS
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # ROOKS
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # QUEEN
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # KING
        self.squares[row_other][4] = Square(row_other, 4, King(color))