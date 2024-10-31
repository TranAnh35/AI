import pygame

class Popup:
    def __init__(self, screen, winner=None, font_name="Comic Sans MS", font_size=36):
        self.screen = screen
        self.winner = winner
        self.font = pygame.font.SysFont(font_name, font_size)
        self.width = 300
        self.height = 150
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)

    def draw(self):
        # Center popup on the screen
        screen_rect = self.screen.get_rect()
        popup_rect = pygame.Rect(0, 0, self.width, self.height)
        popup_rect.center = screen_rect.center

        # Draw the popup background
        pygame.draw.rect(self.screen, self.bg_color, popup_rect)

        # Draw the winning text
        text = f"{self.winner} wins!"
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=popup_rect.center)
        self.screen.blit(text_surface, text_rect)

        # Update display
        pygame.display.flip()

    def wait_for_close(self):
        # Wait until the user closes the popup or presses a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
                    break
                
    def set_winner(self, winner):
        self.winner = winner