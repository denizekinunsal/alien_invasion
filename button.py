import pygame.font
class Button:
    """A class to build buttons for the game."""
    # def __init__(self, ai_game, msg):
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.image = pygame.image.load('images/play.bmp')
        # Build the button's rect object and center it.
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        # The button message needs to be prepped only once.
        

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.blit(self.image, self.rect)