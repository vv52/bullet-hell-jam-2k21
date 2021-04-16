import pygame
from pygame.locals import *
from pygame.math import Vector2
import sprite

WIDTH = 160
HEIGHT = 240

FPS = 60

FAST = 2.4
SLOW = 1.2

vec = pygame.math.Vector2


class Player(sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__("data/img/player.png", spawn_x, spawn_y)
        self.mask = pygame.mask.from_surface(pygame.image.load("data/img/player_collide.png"))
        self.pos = vec(self.rect.center)
        self.acc = vec(0, 0)
        self.speed = FAST
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.slow = False
        self.firing = False
        self.beam = False
        self.grazing = False
        self.clears = 2
        self.spawn_timer = 120
        self.shot_timer = 10

    def update(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        if self.shot_timer > 0:
            self.shot_timer -= 1
        if self.slow:
            self.speed = SLOW
        else:
            self.speed = FAST
        self.move()

    def move(self):
        if self.up:
            self.acc.y = -self.speed
        elif self.down:
            self.acc.y = self.speed
        else:
            self.acc.y = 0
        if self.left:
            self.acc.x = -self.speed
        elif self.right:
            self.acc.x = self.speed
        else:
            self.acc.x = 0
        self.pos += self.acc

        if self.pos.x > WIDTH - 4:
            self.pos.x = WIDTH - 4
        if self.pos.x < 4:
            self.pos.x = 4
        if self.pos.y > HEIGHT - 4:
            self.pos.y = HEIGHT - 4
        if self.pos.y < 4:
            self.pos.y = 4

        self.rect.center = self.pos
