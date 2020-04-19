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
        self.mask = pygame.mask.from_surface(pygame.transform.scale(RessourceLoader.get(PlayerSprite.mask),
                                                                    (self.width, self.height)))
        self.gravityCount = 0

    def update(self):
        keys = pygame.key.get_pressed()
        mur = -TileManager.camera.last_x

        if keys[pygame.K_LEFT] and self.rect.x - self.xvel - 1 > mur:
            if self.xvel > 0:
                self.xvel = 0
            if self.xvel > -8 * Game.DISPLAY_RATIO:
                self.xvel -= 0.5 * Game.DISPLAY_RATIO
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            if self.xvel < 0:
                self.xvel = 0
            if self.xvel < 8 * Game.DISPLAY_RATIO:
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

        if not self.isJump:
            Game.add_debug_info("GRAVITY")
            self.allowJump = False
            self.gravityCount += 1
            self.gravity = math.floor((self.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
            self.yvel = self.gravity

        self.collide()

        self.rect.left += math.floor(self.xvel)
        self.rect.top -= math.floor(self.yvel)

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
                rx = i.rect.x - (self.rect.x + math.floor(self.xvel))
                ry = i.rect.y - (self.rect.y - math.floor(self.yvel))
                if self.mask.overlap(i.mask, (rx, ry)):
                    dx = 0
                    dy = 0

                    if math.floor(self.yvel) == 0:
                        mask = self.mask.overlap_mask(i.mask, (rx, ry))
                        b_rects = mask.get_bounding_rects()
                        for rect in b_rects:
                            if -8 <= rect.height <= 8:
                                dy = rect.height
                                self.yvel = 0
                                self.onPlatform = True
                                self.gravityCount = 0
                                self.isJump = False
                                self.allowJump = True
                                self.jumpCount = self.CONSTJUMPCOUNT
                            break

                    crx = i.rect.x - self.rect.x
                    mask = self.mask.overlap_mask(i.mask, (crx, ry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.y < i.rect.y:
                            dy = rect.height + math.floor(self.yvel)
                            self.yvel = 0
                            self.onPlatform = True
                            self.gravityCount = 0
                            self.isJump = False
                            self.allowJump = True
                            self.jumpCount = self.CONSTJUMPCOUNT
                        elif self.rect.y > i.rect.y:
                            dy = - rect.height + math.floor(self.yvel)
                            self.yvel = 0
                            self.isJump = False
                            self.allowJump = False
                            self.jumpCount = self.CONSTJUMPCOUNT
                        break

                    self.rect.y -= dy

                    cry = (i.rect.y - self.rect.y)
                    mask = self.mask.overlap_mask(i.mask, (rx, cry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.x > i.rect.x:
                            dx = rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        elif self.rect.x < i.rect.x:
                            dx = - rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        break

                    self.rect.x += dx
