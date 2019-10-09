import random
import pygame


class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (0, 0, 0)
        self.hs_color = (100, 100, 100)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        
        # Ship settings.
        self.ship_limit = 3
            
        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 50
        self.bullets_allowed = 3

        # Alien settings.
        self.fleet_drop_speed = 10
            
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

        # Variable to determine if the fleet just changed directions
        self.recently_cd = False

        # Timer to disallow bullet spam
        self.shoot_timer = 0
        self.shoot_delay = 50

        # HOLD buttons
        self.hold_space = False

        # Random UFO
        self.spawn_ufo = False
        self.ufo_timer = 0
        self.ufo_display = 0
        self.ufo_rand = random.randint(500, 10000)
        self.ufo_point = 0
        self.ufo_destroyed = False
        self.ufo_pos = (0, 0)

        # Hi Score Screen
        self.hs_screen = False

        # Music
        self.music_faster = False
        self.music_pos = 0
        self.alien_number = 0

        # Font
        self.font = pygame.font.SysFont(None, 48)
        self.title_font = pygame.font.SysFont(None, 128)
        self.font_point = pygame.font.SysFont(None, 60)

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        # Scoring.
        self.alien_points = 50
        self.t0_scale = 1.5
        self.t1_scale = 1.25
        self.t2_scale = 1
        self.points_a1 = int(round(self.alien_points * self.t0_scale, -1))
        self.points_a2 = int(round(self.alien_points * self.t1_scale, -1))
        self.points_a3 = int(round(self.alien_points * self.t2_scale, -1))
    
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
