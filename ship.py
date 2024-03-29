import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen, frame):
        """Initialize the ship, and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.frame = frame

        # Destroyed Timers
        self.des_timer = 0
        self.anim_delay = 30 / self.ai_settings.sdf
        self.in_anim = False

        # Load the ship image, and get its rect.
        self.img = {0: 'images/Ship/ship.png',
                    1: 'images/ship/D1.png',
                    2: 'images/ship/D2.png',
                    3: 'images/ship/D3.png',
                    4: 'images/ship/D4.png',
                    5: 'images/ship/D5.png',
                    6: 'images/ship/D6.png',
                    7: 'images/ship/D7.png',
                    8: 'images/ship/D8.png',
                    9: 'images/ship/D9.png'}

        if self.frame == 0:
            self.image = pygame.image.load(self.img[self.frame])

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        # Ship sounds
        self.sound_fire = pygame.mixer.Sound('sounds/ship/shoot.wav')
        self.sound_fire.set_volume(.5)
        self.des_sound = pygame.mixer.Sound('sounds/ship/destroy.wav')

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.frame == 0:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        if self.frame == 0:
            self.image = pygame.image.load(self.img[0])

        if self.in_anim:
            if self.des_timer >= self.anim_delay:
                self.image = pygame.image.load(self.img[self.frame])
                self.frame += 1
                self.des_timer = 0
                if self.frame == 10:
                    self.frame = 0
                    self.in_anim = False

        self.screen.blit(self.image, self.rect)
