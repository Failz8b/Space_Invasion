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
        self.white = (255, 255, 255)
        self.green = (0, 200, 0)
        self.title_color = (255, 255, 255)
        # Scale Down Factor to make the game run smoother"
        self.sdf = 2

        # Ship settings.
        self.ship_limit = 3
            
        # Bullet settings.
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
        self.shoot_delay = 75 / self.sdf
        self.abullet_timer = 0
        self.abullet_wait = 20 / self.sdf

        # HOLD buttons
        self.hold_space = False
        self.hold_l = False

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
        self.title_font = pygame.font.SysFont(None, 160)
        self.hs_font = pygame.font.SysFont(None, 125)
        self.font_point = pygame.font.SysFont(None, 64)

        # Collision Points
        c_x = 0
        c_y = 0

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 2 * self.sdf
        self.bullet_speed_factor = 3 * self.sdf
        self.abullet_speed_factor = 1 * self.sdf
        self.alien_speed_factor = 1 * self.sdf
        self.abullets_allowed = 5
        self.abullet_frequency = 10
        
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
        self.abullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        if self.abullets_allowed < 9:
            self.abullets_allowed += 1
        if self.abullet_frequency < 20:
            self.abullet_frequency +=1
        
        self.alien_points = int(self.alien_points * self.score_scale)
