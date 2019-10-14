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
    back_button = Button(ai_settings, screen, "Back", 2)
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen, 0)
    bullets = Group()
    abullets = Group()
    aliens = Group()
    aliens1 = Group()
    aliens2 = Group()
    aliens3 = Group()
    bunkers = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)

    # Create Bunkers
    gf.create_bunker_array(ai_settings, screen, ship, bunkers)

    # Play Menu Music
    pygame.mixer.music.load('sounds/background/menu.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # Set FPS of game
    clock = pygame.time.Clock()

    # Open/Create a HS File
    f = open("hi_scores.txt", "a+")
    f.close()

    # Read from the file (if any)
    with open("hi_scores.txt", "r+") as f:
        for i in range(10):
            read_line = f.readline()
            if read_line.strip():
                sb.hs_list[i] = int(read_line)

    # Start the main loop for the game.
    while True:
        clock.tick(360)
        gf.check_events(ai_settings, screen, stats, sb, play_button, hi_score_button, back_button, ship, aliens,
                        aliens1, aliens2, aliens3, bullets, abullets, bunkers)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets,
                              abullets, bunkers)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                             bunkers)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                         play_button, hi_score_button, back_button, bunkers)


run_game()
