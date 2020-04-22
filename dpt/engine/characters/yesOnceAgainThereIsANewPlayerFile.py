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
        self.gravity = 0
        self.imunityTime = 180
        self.alive = True
        self.damaged = False
        self.big = True
        self.isRebound = False
        self.Ice = True

    def update(self):
        if self.alive:
            keys = pygame.key.get_pressed()
            mur = -TileManager.camera.last_x

            Game.add_debug_info("Player.damaged = " + str(self.damaged))
            Game.add_debug_info("Player.xvel = " + str(self.xvel))
            Game.add_debug_info("Player.yvel = " + str(self.yvel))
            Game.add_debug_info("Player.jumpCount = " + str(self.jumpCount))

            if keys[pygame.K_LEFT] and self.rect.x - self.xvel - 1 > mur:
                if self.xvel > 0 and not self.Ice:
                    self.xvel = 0
                if -4 * Game.DISPLAY_RATIO > self.xvel > -8 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel >= -4 * Game.DISPLAY_RATIO:
                    self.xvel -= 0.25 * Game.DISPLAY_RATIO
                self.left = True
                self.right = False
                self.standing = False
            elif keys[pygame.K_RIGHT]:
                if self.xvel < 0 and not self.Ice:
                    self.xvel = 0
                if 4 * Game.DISPLAY_RATIO < self.xvel < 8 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel <= 4 * Game.DISPLAY_RATIO:
                    self.xvel += 0.25 * Game.DISPLAY_RATIO
                self.left = False
                self.right = True
                self.standing = False
            else:
                if not self.Ice:
                    self.xvel = 0
                else:
                    if self.xvel > 0.05 * Game.DISPLAY_RATIO:
                        self.xvel -= 0.05 * Game.DISPLAY_RATIO
                    elif self.xvel < -0.05 * Game.DISPLAY_RATIO:
                        self.xvel += 0.05 * Game.DISPLAY_RATIO
                    else:
                        self.xvel = 0
                self.standing = True
                self.walkCount = 0
            if self.allowJump and not self.isRebound:
                if not self.isJump:
                    if keys[pygame.K_UP]:
                        self.isJump = True
                        self.walkCount = 0
                        self.onPlatform = False
                else:
                    if not self.onPlatform:
                        if self.jumpCount >= 0:
                            self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO)
                            self.jumpCount -= 1
                        else:
                            self.isJump = False

            if not self.isJump and not self.isRebound:
                Game.add_debug_info("GRAVITY")
                self.allowJump = False
                self.gravityCount += 1
                self.gravity = math.floor((self.gravityCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * -1
                self.yvel = self.gravity

            if self.isRebound:
                self.rebound()

            self.collide()

            self.rect.left += math.floor(self.xvel)
            if not self.isRebound:
                self.rect.top -= math.floor(self.yvel)

            self.animation()
            self.enemies_collision(self.yvel, TileManager.enemy_group)
            self.deadly_object_collision()
            if self.damaged:
                if self.big:
                    self.height = math.floor(self.height * 0.7)
                    self.width = math.floor(self.width * 0.7)
                    self.walkLeft = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                                     RessourceLoader.get_multiple(self.walkLeftTextures)]
                    self.walkRight = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                                      RessourceLoader.get_multiple(self.walkRightTextures)]
                    self.big = False
                    self.rect[2] //= 1.42
                    self.rect[3] //= 1.42
                    self.mask = pygame.mask.from_surface(pygame.transform.scale(RessourceLoader.get(PlayerSprite.mask),
                                                                                (self.width, self.height)))
                self.imunityTime -= 1
            else:
                if not self.big:
                    self.height = self.CONSTHEIGT
                    self.width = self.CONSTWIDTH
                    self.imunityTime = 180
        else:
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
                            if -8 * Game.DISPLAY_RATIO <= rect.height <= 8 * Game.DISPLAY_RATIO:
                                dy = rect.height
                                self.yvel = 0
                                self.onPlatform = True
                                self.gravityCount = 0
                                self.isJump = False
                                self.allowJump = True
                                self.jumpCount = self.CONSTJUMPCOUNT
                                self.isRebound = False
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
                            self.isRebound = False
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
                        Game.add_debug_info("dx = " + str(dx))
                        if self.rect.x > i.rect.x:
                            dx = rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        elif self.rect.x < i.rect.x:
                            dx = - rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        break

                    self.rect.x += dx

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
                    self.jumpCount = 25
                    self.rebound()
                    self.isRebound = True
                print(i)

    def enemies_collision(self, yVelDelta, enemies):
        for i in enemies:
            if pygame.sprite.collide_rect(self, i):
                if yVelDelta < 0:
                    if self.damaged and self.imunityTime < 150:
                        i.kill()
                    elif not self.damaged:
                        i.kill()
                else:
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
                        self.jumpCount = 25
                        self.rebound()
                        self.isRebound = True

    def die(self):
        self.alive = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * neg
        self.jumpCount -= 1
        self.rect.top -= self.yvel

    def death_fall(self):
        if self.rect.top >= Game.surface.get_size()[1]:
            Game.get_logger("Player").info("Player sprite killed")
            Game.freeze_game = True
            Game.player_sprite.kill()
            del self

    def rebound(self):
        self.allowJump = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.gravityCount ** 2) * 0.01 * Game.DISPLAY_RATIO) * neg
        self.jumpCount -= 1
        self.collide()
        self.rect.top -= self.yvel
