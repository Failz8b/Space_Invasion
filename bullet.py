import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship, btype):
        """Create a bullet object, at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        self.btype = btype

        # Create bullet rect at (0, 0), then set correct position.
        if btype == 0:
            # self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.image = pygame.image.load('images/bullet/B1.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            # self.rect = pygame.Rect(0, 0, ai_settings.abullet_width, ai_settings.abullet_height)
            self.image = pygame.image.load('images/bullet/B2.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)

        # Bullet differences
        if btype == 0:
            self.speed_factor = ai_settings.bullet_speed_factor
        else:
            self.speed_factor = ai_settings.abullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        if self.btype == 0:
            # Update the decimal position of the bullet.
            self.y -= self.speed_factor
        else:
            self.y += self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
