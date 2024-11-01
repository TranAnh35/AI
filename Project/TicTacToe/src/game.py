import pygame

from ai import AI
from board import Board
from const import *
from config import Config

class Game:
    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.config = Config()
        self.turn = 'X'
        self.game_mode = 'ai'
        self.hovered_square = None
        
    # -------------
    # Draw methods
    # -------------
    
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg_light.color if (row + col) % 2 == 0 else theme.bg_dark.color
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
            
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    piece.set_texture()
                    texture = piece.texture
                    img = pygame.image.load(texture)
                    img = pygame.transform.scale(img, (100, 100))
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)
                        
    def show_win_line(self, surface):
        theme = self.config.theme
        for row, col in self.board.win_line:
            color = theme.trace.color
            rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, 10)
            
    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, 3)
            
    # -------------
    # Other methods
    # -------------
    
    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self):
        self.config.click_sound.play()
        
    def next_turn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'
        
    def change_game_mode(self):
        self.game_mode = 'ai' if self.game_mode == 'pvp' else 'pvp'
        
    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]
        
    def reset(self):
        self.__init__()