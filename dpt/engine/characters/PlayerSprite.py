import pygame
import math
import time
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class PlayerSprite(pygame.sprite.Sprite):
    screen_width, screen_height = Game.surface.get_size()
    char = RessourceLoader.get("dpt.images.characters.player.standing")
    walkRight = RessourceLoader.get_multiple("dpt.images.characters.player.R*")
    walkLeft = RessourceLoader.get_multiple("dpt.images.characters.player.L*")
    gravityCount = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = self.char
        self.width = math.floor(60 * Game.DISPLAY_RATIO)
        self.height = math.floor(90 * Game.DISPLAY_RATIO)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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
        self.alive = True

    def update(self):
        if self.alive:
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
                # if self.xvel > 0:
                #    self.xvel -= 1
                # elif self.xvel < 0:
                #    self.xvel += 1
                self.standing = True
                self.walkCount = 0
            if self.allowJump:
                if not self.isJump:
                    if keys[pygame.K_UP]:
                        self.isJump = True
                        self.left = False
                        if self.right:
                            self.right = True
                        else:
                            self.right = False
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

            self.rect.left += self.xvel
            self.collide(self.xvel, 0, TileManager.environmentGroup)
            self.rect.top -= self.yvel
            self.collide(0, self.yvel, TileManager.environmentGroup)

            if not self.isJump:
                self.allowJump = False
                PlayerSprite.gravityCount += 1
                PlayerSprite.gravity = math.floor((PlayerSprite.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
                self.rect.top -= PlayerSprite.gravity
                self.collide(0, PlayerSprite.gravity, TileManager.environmentGroup)

            self.animation()
            self.enemiesCollision(self.yvel, TileManager.enemyGroup)
            self.deadlyObjectCollision()
            self.deathFall()

        elif not self.alive:
            self.die()

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
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)

    def collide(self, xVelDelta, yVelDelta, platforms):
        for i in platforms:
            if i.rect.colliderect(Game.display_rect):
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
                        PlayerSprite.gravityCount = 0
                    if yVelDelta > 0:
                        self.rect.top = i.rect.bottom

    def deadlyObjectCollision(self):
        for i in TileManager.deadlyObjectGroup:
            if pygame.sprite.collide_rect(self, i):
                self.yvel = 0
                Game.isPlayerDead = True
                self.xvel = 0
                time.sleep(0.5)
                self.die()

    def enemiesCollision(self, yVelDelta, enemies):
        for i in enemies:
            if pygame.sprite.collide_rect(self, i):
                if yVelDelta < 0:
                    i.kill()
                else:
                    self.yvel = 0
                    Game.isPlayerDead = True
                    self.xvel = 0
                    time.sleep(0.5)
                    self.die()

    def deathFall(self):
        if self.rect.top > 1400:
            self.yvel = 0
            Game.isPlayerDead = True
            self.xvel = 0
            self.die()

    def die(self):
        self.alive = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * neg
        self.jumpCount -= 1
        self.rect.top -= self.yvel
        self.check_void()

    def check_void(self):
        if self.rect.top > 2000:
            self.kill()
