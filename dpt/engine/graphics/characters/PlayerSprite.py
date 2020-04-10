import pygame
import math
import time

from dpt.game import Game


class PlayerSprite(pygame.sprite.Sprite):
    screen_width, screen_height = Game.surface.get_size()
    char = Game.ressources.get("dpt.images.characters.player.standing")
    walkRight = Game.ressources.get_multiple("dpt.images.characters.player.R*")
    walkLeft = Game.ressources.get_multiple("dpt.images.characters.player.L*")
    gravityCount = 0

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = PlayerSprite.char
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
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.alive = True

    def update(self):

        if self.alive:

            keys = pygame.key.get_pressed()
            mur = -Game.camera.last_x
            Game.add_debug_info("Scrolling : " + str(mur))

            if keys[pygame.K_LEFT] and self.rect.x - self.xvel - 1 > mur:
                if self.xvel > 0:
                    self.xvel = 0
                if self.xvel > -8:
                    self.xvel -= 1
                self.left = True
                self.right = False
                self.standing = False
            elif keys[pygame.K_RIGHT]:
                if self.xvel < 0:
                    self.xvel = 0
                if self.xvel < 8:
                    self.xvel += 1
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
                        self.yvel = math.floor((self.jumpCount ** 2) * 0.5) * neg
                        self.jumpCount -= 1
                    elif self.onPlatform:
                        self.jumpCount = self.CONSTJUMPCOUNT
                        self.isJump = False
                        self.yvel = 0

            self.rect.left += self.xvel
            self.collide(self.xvel, 0, Game.environment)
            self.rect.top -= self.yvel
            self.collide(0, self.yvel, Game.environment)

            if not self.isJump:
                self.allowJump = False
                PlayerSprite.gravityCount += 1
                PlayerSprite.gravity = math.floor((PlayerSprite.gravityCount ** 2) * 0.5) * -1
                self.rect.top -= PlayerSprite.gravity
                self.collide(0, PlayerSprite.gravity, Game.environment)

            self.animation()
            self.enemiesCollision(self.yvel, Game.enemyGroup)
            self.deathFall()

        elif not self.alive:
            self.die()

    def animation(self):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                self.image = PlayerSprite.walkLeft[self.walkCount // 3]
                self.walkCount += 1
            elif self.right:
                self.image = PlayerSprite.walkRight[self.walkCount // 3]
                self.walkCount += 1
        else:
            if self.right:
                self.image = PlayerSprite.walkRight[0]
            else:
                self.image = PlayerSprite.walkLeft[0]
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)

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
                    PlayerSprite.gravityCount = 0
                if yVelDelta > 0:
                    self.rect.top = i.rect.bottom

    def enemiesCollision(self, yVelDelta, enemies):
        for i in enemies:
            if pygame.sprite.collide_rect(self, i):
                if yVelDelta < 0:
                    Game.enemyGroup.remove(i)
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
            time.sleep(0.5)
            self.die()

    def die(self):
        self.alive = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.jumpCount ** 2) * 0.5) * neg
        self.jumpCount -= 1
        self.rect.top -= self.yvel
