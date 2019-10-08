import pygame
import random
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play", 0)
    hi_score_button = Button(ai_settings, screen, "Hi Scores", 1)
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    aliens1 = Group()
    aliens2 = Group()
    aliens3 = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)

    # Play Menu Music
    pygame.mixer.music.load('sounds/background/menu.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, hi_score_button, ship, aliens, aliens1, aliens2, aliens3, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, play_button, hi_score_button)


run_game()
