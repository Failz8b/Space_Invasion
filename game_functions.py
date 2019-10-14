import sys
import random
from time import sleep

import pygame
import pygame.gfxdraw

from bullet import Bullet
from alien import Alien
from bunker import Bunker


def check_keydown_events(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                         event, bunkers):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active:
            ai_settings.hold_space = True
    elif event.key == pygame.K_l:
        if stats.game_active:
            ai_settings.hold_l = True
    elif event.key == pygame.K_k:
        if stats.game_active:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers)
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
    elif event.key == pygame.K_l:
        ai_settings.hold_l = False


def check_events(ai_settings, screen, stats, sb, play_button, hi_score_button, back_button, ship, aliens, aliens1,
                 aliens2, aliens3, bullets, abullets, bunkers):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets,
                                 abullets, event, bunkers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, ai_settings)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliens1, aliens2, aliens3,
                              bullets, abullets, mouse_x, mouse_y, bunkers)
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
                      abullets, mouse_x, mouse_y, bunkers):
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
        check_high_score(stats, sb)
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
        abullets.empty()
        bunkers.empty()

        # Create a new , bunkers, and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)
        create_bunker_array(ai_settings, screen, ship, bunkers)
        ship.center_ship()

        # Play in game music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/background/in_game.mp3')
        pygame.mixer.music.play(-1, 0.0)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed and ai_settings.shoot_timer >= ai_settings.shoot_delay:
        new_bullet = Bullet(ai_settings, screen, ship, 0)
        # Cheat Bullets
        if ai_settings.hold_l:
            new_bullet.image = pygame.transform.scale(new_bullet.image, (ai_settings.screen_width * 2, 30))
            new_bullet.rect = new_bullet.image.get_rect()
            new_bullet.mask = pygame.mask.from_surface(new_bullet.image)
            new_bullet.rect.centerx = ship.rect.centerx
            new_bullet.rect.y = ship.rect.y
        else:
            new_bullet.image = pygame.transform.scale(new_bullet.image, (3, 15))
            new_bullet.rect = new_bullet.image.get_rect()
            new_bullet.mask = pygame.mask.from_surface(new_bullet.image)
            new_bullet.rect.centerx = ship.rect.centerx
            new_bullet.rect.y = ship.rect.y
        bullets.add(new_bullet)
        ai_settings.shoot_timer = 0
        ship.sound_fire.play()


def afire_bullet(ai_settings, screen, alien, abullets, stats):
    if len(abullets) < ai_settings.abullets_allowed and ai_settings.abullet_timer >= ai_settings.abullet_wait\
            and stats.game_active:
        new_bullet = Bullet(ai_settings, screen, alien, 1)
        abullets.add(new_bullet)
        ai_settings.abullet_timer = 0
        alien.alien_shoot.play()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                  play_button, hi_score_button, back_button, bunkers):
    """Update images on the screen, and flip to the new screen."""
    # Shoot Bullet if Space is held down
    if ai_settings.hold_space:
        fire_bullet(ai_settings, screen, ship, bullets)

    """Aliens shooting"""
    if random.randint(0, 100) < ai_settings.abullet_frequency:
        a_group = random.choice((aliens, aliens1, aliens2))
        for alien in a_group:
            if random.randint(0, 100) < 5:
                afire_bullet(ai_settings, screen, alien, abullets, stats)

    # UFO?
    if stats.game_active:
        ai_settings.ufo_timer += 1
        ai_settings.ufo_display += 1
    else:
        ai_settings.ufo_timer = 0
    if ai_settings.ufo_timer >= ai_settings.ufo_rand:
        ai_settings.spawn_ufo = True
        for alien in aliens3:
            '''USE THIS TO MAKE THE UFO SOUND LOUDER, at the cost of muting sounds in general while it plays
            alien.ufo_sound.set_volume(.1)
            alien.ufo_sound.play()
            '''
            if not alien.ufo_sound_playing:
                u_channel = pygame.mixer.Channel(1)
                u_channel.play(alien.ufo_sound)
                alien.ufo_sound_playing = True
    for alien in aliens3:
        if alien.x > ai_settings.screen_width + alien.rect.width:
            alien.ufo_sound.fadeout(1000)
            alien.ufo_sound_playing = False
            alien.kill()

    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in abullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    aliens1.draw(screen)
    aliens2.draw(screen)
    aliens3.draw(screen)
    bunkers.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive or HS screen if HS is active.
    if not stats.game_active:
        if ai_settings.hs_screen:
            screen.fill(ai_settings.bg_color)

            # Display High Scores
            hs_shadow = ai_settings.hs_font.render("Hi Scores!!!", True, ai_settings.green, ai_settings.bg_color)
            hs_title = ai_settings.hs_font.render("Hi Scores!!!", False, ai_settings.title_color)
            hs_s_rect = hs_shadow.get_rect()
            hs_t_rect = hs_title.get_rect()
            hs_s_rect.midtop = ((ai_settings.screen_width / 2) + 3, 105)
            hs_t_rect.midtop = ((ai_settings.screen_width / 2), 100)
            screen.blit(hs_shadow, hs_s_rect)
            screen.blit(hs_title, hs_t_rect)

            score = [0] * 10
            score_rect = [pygame.Rect] * 10

            for i in range(10):
                score[i] = ai_settings.font.render(str(sb.hs_list[i]), False, ai_settings.green)
                score_rect[i] = score[i].get_rect()
                score_rect[i].center = (ai_settings.screen_width / 2, ((i + 2) * 60) + 115)
                screen.blit(score[i], score_rect[i])

            back_button.draw_button()
        else:
            # Fill bg
            screen.fill(ai_settings.bg_color)

            # Cool Looking Title
            title_shadow = ai_settings.title_font.render("Space Invaders", True, ai_settings.green,
                                                         ai_settings.bg_color)
            title = ai_settings.title_font.render("Space Invaders", False, ai_settings.title_color)
            title_rect_s = title_shadow.get_rect()
            title_rect = title.get_rect()
            title_rect_s.midtop = ((ai_settings.screen_width / 2) + 3, 105)
            title_rect.midtop = ((ai_settings.screen_width / 2), 100)
            screen.blit(title_shadow, title_rect_s)
            screen.blit(title, title_rect)

            # Point Values
            a_text = [0] * 4
            a_text_rect = [(0, 0)] * 4
            rect_half = [0] * 4

            a_text[0] = ai_settings.font_point.render((" = " + str(ai_settings.points_a1) + " Points"), True,
                                                      ai_settings.green, ai_settings.bg_color)
            a_text[1] = ai_settings.font_point.render((" = " + str(ai_settings.points_a2) + " Points"), True,
                                                      ai_settings.green, ai_settings.bg_color)
            a_text[2] = ai_settings.font_point.render((" = " + str(ai_settings.points_a3) + " Points"), True,
                                                      ai_settings.green, ai_settings.bg_color)
            a_text[3] = ai_settings.font_point.render(" = ??? Points", True, ai_settings.green, ai_settings.bg_color)

            for i in range(4):
                a_text_rect[i] = a_text[i].get_rect()

            # Draw Aliens
            a_sprite = [Alien] * 4
            for i in range(4):
                a_sprite[i] = Alien(ai_settings, screen, i, 1)

            # Balanced, as all things should be
            for i in range(4):
                rect_half[i] = (a_sprite[i].rect.width + a_text_rect[i].width + 10) / 2
                a_text_rect[i].midright = ((ai_settings.screen_width / 2) + rect_half[i], ((i * 80) + 250))
                a_sprite[i].rect.midleft = ((ai_settings.screen_width / 2) - rect_half[i], ((i * 80) + 250))
                screen.blit(a_text[i], a_text_rect[i])
                a_sprite[i].blitme()

            play_button.draw_button()
            hi_score_button.draw_button()

        stats.game_active = False

    ai_settings.alien_number = len(aliens) + len(aliens1) + len(aliens2)

    if ai_settings.alien_number <= 15 and not ai_settings.music_faster:
        ai_settings.music_pos += pygame.mixer.music.get_pos()
        music_time = ai_settings.music_pos / 1150
        pygame.mixer.music.load('sounds/background/in_game_faster.mp3')
        pygame.mixer.music.play(-1, music_time)
        ai_settings.music_faster = True

    if ai_settings.ufo_destroyed and ai_settings.ufo_display <= 180 / ai_settings.sdf:
        ufo_text = ai_settings.font.render(str(ai_settings.ufo_point), True, ai_settings.green, ai_settings.bg_color)
        screen.blit(ufo_text, ai_settings.ufo_pos)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

    # Update Timer Variables
    ai_settings.shoot_timer += 1
    ai_settings.abullet_timer += 1


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets, bunkers):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    abullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in abullets.copy():
        if bullet.rect.bottom >= ai_settings.screen_width:
            abullets.remove(bullet)

    check_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    for i in range(10):
        if stats.score >= sb.hs_list[i]:
            if i == 0:
                stats.high_score = stats.score
                break
            else:
                stats.high_score = sb.hs_list[i - 1]
                break
        else:
            stats.high_score = sb.hs_list[9]
        stats.standing = i + 1
    sb.prep_high_score()


def check_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    collisions1 = pygame.sprite.groupcollide(bullets, aliens1, True, False)
    collisions2 = pygame.sprite.groupcollide(bullets, aliens2, True, False)
    collisions3 = pygame.sprite.groupcollide(bullets, aliens3, True, True)
    if ai_settings.hold_l:
        collisions4 = pygame.sprite.groupcollide(bullets, bunkers, False, False)
    else:
        collisions4 = pygame.sprite.groupcollide(bullets, bunkers, True, False, pygame.sprite.collide_mask)
    collisions5 = pygame.sprite.groupcollide(bunkers, aliens, True, False)
    collisions6 = pygame.sprite.groupcollide(bunkers, aliens1, True, False)
    collisions7 = pygame.sprite.groupcollide(bunkers, aliens2, True, False)
    collisions8 = pygame.sprite.spritecollide(ship, abullets, True)
    collisions9 = pygame.sprite.groupcollide(abullets, bunkers, True, False, pygame.sprite.collide_mask)

    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a1 = round(int(ai_settings.alien_points * len(aliens) * ai_settings.t0_scale),
                                                  -1)
                    stats.score += ai_settings.points_a1
                    sb.prep_score()
        check_high_score(stats, sb)

    if collisions1:
        for aliens1 in collisions1.values():
            for alien in aliens1:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a2 = round(int(ai_settings.alien_points * len(aliens1) * ai_settings.t1_scale),
                                                  -1)
                    stats.score += ai_settings.points_a2
                    sb.prep_score()
        check_high_score(stats, sb)

    if collisions2:
        for aliens2 in collisions2.values():
            for alien in aliens2:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3
                    ai_settings.points_a3 = round(int(ai_settings.alien_points * len(aliens2) * ai_settings.t2_scale),
                                                  -1)
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
                alien.ufo_sound_playing = False
                alien.ufo_des_sound.play()
        check_high_score(stats, sb)

    if collisions4:
        if not ai_settings.hold_l:
            for bullet in collisions4.keys():
                ai_settings.c_x = bullet.rect.centerx
                ai_settings.c_y = int(bullet.y)
            for bunkers in collisions4.values():
                for bunker in bunkers:
                    ai_settings.c_x -= bunker.rect.x
                    ai_settings.c_y -= bunker.rect.y
                    pygame.gfxdraw.filled_circle(bunker.image, ai_settings.c_x, ai_settings.c_y, 20, (0, 0, 0, 255))
                    bunker.image_update()
                    bunker.mask = pygame.mask.from_surface(bunker.image)
                    b_channel = pygame.mixer.Channel(2)
                    b_channel.play(bunker.destroyed_sound)

    if collisions5:
        for aliens in collisions5.values():
            for alien in aliens:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3

    if collisions6:
        for aliens1 in collisions6.values():
            for alien in aliens1:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3

    if collisions7:
        for aliens2 in collisions7.values():
            for alien in aliens2:
                if alien.anim_frame < 3:
                    alien.anim_frame = 3

    if collisions8:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets, bunkers)

    if collisions9:
        for bullet in collisions9.keys():
            ai_settings.c_x = bullet.rect.centerx
            ai_settings.c_y = int(bullet.y) + bullet.rect.height
        for bunkers in collisions9.values():
            for bunker in bunkers:
                ai_settings.c_x -= bunker.rect.x
                ai_settings.c_y -= bunker.rect.y
                pygame.gfxdraw.filled_circle(bunker.image, ai_settings.c_x, ai_settings.c_y, 50, (0, 0, 0, 255))
                bunker.image_update()
                bunker.mask = pygame.mask.from_surface(bunker.image)
                b_channel = pygame.mixer.Channel(2)
                b_channel.play(bunker.destroyed_sound)

    if len(aliens) == 0 and len(aliens1) == 0 and len(aliens2) == 0 and \
            (len(aliens3) == 0 or not ai_settings.spawn_ufo):
        # If the entire fleet is destroyed, start a new level.
        aliens3.empty()
        bullets.empty()
        abullets.empty()
        bunkers.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, aliens1, aliens2, aliens3)
        create_bunker_array(ai_settings, screen, ship, bunkers)

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


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets, bunkers):
    """Respond to ship being hit by alien."""
    ship.des_sound.play()
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
    else:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        stats.game_active = False
        pygame.mouse.set_visible(True)

        for j in range(10):
            if stats.score >= sb.hs_list[j]:
                for i in range(9 - j):
                    sb.hs_list[9 - i] = sb.hs_list[9 - i - 1]
                sb.hs_list[j] = stats.score
                break

        # Open/Create a HS File
        with open("hi_scores.txt", "w+") as f:
            for i in range(10):
                f.write(str(sb.hs_list[i]) + "\n")

        # Play Menu Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/background/menu.mp3')
        pygame.mixer.music.play(-1, 0.0)

    # Empty the list of aliens and bullets.
    aliens.empty()
    aliens1.empty()
    aliens2.empty()
    for alien in aliens3:
        alien.kill()
        alien.ufo_sound.stop()
        alien.ufo_sound_playing = False
    aliens3.empty()
    bullets.empty()
    abullets.empty()
    bunkers.empty()

    # Set New UFO timers
    ai_settings.ufo_timer = 0
    ai_settings.ufo_rand = random.randint(500, 10000) / ai_settings.alien_speed_factor
    ai_settings.spawn_ufo = False
    ai_settings.ufo_destroyed = False

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
    create_bunker_array(ai_settings, screen, ship, bunkers)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                        bunkers):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers)
            break
    for alien in aliens1.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers)
            break
    for alien in aliens2.sprites():
        if alien.rect.bottom >= screen_rect.bottom and alien.anim_frame < 3:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                     bunkers)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets, bunkers):
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
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                 bunkers)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliens1, aliens2, aliens3, bullets, abullets,
                        bunkers)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 3 * alien_width
    number_aliens_x = int(available_space_x / (1.7 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - 100 - (6 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number, alien_type, frame):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen, alien_type, frame)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.7 * alien_width * alien_number
    if alien_type == 3:
        alien.x = 0 - alien_width
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 1.5 * alien.rect.height * row_number)
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
            if (alien_number + row_number) % 2 == 0:
                frame = 2
            else:
                frame = 1
            create_alien(ai_settings, screen, aliens, aliens1, aliens2, aliens3, alien_number, row_number + 1,
                         alien_type, frame)


def get_number_bunkers(ai_settings, bunker_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width
    number_bunker = int(available_space_x / (4 * bunker_width))
    return number_bunker


def create_bunker(ai_settings, screen, ship, bunkers, bunker_number):
    """Create a bunker, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = (4 * bunker_width * (bunker_number + 1)) - (5 * bunker_width / 2)
    bunker.rect.x = bunker.x
    bunker.rect.y = ai_settings.screen_height - ship.rect.height - 30 - bunker.rect.height
    bunkers.add(bunker)


def create_bunker_array(ai_settings, screen, ship, bunkers):
    """Create a bunker and put it in the defense array"""
    bunker = Bunker(ai_settings, screen)
    number_bunkers = get_number_bunkers(ai_settings, bunker.rect.width)

    # Create Defense Array
    for bunker_number in range(number_bunkers):
        create_bunker(ai_settings, screen, ship, bunkers, bunker_number)
