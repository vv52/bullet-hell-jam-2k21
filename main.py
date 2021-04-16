import pygame
from pygame.locals import *
import projectiles
import player
import sys

WIDTH = 160
HEIGHT = 240

BG_SIZE = 240
SCROLL_SPEED = 3

FPS = 60

vec = pygame.math.Vector2


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
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    p1 = player.Player(WIDTH / 2, HEIGHT / 2)
    players.add(p1)
    sprites.add(p1)

    bg_offset = 0

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
                if event.key == pygame.K_x:
                    if p1.fire_helper:
                        p1.firing = True
                    p1.beam = False
                    p1.slow = False

        if p1.firing and p1.shot_timer == 0:
            pb = projectiles.PlayerBullet(vec(p1.pos.x, p1.pos.y - 8))
            player_bullets.add(pb)
            sprites.add(pb)
            p1.shot_timer = 10
        if p1.beam:
            pb = projectiles.PlayerBeam(vec(p1.pos.x, p1.pos.y - 8))
            player_bullets.add(pb)
            sprites.add(pb)

        if bg_offset == BG_SIZE:
            bg_offset = 0
        screen.blit(background, background.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + bg_offset)))
        screen.blit(background, background.get_rect(center=(WIDTH / 2, (HEIGHT / 2) - HEIGHT + bg_offset)))
        bg_offset += SCROLL_SPEED

        for obj in sprites:
            obj.update()
            obj.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()