import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, alien_type):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_type = alien_type
        self.anim_timer = 0
        self.anim_frame = 1

        # Image Dictionaries
        self.img1 = {0: 'images/A0/S1.png',
                    1: 'images/A1/S1.png',
                    2: 'images/A2/S1.png',
                    3: 'images/A3/S1.png'}

        self.img2 = {0: 'images/A0/S2.png',
                     1: 'images/A1/S2.png',
                     2: 'images/A2/S2.png'}

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load(self.img1[self.alien_type])
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left. Change image if needed"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        anim_delay = 75
        self.anim_timer += 1
        if self.anim_timer >= anim_delay and (self.alien_type == 0 or self.alien_type == 1 or self.alien_type == 2):
            if self.anim_frame == 1:
                self.image = pygame.image.load(self.img2[self.alien_type])
                self.anim_timer = 0
                self.anim_frame = 2
            elif self.anim_frame == 2:
                self.image = pygame.image.load(self.img1[self.alien_type])
                self.anim_timer = 0
                self.anim_frame = 1

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
