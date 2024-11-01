import pygame

class Popup:
    def __init__(self, surface, winner=None, font_name="Comic Sans MS", font_size=36):
        self.surface = surface
        self.winner = winner
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = self.font.render(self.winner, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(250, 250))