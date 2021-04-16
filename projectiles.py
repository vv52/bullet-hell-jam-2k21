import pygame
from pygame.locals import *
from random import Random

vec = pygame.math.Vector2
rand = Random()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, col_img, pos, angle, mult, jit):
        super().__init__()
        self.image = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(pygame.image.load(col_img))
        self.rect = self.image.get_rect()
        self.rect.center = [pos.x, pos.y]
        self.vel = vec(1, 0).rotate(angle) * mult
        self.pos = vec(self.rect.center)
        self.jit = jit

    def update(self):
        if self.jit > 0:
            offset = vec((rand.randint(0, self.jit) - (self.jit / 2)),
                         (rand.randint(0, self.jit) - (self.jit / 2)))
        else:
            offset = 0
        self.pos += self.vel + offset
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("data/img/player_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [pos.x, pos.y]
        self.pos = vec(self.rect.center)
        self.speed = vec(0, 4)

    def update(self):
        self.pos -= self.speed
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlayerBeam(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("data/img/player_beam.png")
        self.rect = self.image.get_rect()
        self.rect.center = [pos.x, pos.y]
        self.pos = vec(self.rect.center)
        self.speed = vec(0, 5)

    def update(self):
        self.pos -= self.speed
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)