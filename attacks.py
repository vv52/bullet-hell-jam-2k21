import pygame
from pygame.locals import *
import projectiles
from random import Random as rand


def CircleSpawner(img, col_img, pos, speed, jit, div, offset, enemy_bullets, bullets, sprites):
    bullet_counter = 0
    angle = 360 / div
    while bullet_counter < div:
        new_bullet = projectiles.Bullet(img, col_img, pos, bullet_counter * angle + offset, speed, jit)
        enemy_bullets.add(new_bullet)
        bullets.add(new_bullet)
        sprites.add(new_bullet)
        bullet_counter += 1