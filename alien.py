import pygame
import random
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, alien_type, frame):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_type = alien_type
        self.anim_timer = 0
        self.anim_frame = 1
        self.frame = frame
        self.des_timer = 0
        self.anim_delay = 0

        # Image Dictionaries
        self.img1 = {0: 'images/A0/S1.png',
                     1: 'images/A1/S1.png',
                     2: 'images/A2/S1.png',
                     3: 'images/A3/S1.png'}

        self.img2 = {0: 'images/A0/S2.png',
                     1: 'images/A1/S2.png',
                     2: 'images/A2/S2.png'}

        self.ufo_anim = {0: 'images/A3/S2.png',
                         1: 'images/A3/S3.png',
                         2: 'images/A3/S4.png'}

        self.img3 = {0: 'images/A_Destroyed/D1.png',
                     1: 'images/A_Destroyed/D2.png',
                     2: 'images/A_Destroyed/D3.png'}

        # Load the alien image, and set its rect attribute.
        if self.frame == 1:
            self.image = pygame.image.load(self.img1[self.alien_type])
            self.anim_frame = 1
        else:
            self.image = pygame.image.load(self.img2[self.alien_type])
            self.anim_frame = 2
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        # UFO Sounds
        self.ufo_sound = pygame.mixer.Sound('sounds/ufo/UFO.wav')
        self.ufo_des_sound = pygame.mixer.Sound('sounds/ufo/destroyed.wav')
        self.ufo_sound_playing = False

        # Destroyed Sound
        self.des_sound = pygame.mixer.Sound('sounds/alien/destroyed.wav')

        # Shoot Sound
        self.alien_shoot = pygame.mixer.Sound('sounds/alien/shoot.wav')
        self.alien_shoot.set_volume(.5)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left. Change image if needed"""
        if self.alien_type == 3:
            if self.ai_settings.spawn_ufo:
                self.x += random.randint(25, 101) * self.ai_settings.ship_speed_factor / 100
            else:
                self.x = self.x
        else:
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        self.anim_delay = 75
        self.anim_timer += 1
        if self.anim_timer >= self.anim_delay:
            if self.anim_frame == 1:
                if self.alien_type == 3:
                    self.image = pygame.image.load(self.ufo_anim[0])
                else:
                    self.image = pygame.image.load(self.img2[self.alien_type])
                self.anim_timer = 0
                self.anim_frame = 2
            elif self.anim_frame == 2:
                if self.alien_type == 3:
                    self.image = pygame.image.load(self.ufo_anim[1])
                    self.anim_frame = 8
                else:
                    self.image = pygame.image.load(self.img1[self.alien_type])
                    self.anim_frame = 1
                self.anim_timer = 0
            elif self.anim_frame == 8:
                self.image = pygame.image.load(self.ufo_anim[2])
                self.anim_timer = 0
                self.anim_frame = 9
            elif self.anim_frame == 9:
                self.image = pygame.image.load(self.img1[3])
                self.anim_timer = 0
                self.anim_frame = 1

        des_delay = 25
        self.des_timer += 1
        if self.anim_frame == 3:
            self.des_sound.play()
            self.image = pygame.image.load(self.img3[0])
            self.anim_frame = 4
            self.des_timer = 0
        elif self.anim_frame == 4 and self.des_timer >= des_delay:
            self.image = pygame.image.load(self.img3[1])
            self.anim_frame = 5
            self.des_timer = 0
        elif self.anim_frame == 5 and self.des_timer >= des_delay:
            self.image = pygame.image.load(self.img3[2])
            self.anim_frame = 6
            self.des_timer = 0
        elif self.anim_frame == 6 and self.des_timer >= des_delay:
            self.kill()
            self.des_timer = 0

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
