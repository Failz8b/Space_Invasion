import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    """A class to make a single bunker."""

    def __init__(self, ai_settings, screen):
        """Initialize the bunker, and set its starting position."""
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/bunker/b1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Bunker Sounds
        self.destroyed_sound = pygame.mixer.Sound('sounds/bunker/destroyed.wav')

    def blitme(self):
        """Draw the bunker at its current state."""
        self.screen.blit(self.image, self.rect)
