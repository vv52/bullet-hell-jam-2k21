import pygame
from pygame.locals import *
from pygame.math import Vector2
import sprite

WIDTH = 160
HEIGHT = 240

FPS = 60

FAST = 2.6
SLOW = 1.3

vec = pygame.math.Vector2


class EnemyA(sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__("data/img/enemy_a_0.png", spawn_x, spawn_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(self.rect.center)
        self.timer = 0
        self.frame = 0
        self.health = 200
        self.screen = False

    def update(self):
        if self.timer % 15 == 0:
            if self.frame < 3:
                self.frame += 1
            else:
                self.frame = 0
            self.image = pygame.image.load(f"data/img/enemy_a_{self.frame}.png")
        if self.timer == 60:
            self.timer = 0
        self.timer += 1
        self.rect.center = self.pos


class EnemyB(sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__("data/img/enemy_b_0.png", spawn_x, spawn_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec(self.rect.center)
        self.timer = 0
        self.frame = 0
        self.health = 600
        self.screen = False

    def update(self):
        if self.timer % 5 == 0:
            if self.frame < 6:
                self.frame += 1
            else:
                self.frame = 0
            self.image = pygame.image.load(f"data/img/enemy_b_{self.frame}.png")
        if self.timer == 60:
            self.timer = 0
        self.timer += 1
        self.rect.center = self.pos