import sys, pygame

from const import *
from game import Game
from square import Square
from piece import *
from popup import Popup

class Main:
    
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tic Tac Toe')
        self.game = Game()
        # self.popup = Popup(self.surface)
        
    def mainloop(self):
        
        surface = self.surface
        game = self.game
        board = game.board
        ai = game.ai
        
        while True:
            
            game.show_bg(surface)
            game.show_pieces(surface)
            
            game.show_hover(surface)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    pos = event.pos
                    clicked_row = pos[1] // SQSIZE
                    clicked_col = pos[0] // SQSIZE
                    
                    if board.squares[clicked_row][clicked_col].is_empty():
                        if game.game_mode == 'ai':
                            board.add_piece(clicked_row, clicked_col, X())
                            game.sound_effect()
                            game.next_turn()
                            if board.is_the_board_filled():
                                board.winner = 'Draw'
                            else:
                                ai_move = ai.pickSpot(board)
                                board.add_piece(ai_move[0], ai_move[1], O())
                                game.sound_effect()
                                game.next_turn()
                                if board.is_the_board_filled():
                                    board.winner = 'Draw'
                        else:
                            if game.turn == 'X':
                                board.add_piece(clicked_row, clicked_col, X())
                                game.sound_effect()
                                game.next_turn()
                                if board.is_the_board_filled():
                                    board.winner = 'Draw'
                            else:
                                board.add_piece(clicked_row, clicked_col, O())
                                game.sound_effect()
                                game.next_turn()
                                if board.is_the_board_filled():
                                    board.winner = 'Draw'
                        if board.is_there_a_winner():
                            game.show_bg(surface)
                            game.show_pieces(surface)
                            game.show_win_line(surface)
                            waiting = True
                            while waiting:
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or event.type == pygame.QUIT:
                                        waiting = False
                                        break

                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    motion_row = pos[1] // SQSIZE
                    motion_col = pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)
                    
                    game.show_bg(surface)
                    game.show_pieces(surface)
                    
                    game.show_hover(surface)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        surface = self.surface
                        game = self.game
                        board = game.board
                        ai = game.ai
                        # popup = self.popup
                    elif event.key == pygame.K_t:
                        game.change_theme()
                    elif event.key == pygame.K_m:
                        game.change_game_mode()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
            
if __name__ == '__main__':
    Main().mainloop()