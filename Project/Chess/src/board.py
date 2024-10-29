from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import copy
import os

class Board:
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final
        
        en_passant_empty = self.squares[initial.row][final.col].is_empty()
        
        # Cập nhật nước đi cho bàn cờ
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        if isinstance(piece, Pawn):
            # Bắt quân cờ qua đường
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # Cập nhật nước đi cho bàn cờ
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(
                        os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            
            # Thăng cấp        
            else:
                self.check_promotion(piece, final)
                
        # Nhập thành
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moved[-1])
                
        # Quân cờ đã di chuyển
        piece.moved = True
        
        # Xóa các nước đi của tất cả các quân cờ
        piece.clear_moves()
        
        # Đăt nước đi cuối cùng
        self.last_move = move
                
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
            
    def castling(self, initial, final):
        return abs(final.col - initial.col) == 2
    
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
                    
        piece.en_passant = True
        
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
                        
        return False
    
    def calc_moves(self, piece, row, col, bool=True):
        '''
            Tính toán tất cả các nước đi có thể (hợp lệ) của một quân cờ cụ thể ở một vị trí cụ thể
        '''
        
        def pawn_moves():
            # Di chuyển cơ bản
            steps = 1 if piece.moved else 2
            
            # Di chuyển theo chiều dọc
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # tạo ra các ô di chuyển đầu tiên và cuối cùng
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Tạo ra một nước đi mới
                        move = Move(initial, final)
                        
                        # Kiểm tra các nước chiếu tiềm năng
                        if bool:
                            if not self.in_check(piece, move):
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                        else:
                            # Thêm nước đi vào danh sách nước đi của quân cờ
                            piece.add_move(move)
                    # Quân cờ bị chặn
                    else:
                        break
                # Không nằm trong bàn cờ
                else:
                    break
            
            # Di chuyển theo đường chéo
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # Tạo ra các ô di chuyển đầu tiên và cuối cùng
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Tạo ra một nước đi mới
                        move = Move(initial, final)
                        
                        # Kiểm tra các nước chiếu tiềm năng
                        if bool:
                            if not self.in_check(piece, move):
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                        else:
                            # Thêm nước đi vào danh sách nước đi của quân cờ
                            piece.add_move(move)

            # Nước bắt tốt chéo
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # Bắt tốt chéo trái
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # Tạo ô initial và final của nước đi
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # Tạo 1 nước đi mới
                            move = Move(initial, final)
                            
                            # Kiểm tra các nước chiếu tiềm năng
                            if bool:
                                if not self.in_check(piece, move):
                                    # Thêm nước đi vào danh sách nước đi của quân cờ
                                    piece.add_move(move)
                            else:
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                                
            # Bắt tốt chéo phải
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # Tạo ô initial và final của nước đi
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # Tạo 1 nước đi mới
                            move = Move(initial, final)
                            
                            # Kiểm tra các nước chiếu tiềm năng
                            if bool:
                                if not self.in_check(piece, move):
                                    # Thêm nước đi vào danh sách nước đi của quân cờ
                                    piece.add_move(move)
                            else:
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                                
        def knight_moves():
            # 8 ô di chuyển có thể của mã
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # Tạo ra các ô vuông của nước đi mới
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Tạo ra một nước đi mới
                        move = Move(initial, final)
                        
                        # Kiểm tra các nước chiếu tiềm năng
                        if bool:
                            if not self.in_check(piece, move):
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                            else: break
                        else:
                            # Thêm nước đi vào danh sách nước đi của quân cờ
                            piece.add_move(move)
                            
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Tạo ra các ô vuông của nước đi mới có thể
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Tạo một nước đi mới có thể thực hiện
                        move = Move(initial, final)

                        # Nếu rỗng thì tiếp tục lặp lại
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # Kiểm tra các nước chiếu tiềm năng
                            if bool:
                                if not self.in_check(piece, move):
                                    # Thêm nước đi vào danh sách nước đi của quân cờ
                                    piece.add_move(move)
                            else:
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)

                        # Nếu có quân địch thì bắt quân địch và kết thúc vòng lặp
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # Kiểm tra các nước chiếu tiềm năng
                            if bool:
                                if not self.in_check(piece, move):
                                    # Thêm nước đi vào danh sách nước đi của quân cờ
                                    piece.add_move(move)
                            else:
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                            break

                        # Nếu có quân đồng minh thì kết thúc vòng lặp
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # Nếu không nằm trong bàn cờ thì kết thúc vòng lặp
                    else: break

                    # Tăng cột và hàng
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # Lên
                (row-1, col+1), # Chéo phải lên
                (row+0, col+1), # Phải
                (row+1, col+1), # Chéo phải xuống
                (row+1, col+0), # Xuống
                (row+1, col-1), # Chéo trái xuống
                (row+0, col-1), # Trái
                (row-1, col-1), # Chéo trái lên
            ]

            # Duyệt qua các ô xung quanh
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # Tạo ra các ô vuông của nước đi mới
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # Tạo ra một nước đi mới
                        move = Move(initial, final)
                        # Kiểm tra các nước chiếu tiềm năng
                        if bool:
                            if not self.in_check(piece, move):
                                # Thêm nước đi vào danh sách nước đi của quân cờ
                                piece.add_move(move)
                            else: break
                        else:
                            # Thêm nước đi vào danh sách nước đi của quân cờ
                            piece.add_move(move)

            # Nhập thành
            if not piece.moved:
                # Nhập thành cánh hậu
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # Không thể nhập thành vì có những quân cờ ở giữa?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # Thêm quân xe trái vào vua
                                piece.left_rook = left_rook

                                # Di chuyển quân xe
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # Di chuyển quân vua
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # Kiểm tra các nước chiếu tiềm năng
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # Thêm nước đi vào danh sách nước đi của quân xe
                                        left_rook.add_move(moveR)
                                        # Thêm nước đi vào danh sách nước đi của quân vua
                                        piece.add_move(moveK)
                                else:
                                    # Thêm nước đi vào danh sách nước đi của quân xe
                                    left_rook.add_move(moveR)
                                    # Thêm nước đi vào danh sách nước đi của quân vua
                                    piece.add_move(moveK)

                # Nhập thành cánh vua
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # Không thể nhập thành vì có những quân cờ ở giữa?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # Thêm quân xe phải vào vua
                                piece.right_rook = right_rook

                                # Di chuyển quân xe
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # Di chuyển quân vua
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # Kiểm tra các nước chiếu tiềm năng
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # Thêm nước đi vào danh sách nước đi của quân xe
                                        right_rook.add_move(moveR)
                                        # Thêm nước đi vào danh sách nước đi của quân vua
                                        piece.add_move(moveK)
                                else:
                                    # Thêm nước đi vào danh sách nước đi của quân xe
                                    right_rook.add_move(moveR)
                                    # Thêm nước đi vào danh sách nước đi của quân vua
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # Chéo phải lên
                (-1, -1), # Chéo trái lên
                (1, 1), # Chéo phải xuống
                (1, -1), # Chéo trái xuống
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0), # Lên
                (0, 1), # Phải
                (1, 0), # Xuống
                (0, -1), # Trái
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), # Chéo phải lên
                (-1, -1), # Chéo trái lên
                (1, 1), # Chéo phải xuống
                (1, -1), # Chéo trái xuống
                (-1, 0), # Lên
                (0, 1), # Phải
                (1, 0), # Xuống
                (0, -1) # Trái
            ])

        elif isinstance(piece, King): 
            king_moves()
            
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Quân tốt
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Quân Mã
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Quân tượng
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Quân xe
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Quân hậu
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # Quân vua
        self.squares[row_other][4] = Square(row_other, 4, King(color))