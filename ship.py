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
        self.anim_delay = 20
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
                    8: 'images/ship/D8.png'}

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
        self.sound_fire.set_volume(.2)
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
        elif self.frame == 1:
            self.image = pygame.image.load(self.img[1])
            self.frame = 2
            self.des_timer = 0
        elif self.frame == 2 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[2])
            self.frame = 3
            self.des_timer = 0
        elif self.frame == 3 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[3])
            self.frame = 4
            self.des_timer = 0
        elif self.frame == 4 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[4])
            self.frame = 5
            self.des_timer = 0
        elif self.frame == 5 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[5])
            self.frame = 6
            self.des_timer = 0
        elif self.frame == 6 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[6])
            self.frame = 7
            self.des_timer = 0
        elif self.frame == 7 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[7])
            self.frame = 8
            self.des_timer = 0
        elif self.frame == 8 and self.des_timer >= self.anim_delay:
            self.image = pygame.image.load(self.img[8])
            self.frame = 9
            self.des_timer = 0
        elif self.frame == 9 and self.des_timer >= self.anim_delay * 2:
            self.frame = 0
            self.in_anim = False
            self.des_timer = 0
        self.screen.blit(self.image, self.rect)
