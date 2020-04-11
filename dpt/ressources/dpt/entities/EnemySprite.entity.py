import pygame
import math

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class EnemySprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.player.standing"
    screen_width, screen_height = Game.surface.get_size()

    def __init__(self, x, y):
        from dpt.engine.graphics.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemyGroup, TileManager.entityGroup)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.xvel = 0
        self.yvel = 0
        self.left = False
        self.right = True
        self.standing = False
        self.width = 48 * Game.DISPLAY_RATIO
        self.height = 72 * Game.DISPLAY_RATIO
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.gravityCount = 0
        self.gravity = 0
        self.lastx = 0
        self.lasty = 0

    def update(self):
        from dpt.engine.graphics.tileManager import TileManager
        if not Game.isPlayerDead:
            if self.left:
                if self.xvel > 0:
                    self.xvel = 0
                if self.xvel > -5:
                    self.xvel -= 1
                self.left = True
                self.right = False
                self.standing = False
            elif self.right:
                if self.xvel < 0:
                    self.xvel = 0
                if self.xvel < 5:
                    self.xvel += 1
                self.left = False
                self.right = True
                self.standing = False
            else:
                self.xvel = 0
                self.standing = True

            self.lastx = self.rect.left
            self.rect.left += self.xvel
            self.collide(self.xvel, 0, TileManager.environmentGroup)

            if not self.isJump:
                self.allowJump = False
                self.gravityCount += 1
                self.gravity = math.floor((self.gravityCount ** 2) * 0.5) * -1
                self.rect.top -= self.gravity
                self.collide(0, self.gravity, TileManager.environmentGroup)
        self.animation()

        if self.lastx == self.rect.left:
            self.left = not self.left
            self.right = not self.right

        self.rect.top -= self.yvel
        self.collide(0, self.yvel, TileManager.environmentGroup)

    def animation(self):
        #pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)
        pass

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
