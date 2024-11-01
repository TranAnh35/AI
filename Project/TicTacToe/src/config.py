import os, pygame

from sound import Sound
from theme import Theme

class Config:
    
    def __init__(self):
        self._add_theme()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.click_sound = Sound(os.path.join('assets/sounds/click.wav'))
    
    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]
        
    # -------------
    # Init methods
    # -------------
    
    def _add_theme(self):
        
        green = Theme('0x80bdab', '0x2ad6a3', (244, 247, 116))
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100))
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227))
        gray = Theme((120, 119, 118), (86, 85, 84), (200, 200, 200))
        
        self.themes = [
            green,
            brown,
            blue,
            gray,
        ]