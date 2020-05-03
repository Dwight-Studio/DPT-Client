import pygame
import math
import time
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager
from dpt.engine.gui.ui.Heart import Heart


class PlayerSprite(pygame.sprite.Sprite):
    char = "dpt.images.characters.player.standing"
    walk_right_textures = "dpt.images.characters.player.R-*"
    walk_left_textures = "dpt.images.characters.player.L-*"
    jump_right_texture = "dpt.images.characters.player.RJump"
    jump_left_texture = "dpt.images.characters.player.LJump"
    mask = "dpt.images.characters.player.mask"

    width = math.floor(156 * Game.DISPLAY_RATIO)
    height = math.floor(117 * Game.DISPLAY_RATIO)

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, Game.player_group)  # Sprite's constructor called
        self.CONSTWIDTH = self.width
        self.CONSTHEIGT = self.height
        self.image = pygame.transform.scale(RessourceLoader.get(self.char), (self.width, self.height))
        self.walkLeft = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                         RessourceLoader.get_multiple(self.walk_left_textures)]
        self.jumpLeft = pygame.transform.smoothscale(RessourceLoader.get(self.jump_left_texture), (self.width, self.height))

        self.walkRight = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                          RessourceLoader.get_multiple(self.walk_right_textures)]
        self.jumpRight = pygame.transform.smoothscale(RessourceLoader.get(self.jump_right_texture), (self.width, self.height))

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
        self.Ice = False
        self.Slow = False
        self.frameCount = 0
        self.lowGravity = False
        self.gravityModifier = 0
        self.Fast = False
        self.maxvelocity = 4
        self.jumpBoost = False
        self.jumpModifier = 0
        self.inversion = False
        self.star = False
        self.monsterimmortal = False
        Heart()

    def update(self):
        if self.alive:

            if self.Fast:
                self.maxvelocity = 6
            else:
                self.maxvelocity = 4

            if self.lowGravity:
                self.gravityModifier = 0.04
            else:
                self.gravityModifier = 0

            if self.Slow:
                self.frameCount += 1
            else:
                self.frameCount = 0

            if self.jumpBoost:
                self.jumpModifier = 0.07
            else:
                self.jumpModifier = 0

            keys = pygame.key.get_pressed()
            mur = -TileManager.camera.last_x

            Game.add_debug_info("Player.damaged = " + str(self.damaged))
            Game.add_debug_info("Player.xvel = " + str(self.xvel))
            Game.add_debug_info("Player.yvel = " + str(self.yvel))
            Game.add_debug_info("Player.jumpCount = " + str(self.jumpCount))
            Game.add_debug_info("Player.isJump = " + str(self.isJump))

            if self.inversion:
                left = pygame.K_RIGHT
                right = pygame.K_LEFT
                up = pygame.K_DOWN
            else:
                left = pygame.K_LEFT
                right = pygame.K_RIGHT
                up = pygame.K_UP

            if keys[left] and self.rect.x - self.xvel - 1 > mur:
                if self.xvel > 0 and not self.Ice:
                    self.xvel = 0
                if -self.maxvelocity * Game.DISPLAY_RATIO > self.xvel > -self.maxvelocity * 2 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel >= -self.maxvelocity * Game.DISPLAY_RATIO:
                    self.xvel -= 0.25 * Game.DISPLAY_RATIO
                self.left = True
                self.right = False
                self.standing = False
            elif keys[right]:
                if self.xvel < 0 and not self.Ice:
                    self.xvel = 0
                if self.maxvelocity * Game.DISPLAY_RATIO < self.xvel < self.maxvelocity * 2 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel <= self.maxvelocity * Game.DISPLAY_RATIO:
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
                        if self.rect.x - self.xvel - 1 > mur:
                            self.xvel += 0.05 * Game.DISPLAY_RATIO
                        else:
                            self.xvel = 0
                    else:
                        self.xvel = 0
                self.standing = True
                self.walkCount = 0
            if self.allowJump:
                if not self.isJump:
                    if keys[up]:
                        self.isJump = True
                        self.walkCount = 0
                        self.onPlatform = False
                else:
                    if not self.onPlatform:
                        if (self.jumpCount >= 0 and not self.Slow) or (self.Slow and self.frameCount % 3 == 0):
                            self.yvel = math.floor((self.jumpCount ** 2) * (0.05 + self.gravityModifier + self.jumpModifier) * Game.DISPLAY_RATIO)
                            self.jumpCount -= 1
                            if self.Slow:
                                self.frameCount += 1
                        elif self.jumpCount < 0:
                            self.isJump = False
                        else:
                            self.yvel = 0
                            if self.Slow:
                                self.frameCount += 1

            if not self.isJump:
                if (self.Slow and self.frameCount % 3 == 0) or not self.Slow:
                    self.frameCount += 1
                    Game.add_debug_info("GRAVITY")
                    self.allowJump = False
                    self.gravityCount += 1
                    self.gravity = math.floor((self.gravityCount ** 2) * (0.05 - self.gravityModifier) * Game.DISPLAY_RATIO) * -1
                    self.yvel = self.gravity
                else:
                    self.frameCount += 1

            self.collide()

            self.rect.left += math.floor(self.xvel)
            self.rect.top -= math.floor(self.yvel)

            self.animation()
            self.enemies_collision(self.yvel, TileManager.enemy_group)
            if not self.star:
                self.deadly_object_collision()
            if self.damaged:
                self.imunityTime -= 1
                Game.life = 2
            else:
                self.imunityTime = 180
                Game.life = 1
        else:
            self.die()
        self.death_fall()

    def animation(self):
        add = abs(math.floor(self.xvel / (self.maxvelocity // 4)))
        if self.walkCount + add >= 180:
            self.walkCount = 0

        if self.onPlatform:
            if not self.standing:
                if self.left:
                    self.image = self.walkLeft[self.walkCount // 12 + 1]
                    self.walkCount += add
                elif self.right:
                    self.image = self.walkRight[self.walkCount // 12 + 1]
                    self.walkCount += add
            else:
                if self.right:
                    self.image = self.walkRight[0]
                else:
                    self.image = self.walkLeft[0]
        else:
            if self.right:
                self.image = self.jumpRight
            else:
                self.image = self.jumpLeft
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
                                self.frameCount = 0
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
                            self.frameCount = 0
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
                    self.isJump = True
                    self.walkCount = 0
                    self.onPlatform = False
                    self.damaged = True
                    self.allowJump = True
                    self.gravityCount = 0

    def enemies_collision(self, yVelDelta, enemies):
        for i in enemies:
            if pygame.sprite.collide_rect(self, i):
                if yVelDelta < 0 and not self.monsterimmortal:
                    if self.damaged and self.imunityTime < 150:
                        i.kill()
                    elif not self.damaged:
                        i.kill()
                else:
                    if self.damaged and not self.star:
                        if self.imunityTime < 0:
                            self.alive = False
                            self.yvel = 0
                            Game.freeze_game = True
                            self.xvel = 0
                            time.sleep(0.5)
                            self.die()
                            self.jumpCount = self.CONSTJUMPCOUNT
                    elif self.star:
                        i.kill()
                    else:
                        self.isJump = True
                        self.walkCount = 0
                        self.onPlatform = False
                        self.damaged = True
                        self.allowJump = True
                        self.gravityCount = 0

    def die(self):
        Game.life = 3
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

            from dpt.engine.scenes import Scenes
            Scenes.game_over()

            Game.player_sprite.kill()
            del self
