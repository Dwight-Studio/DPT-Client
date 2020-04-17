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
        self.CONSTWIDTH = self.width
        self.CONSTHEIGT = self.height
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
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
        self.damaged = False
        self.big = True
        self.imunityTime = 180

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
            self.collide(self.xvel, 0, TileManager.environment_group)
            self.rect.top -= self.yvel
            self.collide(0, self.yvel, TileManager.environment_group)

            if not self.isJump:
                self.allowJump = False
                PlayerSprite.gravityCount += 1
                PlayerSprite.gravity = math.floor((PlayerSprite.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
                self.rect.top -= PlayerSprite.gravity
                self.collide(0, PlayerSprite.gravity, TileManager.environment_group)

            self.animation()
            self.enemies_collision(self.yvel, TileManager.enemy_group)
            self.deadly_object_collision()

            if self.damaged:
                if self.big:
                    self.height *= 0.7
                    self.width *= 0.7
                    self.big = False
                    self.rect[2] //= 1.42
                    self.rect[3] //= 1.42
                self.imunityTime -= 1
            else:
                if not self.big:
                    self.height = self.CONSTHEIGT
                    self.width = self.CONSTWIDTH
                    self.imunityTime = 180

        elif not self.alive:
            self.die()
        self.death_fall()

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
        self.image = pygame.transform.smoothscale(self.image, (math.floor(self.width), math.floor(self.height)))
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)

    def collide(self, x_vel_delta, y_vel_delta, platforms):
        for i in platforms:
            if i.rect.colliderect(Game.display_rect):
                if pygame.sprite.collide_rect(self, i):
                    if x_vel_delta > 0:
                        self.rect.right = i.rect.left
                        self.xvel = 0
                    if x_vel_delta < 0:
                        self.rect.left = i.rect.right
                        self.xvel = 0
                    if y_vel_delta < 0:
                        self.rect.bottom = i.rect.top
                        self.onPlatform = True
                        self.jumpCount = self.CONSTJUMPCOUNT
                        self.allowJump = True
                        PlayerSprite.gravityCount = 0
                    if y_vel_delta > 0:
                        self.rect.top = i.rect.bottom
                        self.jumpCount = 0

    def deadly_object_collision(self):
        for i in TileManager.deadly_object_group:
            if pygame.sprite.collide_rect(self, i):
                if self.damaged:
                    if self.imunityTime < 0:
                        self.alive = False
                        self.yvel = 0
                        Game.freeze_game = True
                        self.xvel = 0
                        time.sleep(0.5)
                        self.die()
                        self.jumpCount = self.CONSTJUMPCOUNT
                else:
                    self.damaged = True

    def enemies_collision(self, yVelDelta, enemies):
        for i in enemies:
            if pygame.sprite.collide_rect(self, i):
                if yVelDelta < 0:
                    i.kill()
                else:
                    if self.damaged:
                        if self.imunityTime < 0:
                            self.yvel = 0
                            Game.freeze_game = True
                            self.xvel = 0
                            time.sleep(0.5)
                            self.die()
                            self.jumpCount = self.CONSTJUMPCOUNT
                    else:
                        self.damaged = True

    def death_fall(self):
        if self.rect.top >= Game.surface.get_size()[1]:
            Game.get_logger("Player").info("Player sprite killed")
            Game.freeze_game = True
            Game.player_sprite.kill()
            del self

    def die(self):
        self.alive = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * neg
        self.jumpCount -= 1
        self.rect.top -= self.yvel
