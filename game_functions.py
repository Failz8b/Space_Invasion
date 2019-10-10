import sys
import random
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, ship):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ai_settings.hold_space = True
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship, ai_settings):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        ai_settings.hold_space = False


def check_events(ai_settings, screen, stats, sb, play_button, hi_score_button, back_button, ship, aliens, aliens1,
                 aliens2, aliens3, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, ai_settings)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3,
                              bullets, mouse_x, mouse_y)
            check_hi_score_button(ai_settings, stats, hi_score_button, mouse_x, mouse_y)
            check_back_button(ai_settings, stats, back_button, mouse_x, mouse_y)


def check_hi_score_button(ai_settings, stats, hi_score_button, mouse_x, mouse_y):
    button_clicked = hi_score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not ai_settings.hs_screen:
        ai_settings.hs_screen = True


def check_back_button(ai_settings, stats, back_button, mouse_x, mouse_y):
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and ai_settings.hs_screen:
        ai_settings.hs_screen = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3, bullets,
                      mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        aliens1.empty()
        aliens2.empty()
        aliens3.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)
        ship.center_ship()

        # Play in game music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/background/in_game.mp3')
        pygame.mixer.music.play(-1, 0.0)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed and ai_settings.shoot_timer >= ai_settings.shoot_delay:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ai_settings.shoot_timer = 0
        ship.sound_fire.play()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, play_button,
                  hi_score_button, back_button):
    """Update images on the screen, and flip to the new screen."""
    # Shoot Bullet is Space is held down
    if ai_settings.hold_space:
        fire_bullet(ai_settings, screen, ship, bullets)

    # UFO?
    if stats.game_active:
        ai_settings.ufo_timer += 1
        ai_settings.ufo_display += 1
    else:
        ai_settings.ufo_timer =0
    if ai_settings.ufo_timer >= ai_settings.ufo_rand:
        ai_settings.spawn_ufo = True
        for alien in aliens3:
            alien.ufo_sound.set_volume(.1)
            alien.ufo_sound.play(1)
    for alien in aliens3:
        if alien.x > ai_settings.screen_width + alien.rect.width:
            alien.kill()
            alien.ufo_sound.fadeout(1000)

    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    aliens1.draw(screen)
    aliens2.draw(screen)
    aliens3.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive or HS screen if HS is active.
    if not stats.game_active:
        if ai_settings.hs_screen:
            screen.fill(ai_settings.hs_color)

            # Display High Scores
            score = ai_settings.font.render(str(sb.hs_list[0]), False, ai_settings.white)
            screen.blit(score, (ai_settings.screen_width / 2, 50))

            score1 = ai_settings.font.render(str(sb.hs_list[1]), False, ai_settings.white)
            screen.blit(score1, (ai_settings.screen_width / 2, 100))

            score2 = ai_settings.font.render(str(sb.hs_list[2]), False, ai_settings.white)
            screen.blit(score2, (ai_settings.screen_width / 2, 150))

            score3 = ai_settings.font.render(str(sb.hs_list[3]), False, ai_settings.white)
            screen.blit(score3, (ai_settings.screen_width / 2, 200))

            score4 = ai_settings.font.render(str(sb.hs_list[4]), False, ai_settings.white)
            screen.blit(score4, (ai_settings.screen_width / 2, 250))

            score5 = ai_settings.font.render(str(sb.hs_list[5]), False, ai_settings.white)
            screen.blit(score5, (ai_settings.screen_width / 2, 300))

            score6 = ai_settings.font.render(str(sb.hs_list[6]), False, ai_settings.white)
            screen.blit(score6, (ai_settings.screen_width / 2, 350))

            score7 = ai_settings.font.render(str(sb.hs_list[7]), False, ai_settings.white)
            screen.blit(score7, (ai_settings.screen_width / 2, 400))

            score8 = ai_settings.font.render(str(sb.hs_list[8]), False, ai_settings.white)
            screen.blit(score8, (ai_settings.screen_width / 2, 450))

            score9 = ai_settings.font.render(str(sb.hs_list[9]), False, ai_settings.white)
            screen.blit(score9, (ai_settings.screen_width / 2, 500))

            back_button.draw_button()
        else:
            # Fill bg
            screen.fill(ai_settings.bg_color)

            # Cool Looking Title
            title_shadow = ai_settings.title_font.render("Space Invaders", True, ai_settings.green, ai_settings.bg_color)
            title_rect_s = title_shadow.get_rect()
            screen.blit(title_shadow, ((ai_settings.screen_width / 2) - (title_rect_s.width / 2) + 3, 30))
            title = ai_settings.title_font.render("Space Invaders", False, ai_settings.white)
            title_rect = title.get_rect()
            screen.blit(title, ((ai_settings.screen_width / 2) - (title_rect.width / 2), 25))

            # Point Values
            a1_text = ai_settings.font_point.render((" = " + str(ai_settings.points_a1) + " Points"), True, ai_settings.green, ai_settings.bg_color)
            a2_text = ai_settings.font_point.render((" = " + str(ai_settings.points_a2) + " Points"), True, ai_settings.green, ai_settings.bg_color)
            a3_text = ai_settings.font_point.render((" = " + str(ai_settings.points_a3) + " Points"), True, ai_settings.green, ai_settings.bg_color)
            a4_text = ai_settings.font_point.render(" = ??? Points", True, ai_settings.green, ai_settings.bg_color)

            screen.blit(a1_text, ((ai_settings.screen_width / 2) - 90, 210))
            screen.blit(a2_text, ((ai_settings.screen_width / 2) - 90, 290))
            screen.blit(a3_text, ((ai_settings.screen_width / 2) - 90, 370))
            screen.blit(a4_text, ((ai_settings.screen_width / 2) - 90, 450))

            # Draw Aliens
            a1 = Alien(ai_settings, screen, 0, 1)
            a2 = Alien(ai_settings, screen, 1, 1)
            a3 = Alien(ai_settings, screen, 2, 1)
            a4 = Alien(ai_settings, screen, 3, 1)

            a1.rect.x = (ai_settings.screen_width / 2) - 160
            a2.rect.x = (ai_settings.screen_width / 2) - 160
            a3.rect.x = (ai_settings.screen_width / 2) - 160
            a4.rect.x = (ai_settings.screen_width / 2) - 160

            a1.rect.y = 200
            a2.rect.y = 280
            a3.rect.y = 360
            a4.rect.y = 440

            a1.blitme()
            a2.blitme()
            a3.blitme()
            a4.blitme()

            hi_score_button.draw_button()

        stats.game_active = False
        play_button.draw_button()

    ai_settings.alien_number = len(aliens) + len(aliens1) + len(aliens2)

    if ai_settings.alien_number <= 9 and not ai_settings.music_faster:
        ai_settings.music_pos += pygame.mixer.music.get_pos()
        music_time = ai_settings.music_pos / 1150
        pygame.mixer.music.load('sounds/background/in_game_faster.mp3')
        pygame.mixer.music.play(-1, music_time)
        ai_settings.music_faster = True

    if ai_settings.ufo_destroyed and ai_settings.ufo_display <= 180:
        ufo_text = ai_settings.font.render(str(ai_settings.ufo_point), True, ai_settings.white, ai_settings.bg_color)
        screen.blit(ufo_text, ai_settings.ufo_pos)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

    # Update Timer Variables
    ai_settings.shoot_timer += 1


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

'''
    for j in range(10):
        if stats.high_score > sb.hs_list[j]:
            stats.high_score = stats.score
            for i in range(9 - j):
                sb.hs_list[9 - i] = sb.hs_list[9 - i - 1]
            sb.hs_list[0] = stats.score
'''


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    collisions1 = pygame.sprite.groupcollide(bullets, aliens1, True, False)
    collisions2 = pygame.sprite.groupcollide(bullets, aliens2, True, False)
    collisions3 = pygame.sprite.groupcollide(bullets, aliens3, True, True)

    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a1 = ai_settings.alien_points * len(aliens) * ai_settings.t0_scale
                    stats.score += ai_settings.points_a1
                    sb.prep_score()
        check_high_score(stats, sb)

    if collisions1:
        for aliens1 in collisions1.values():
            for alien in aliens1:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a2 = ai_settings.alien_points * len(aliens1) * ai_settings.t1_scale
                    stats.score += ai_settings.points_a2
                    sb.prep_score()
        check_high_score(stats, sb)

    if collisions2:
        for aliens2 in collisions2.values():
            for alien in aliens2:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a3 = ai_settings.alien_points * len(aliens2) * ai_settings.t2_scale
                    stats.score += ai_settings.points_a3
                    sb.prep_score()
        check_high_score(stats, sb)

    if collisions3:
        for aliens3 in collisions3.values():
            ai_settings.ufo_point = int(round(ai_settings.alien_points * len(aliens3) * random.randint(2, 10), -1))
            stats.score += ai_settings.ufo_point
            sb.prep_score()
            ai_settings.ufo_destroyed = True
            ai_settings.ufo_display = 0
            for alien in aliens3:
                ai_settings.ufo_pos = (alien.rect.x + (alien.rect.width/2), alien.rect.y + (alien.rect.height/2))
                alien.ufo_sound.stop()
                alien.ufo_des_sound.play()
        check_high_score(stats, sb)

    if len(aliens) == 0 and len(aliens1) == 0 and len(aliens2) == 0 and \
            (len(aliens3) == 0 or not ai_settings.spawn_ufo):
        # If the entire fleet is destroyed, start a new level.
        aliens3.empty()
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)

        # Set New UFO timers
        ai_settings.ufo_timer = 0
        ai_settings.ufo_rand = random.randint(500, 10000)
        ai_settings.spawn_ufo = False
        ai_settings.ufo_destroyed = False

        # Go back to slow music
        ai_settings.music_pos += pygame.mixer.music.get_pos()
        music_time = ai_settings.music_pos / 870
        pygame.mixer.music.load('sounds/background/in_game.mp3')
        pygame.mixer.music.play(-1, music_time)
        ai_settings.music_faster = False


def check_fleet_edges(ai_settings, aliens, aliens1, aliens2):
    """Respond appropriately if any aliens have reached an edge."""
    ai_settings.recently_cd = False
    for alien in aliens.sprites():
        if alien.check_edges() and not ai_settings.recently_cd:
            change_fleet_direction(ai_settings, aliens, aliens1, aliens2)
            break
    for alien in aliens1.sprites():
        if alien.check_edges() and not ai_settings.recently_cd:
            change_fleet_direction(ai_settings, aliens, aliens1, aliens2)
            break
    for alien in aliens2.sprites():
        if alien.check_edges() and not ai_settings.recently_cd:
            change_fleet_direction(ai_settings, aliens, aliens1, aliens2)
            break


def change_fleet_direction(ai_settings, aliens, aliens1, aliens2):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    for alien in aliens1.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    for alien in aliens2.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1
    ai_settings.recently_cd = True


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Respond to ship being hit by alien."""
    ship.des_sound.play()
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

        # Play Menu Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/background/menu.mp3')
        pygame.mixer.music.play(-1, 0.0)

    # Empty the list of aliens and bullets.
    aliens.empty()
    aliens1.empty()
    aliens2.empty()
    aliens3.empty()
    for alien in aliens3:
        alien.kill()
    bullets.empty()

    ship.frame = 1
    ship.in_anim = True
    while ship.in_anim:
        ship.des_timer += 1
        screen.fill(ai_settings.bg_color)
        sb.show_score()
        ship.blitme()
        pygame.display.flip()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            break
    for alien in aliens1.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            break
    for alien in aliens2.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """
    Check if the fleet is at an edge, then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens, aliens1, aliens2)
    aliens.update()
    aliens1.update()
    aliens2.update()
    aliens3.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens) or pygame.sprite.spritecollideany(ship, aliens1) or \
            pygame.sprite.spritecollideany(ship, aliens2):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - 100 - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number, alien_type, frame):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen, alien_type, frame)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    if alien_type == 3:
        alien.x = 0 - alien_width
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number)
    if alien.alien_type == 0:
        aliens.add(alien)
    elif alien.alien_type == 1:
        aliens1.add(alien)
    elif alien.alien_type == 2:
        aliens2.add(alien)
    elif alien.alien_type == 3:
        aliens3.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen, 0, 1)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create UFO
    create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, 0, 0, 3, 1)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        if row_number >= 2:
            alien_type = 2
        else:
            alien_type = row_number
        for alien_number in range(number_aliens_x):
            if alien_number % 2 == 0:
                frame = 2
            else:
                frame = 1
            create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number + 1,
                         alien_type, frame)
