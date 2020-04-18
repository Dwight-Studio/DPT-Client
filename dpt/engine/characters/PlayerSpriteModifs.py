import pygame
import math
import time
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class PlayerSprite(pygame.sprite.Sprite):
    screen_width, screen_height = Game.surface.get_size()
    char = "dpt.images.characters.player.standing"
    walkRightTextures = "dpt.images.characters.player.R*"
    walkLeftTextures = "dpt.images.characters.player.L*"
    mask = "dpt.images.characters.player.mask"
    gravityCount = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.width = math.floor(60 * Game.DISPLAY_RATIO)
        self.height = math.floor(90 * Game.DISPLAY_RATIO)
        self.CONSTWIDTH = self.width
        self.CONSTHEIGT = self.height
        self.image = pygame.transform.scale(RessourceLoader.get(self.char), (self.width, self.height))
        self.walkLeft = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                         RessourceLoader.get_multiple(self.walkLeftTextures)]
        self.walkRight = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                          RessourceLoader.get_multiple(self.walkRightTextures)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0
        self.left = True
        self.right = False
        self.standing = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 21
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.isFalling = True
        self.mask = pygame.mask.from_surface(pygame.transform.scale(RessourceLoader.get(PlayerSprite.mask),
                                                                    (self.width, self.height)))

    def update(self):
        keys = pygame.key.get_pressed()
        mur = -TileManager.camera.last_x

        if keys[pygame.K_LEFT] and self.rect.x - self.xvel - 1 > mur:
            if self.xvel > 0:
                self.xvel = 0
            if self.xvel > -4 * Game.DISPLAY_RATIO:
                self.xvel -= 0.5 * Game.DISPLAY_RATIO
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            if self.xvel < 0:
                self.xvel = 0
            if self.xvel < 4 * Game.DISPLAY_RATIO:
                self.xvel += 0.5 * Game.DISPLAY_RATIO
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.xvel = 0
            self.standing = True
            self.walkCount = 0
        if self.allowJump:
            if not self.isJump:
                if keys[pygame.K_UP]:
                    self.isJump = True
                    self.walkCount = 0
                    self.onPlatform = False
            else:
                if not self.onPlatform:
                    if self.jumpCount > 0:
                        neg = 1
                    else:
                        neg = -1
                    self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * neg
                    self.jumpCount -= 1
                elif self.onPlatform:
                    self.jumpCount = self.CONSTJUMPCOUNT
                    self.isJump = False
                    self.yvel = 0

        if not self.isJump:
            self.isFalling = True
            self.allowJump = False
            PlayerSprite.gravityCount += 1
            PlayerSprite.gravity = math.floor((PlayerSprite.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
            self.yvel = PlayerSprite.gravity

        self.collide()

        self.rect.left += self.xvel
        self.rect.top -= self.yvel

        self.animation()

    def animation(self):
        if self.walkCount + 1 >= 54:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                self.image = self.walkLeft[self.walkCount // 6]
                self.walkCount += 1
            elif self.right:
                self.image = self.walkRight[self.walkCount // 6]
                self.walkCount += 1
        else:
            if self.right:
                self.image = self.walkRight[0]
            else:
                self.image = self.walkLeft[0]
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)

    def collide(self):
        for i in TileManager.environment_group:
            if i.rect.colliderect(Game.display_rect):
                rx = math.floor(i.rect.x - (self.rect.x + self.xvel))
                crx = i.rect.x - self.rect.x
                ry = math.floor(i.rect.y - (self.rect.y - self.yvel))
                if self.mask.overlap(i.mask, (rx, ry)):
                    coords = self.mask.overlap(i.mask, (crx, ry))
                    dy = 0
                    if coords is not None:
                        x, y = coords
                        dy = (self.rect.height - y)
                        if dy != 0:
                            self.yvel = 0
                            PlayerSprite.gravityCount = 0
                        if dy > 0:
                            self.onPlatform = True
                            self.allowJump = True
                        self.rect.y -= dy
                    else:
                        self.onPlatform = False
                        self.allowJump = False

                    coords = self.mask.overlap(i.mask, (rx, ry + dy))
                    if coords is not None:
                        x, y = coords
                        dx = (self.rect.width - x)
                        if dx != 0:
                            self.xvel = 0
                        self.rect.x -= dx
