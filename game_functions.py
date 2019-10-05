import sys
import random
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3, bullets, mouse_x, mouse_y):
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


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, play_button):
    """Update images on the screen, and flip to the new screen."""
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

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


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


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions1 = pygame.sprite.groupcollide(bullets, aliens1, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets, aliens2, True, True)
    collisions3 = pygame.sprite.groupcollide(bullets, aliens3, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens) * ai_settings.t0_scale
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions1:
        for aliens1 in collisions1.values():
            stats.score += ai_settings.alien_points * len(aliens1) * ai_settings.t1_scale
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions2:
        for aliens2 in collisions2.values():
            stats.score += ai_settings.alien_points * len(aliens2) * ai_settings.t2_scale
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions3:
        for aliens3 in collisions3.values():
            stats.score += ai_settings.alien_points * len(aliens3) * ai_settings.t3_scale
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0 and len(aliens1) == 0 and len(aliens2) == 0 and len(aliens3) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)


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
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    aliens1.empty()
    aliens2.empty()
    aliens3.empty()
    bullets.empty()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            break
    for alien in aliens1.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets)
            break
    for alien in aliens2.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
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
    if pygame.sprite.spritecollideany(ship, aliens) or pygame.sprite.spritecollideany(ship, aliens1) or pygame.sprite.spritecollideany(ship, aliens2):
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
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number, alien_type):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + alien.rect.height
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
    alien = Alien(ai_settings, screen, 0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        if row_number >= 2:
            alien_type = 2
        else:
            alien_type = row_number
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number, alien_type)
