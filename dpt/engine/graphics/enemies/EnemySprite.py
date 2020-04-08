import pygame
import random
import math

from opensimplex import OpenSimplex
from dpt.game import Game


class EnemySprite(pygame.sprite.Sprite):
    screen_width, screen_height = Game.surface.get_size()
    char = Game.ressources.get("dpt.images.characters.player.standing")

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = EnemySprite.char
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0
        self.left = True
        self.right = False
        self.standing = False
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.gravityCount = 0
        self.gravity = 0
        self.tmp = OpenSimplex()
        self.x = random.randint(0, 10000)
        self.y = 0

    def update(self):
        self.y += 0.02
        if 0.95 > self.tmp.noise2d(self.x, self.y) > 0:
            if self.xvel > 0:
                self.xvel = 0
            if self.xvel > -8:
                self.xvel -= 1
            self.left = True
            self.right = False
            self.standing = False
        elif -0.95 < self.tmp.noise2d(self.x, self.y) < 0:
            if self.xvel < 0:
                self.xvel = 0
            if self.xvel < 8:
                self.xvel += 1
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.xvel = 0
            self.standing = True

        self.rect.left += self.xvel
        self.collide(self.xvel, 0, Game.enemyList)
        self.rect.top -= self.yvel
        self.collide(0, self.yvel, Game.enemyList)

        if not self.isJump:
            self.allowJump = False
            self.gravityCount += 1
            self.gravity = math.floor((self.gravityCount ** 2) * 0.5) * -1
            self.rect.top -= self.gravity
            self.collide(0, self.gravity, Game.enemyList)
        self.animation()

    def animation(self):
        pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)

    def collide(self, xVelDelta, yVelDelta, platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                if xVelDelta > 0:
                    self.rect.right = i.rect.left
                    self.xvel = 0
                if xVelDelta < 0:
                    self.rect.left = i.rect.right
                    self.xvel = 0
                if yVelDelta < 0:
                    self.rect.bottom = i.rect.top
                    self.onPlatform = True
                    self.jumpCount = self.CONSTJUMPCOUNT
                    self.allowJump = True
                    self.gravityCount = 0
                if yVelDelta > 0:
                    self.rect.top = i.rect.bottom
