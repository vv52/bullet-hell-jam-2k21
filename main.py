import pygame
from pygame.locals import *
from random import Random
import movement
import projectiles
import player
import enemy as ex
import attacks
import math
import sys

WIDTH = 160
HEIGHT = 240

BG_SIZE = 240
SCROLL_SPEED = 3

FPS = 60

vec = pygame.math.Vector2
rand = Random()


def main():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
    pygame.display.set_caption("Sweet Dreams")
    background = pygame.image.load("data/img/background.png")

    sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    player_beam = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    exA = pygame.sprite.Group()
    exB = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    p1 = player.Player(WIDTH / 2, HEIGHT - (HEIGHT / 4))
    players.add(p1)
    sprites.add(p1)

    inv = player.Circle(p1.pos.x, p1.pos.y)
    pbc = player.PBCircle(p1.pos.x, p1.pos.y)

    e1 = ex.EnemyA(WIDTH / 2, -10)
    e2 = ex.EnemyA(WIDTH / 2, -10)
    e3 = ex.EnemyB(WIDTH / 2, -10)
    exA.add(e1)
    exA.add(e2)
    exB.add(e3)
    enemies.add(e1)
    enemies.add(e2)
    enemies.add(e3)
    sprites.add(e1)
    sprites.add(e2)
    sprites.add(e3)

    bg_offset = 0

    phase_counter = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1.up = True
                if event.key == pygame.K_DOWN:
                    p1.down = True
                if event.key == pygame.K_LEFT:
                    p1.left = True
                if event.key == pygame.K_RIGHT:
                    p1.right = True
                if event.key == pygame.K_z:
                    p1.fire_helper = True
                    if not p1.beam:
                        p1.firing = True
                if event.key == pygame.K_x:
                    p1.firing = False
                    p1.beam = True
                    p1.slow = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    p1.up = False
                if event.key == pygame.K_DOWN:
                    p1.down = False
                if event.key == pygame.K_LEFT:
                    p1.left = False
                if event.key == pygame.K_RIGHT:
                    p1.right = False
                if event.key == pygame.K_z:
                    p1.fire_helper = False
                    p1.firing = False
                    p1.close = False
                if event.key == pygame.K_x:
                    if p1.fire_helper:
                        p1.firing = True
                    p1.beam = False
                    p1.slow = False
                    p1.close = False

    # STAGE START

        if 0 <= phase_counter < 100:
            movement.FrameMove(e1.pos, vec(WIDTH / 4, HEIGHT / 4), 1)
            movement.FrameMove(e2.pos, vec(WIDTH - (WIDTH / 4), HEIGHT / 4), 1)

        if 100 <= phase_counter < 560:
            if phase_counter % 60 == 0:
                for enemy in exA:
                    attacks.CircleSpawner("data/img/bullet_a.png", "data/img/bullet_collide.png", enemy.pos,
                                          1.5, 1, 8, rand.randint(0, 89) - 45, enemy_bullets, bullets, sprites)
            movement.FrameMove(e1.pos, p1.pos, 0.1)
            movement.FrameMove(e2.pos, p1.pos, 0.1)
        if 560 <= phase_counter < 780:
            if phase_counter % 30 == 0:
                for enemy in exA:
                    attacks.CircleSpawner("data/img/bullet_a.png", "data/img/bullet_collide.png", enemy.pos,
                                          1.5, 1, 8, rand.randint(0, 89) - 45, enemy_bullets, bullets, sprites)
            movement.FrameMove(e1.pos, vec(-20, e1.pos.y), 0.4)
            movement.FrameMove(e2.pos, vec(WIDTH + 20, e2.pos.y), 0.4)
            movement.FrameMove(e3.pos, vec(WIDTH / 2, HEIGHT / 3), 0.4)
        if 780 <= phase_counter < 1380:
            if phase_counter % 5 == 0:
                for enemy in exB:
                    attacks.CircleSpawner("data/img/bullet_a.png", "data/img/bullet_collide.png", enemy.pos,
                                          1, 0, 5, phase_counter % 360, enemy_bullets, bullets, sprites)
        if 1380 <= phase_counter < 1620:
            if phase_counter % 30 == 0 and len(exB) > 0:
                attacks.CircleSpawner("data/img/bullet_a.png", "data/img/bullet_collide.png", e3.pos,
                                      1.5, 1, 8, rand.randint(0, 89) - 45, enemy_bullets, bullets, sprites)
            movement.FrameMove(e3.pos, vec(WIDTH / 2, HEIGHT + 20), 1)

    # STAGE END

    # HANDLE PLAYER ATTACKS

        if p1.firing and p1.shot_timer == 0:
            pb = projectiles.PlayerBullet(vec(p1.pos.x, p1.pos.y - 8))
            player_bullets.add(pb)
            bullets.add(pb)
            sprites.add(pb)
            p1.shot_timer = 10
        if p1.beam:
            pb = projectiles.PlayerBeam(vec(p1.pos.x, p1.pos.y - 8))
            bullets.add(pb)
            player_beam.add(pb)
            sprites.add(pb)

    # CHECK PLAYER DEATH

        for bullet in enemy_bullets:
            p1_hit = pygame.sprite.collide_mask(p1, bullet)
            if p1_hit and p1.spawn_timer == 0:
                p1.death = True

    # HANDLE ENEMY DAMAGE AND PROXIMITY CALCULATION

        for enemy in enemies:
            p1_ex_hit = pygame.sprite.collide_mask(p1, enemy)
            if p1_ex_hit and p1.spawn_timer == 0:
                p1.death = True
            p1_pb1_hit = pygame.sprite.spritecollide(enemy, player_bullets, True)
            if p1_pb1_hit:
                if -50 <= math.hypot(e1.pos.x - p1.pos.x, e1.pos.y - p1.pos.y) <= 50:
                    enemy.health -= 20
                    p1.close = True
                else:
                    enemy.health -= 10
                    p1.close = False
                if enemy.health < 0:
                    enemy.kill()
            p1_pb2_hit = pygame.sprite.spritecollide(enemy, player_beam, True)
            if p1_pb2_hit:
                if -50 <= math.hypot(e1.pos.x - p1.pos.x, e1.pos.y - p1.pos.y) <= 50:
                    enemy.health -= 2
                    p1.close = True
                else:
                    enemy.health -= 1
                    p1.close = False
                if enemy.health < 0:
                    enemy.kill()
            #if enemy.rect.center[1] > (HEIGHT / 3) * 2:
            #    enemy.pos = vec(enemy.pos.x, (HEIGHT / 3) * 2)

    # HANDLE PLAYER DEATH

        if p1.death:
            p1.kill()
            p1 = player.Player(WIDTH / 2, HEIGHT - (HEIGHT / 4))
            players.add(p1)
            sprites.add(p1)

    # DESPAWN BULLETS ONCE THEY'VE LEFT THE SCREEN

        for bullet in bullets:
            if bullet.rect.center[0] < -4:
                bullet.kill()
            elif bullet.rect.center[0] > WIDTH + 4:
                bullet.kill()
            elif bullet.rect.center[1] > HEIGHT + 4:
                bullet.kill()
            elif bullet.rect.center[1] < -4:
                bullet.kill()

    # RENDER INFINITE BACKGROUND SCROLL

        if bg_offset == BG_SIZE:
            bg_offset = 0
        screen.blit(background, background.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + bg_offset)))
        screen.blit(background, background.get_rect(center=(WIDTH / 2, (HEIGHT / 2) - HEIGHT + bg_offset)))
        bg_offset += SCROLL_SPEED

    # RENDER PLAYER INVINCIBILITY INDICATOR

        if p1.spawn_timer > 60:
            inv.rect.center = p1.rect.center
            screen.blit(inv.image, inv.rect)
        if 60 >= p1.spawn_timer > 0:
            if phase_counter % 15 < 10:
                inv.rect.center = p1.rect.center
                screen.blit(inv.image, inv.rect)

    # RENDER PLAYER POINT BLANK CIRCLE

        if p1.close:
            pbc.rect.center = p1.rect.center
            screen.blit(pbc.image, pbc.rect)

    # UPDATE AND DRAW EVERYTHING OTHER THAN THE BACKGROUND AND CIRCLES

        for obj in sprites:
            obj.update()
            obj.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        phase_counter += 1

    pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()