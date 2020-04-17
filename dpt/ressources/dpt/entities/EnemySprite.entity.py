import math

import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class EnemySprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.player.standing"
    screen_width, screen_height = Game.surface.get_size()
    width = math.floor(60 * Game.DISPLAY_RATIO)
    height = math.floor(90 * Game.DISPLAY_RATIO)
    offset_x = (Game.TILESIZE - width) // 2
    offset_y = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemy_group, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.xvel = 0
        self.yvel = 0
        self.left = False
        self.right = True
        self.standing = False
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.isJump = False
        self.jumpCount = 21
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.gravityCount = 0
        self.gravity = 0
        self.lastx = 0
        self.lasty = 0
        self.securityTime = 60

    def update(self):
        from dpt.engine.tileManager import TileManager
        if not Game.freeze_game:
            if self.left:
                if self.xvel > 0:
                    self.xvel = 0
                if self.xvel > -2 * Game.DISPLAY_RATIO:
                    self.xvel -= 1 * Game.DISPLAY_RATIO
                self.left = True
                self.right = False
                self.standing = False
            elif self.right:
                if self.xvel < 0:
                    self.xvel = 0
                if self.xvel < 2 * Game.DISPLAY_RATIO:
                    self.xvel += 1 * Game.DISPLAY_RATIO
                self.left = False
                self.right = True
                self.standing = False
            else:
                self.xvel = 0
                self.standing = True

            self.lastx = self.rect.left
            self.rect.left += self.xvel
            self.collide(self.xvel, 0, TileManager.environment_group)

            if not self.isJump:
                self.allowJump = False
                self.gravityCount += 1
                self.gravity = math.floor((self.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
                self.rect.top -= self.gravity
                self.collide(0, self.gravity, TileManager.environment_group)
        self.animation()

        Game.add_debug_info("Enemy.lastx = " + str(self.lastx))
        Game.add_debug_info("Enemy.rect.left" + str(self.rect.left))
        Game.add_debug_info("Enemy.left " + str(self.left))
        Game.add_debug_info("Enemy.right " + str(self.right))

        if self.lastx == self.rect.left:
            self.left = not self.left
            self.right = not self.right

        self.securityTime -= 1
        if self.check_fall(TileManager.environment_group):
            self.left = not self.left
            self.right = not self.right

            if self.left:
                self.xvel -= 1 * Game.DISPLAY_RATIO
            elif self.right:
                self.xvel += 1 * Game.DISPLAY_RATIO

        self.rect.top -= self.yvel
        self.collide(0, self.yvel, TileManager.environment_group)
        self.check_void()

    def animation(self):
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)
        pass

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
                        self.gravityCount = 0
                    if y_vel_delta > 0:
                        self.rect.top = i.rect.bottom

    def check_void(self):
        if self.rect.top > 2000:
            self.kill()

    def check_fall(self, platforms):
        if self.securityTime < 0:
            if self.right:
                neg = 1
            else:
                neg = -1
            self.rect.left += self.width * Game.DISPLAY_RATIO * neg
            self.rect.top += self.height * Game.DISPLAY_RATIO
            for i in platforms:
                if pygame.sprite.collide_rect(self, i):
                    self.rect.left -= self.width * Game.DISPLAY_RATIO * neg
                    self.rect.top -= self.height * Game.DISPLAY_RATIO
                    return False
            self.rect.left -= self.width * Game.DISPLAY_RATIO * neg
            self.rect.top -= self.height * Game.DISPLAY_RATIO
            self.securityTime = 60
            return True
