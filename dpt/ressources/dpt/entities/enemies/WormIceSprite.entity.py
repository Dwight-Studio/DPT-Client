import math

import pygame

from dpt.engine.characters.DeadBody import DeadBody
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.effectsManagement import EffectsManagement
from dpt.engine.tileManager import TileManager
from dpt.game import Game


class WormIceSprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.animals.Worm_Ice_1"
    dead_texture = "dpt.images.characters.animals.Dead_Worm_Grass"
    textures = "dpt.images.characters.animals.Worm_Ice_*"
    width = math.floor(77.2 * Game.DISPLAY_RATIO)
    height = math.floor(21.2 * Game.DISPLAY_RATIO)
    offset_x = (Game.TILESIZE - width) // 2
    offset_y = Game.TILESIZE - height
    mask = "dpt.images.characters.animals.wormMask"

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemy_group, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.anim = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(self.textures)]
        self.animReverse = [pygame.transform.flip(i, True, False) for i in self.anim]
        self.lenAnim = len(self.anim)
        self.animFrameTime = 24 // Game.settings["30_FPS"]
        self.xvel = 0
        self.yvel = 0
        self.left = False
        self.right = True
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.maskSurface = pygame.transform.scale(RessourceLoader.get(WormIceSprite.mask),
                                                  (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.maskSurface)
        self.CONSTMASK = self.mask
        self.maskSurfaceReverse = pygame.transform.flip(self.maskSurface, True, False)
        self.maskReverse = pygame.mask.from_surface(self.maskSurfaceReverse)
        self.CONSTHEIGT = self.height
        self.CONSTWIDTH = self.width
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.CONSTRECT2 = self.rect[2]
        self.CONSTRECT3 = self.rect[3]
        self.isJump = False
        self.gravityCount = 0
        self.gravity = 0
        self.lastx = 0
        self.lasty = 0
        self.securityTime = 60
        self.frameCount = 0
        self.maxvelocity = 2
        self.gravityModifier = 0
        self.big = False
        self.moveCount = 0

    def update(self):
        if not TileEditor.is_editing:
            from dpt.engine.tileManager import TileManager
            if not Game.freeze_game:

                Game.add_debug_info("Enemy.left = " + str(self.left))
                Game.add_debug_info("Enemy.right = " + str(self.right))

                if EffectsManagement.dico_current_effects["Slow"]:
                    self.maxvelocity = 1
                else:
                    self.maxvelocity = 2

                if EffectsManagement.dico_current_effects["lowGravity"]:
                    self.gravityModifier = 0.02
                else:
                    self.gravityModifier = 0

                if EffectsManagement.dico_current_effects["monsterimmortal"] and not self.big:
                    self.height = math.floor(self.height * 1.4)
                    self.width = math.floor(self.width * 1.4)
                    self.big = True
                    self.rect[2] //= 0.71
                    self.rect[3] //= 0.71
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                elif not EffectsManagement.dico_current_effects["monsterimmortal"]:
                    self.height = self.CONSTHEIGT
                    self.width = self.CONSTWIDTH
                    self.big = False
                    self.rect[2] = self.CONSTRECT2
                    self.rect[3] = self.CONSTRECT3
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

                if self.left:
                    if self.xvel > 0 and not EffectsManagement.dico_current_effects["Ice"]:
                        self.xvel = 0
                    if self.xvel > -self.maxvelocity * Game.DISPLAY_RATIO:
                        self.xvel -= (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.left = True
                    self.right = False
                elif self.right:
                    if self.xvel < 0 and not EffectsManagement.dico_current_effects["Ice"]:
                        self.xvel = 0
                    if self.xvel < self.maxvelocity * Game.DISPLAY_RATIO:
                        self.xvel += (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.left = False
                    self.right = True
                else:
                    self.xvel = 0

                self.lastx = self.rect.x

                if not (self.isJump and not EffectsManagement.dico_current_effects["Slow"]) or (EffectsManagement.dico_current_effects["Slow"] and self.frameCount % 3 == 0):
                    self.gravityCount += 1
                    self.gravity = math.floor((self.gravityCount ** 2) * (0.05 - self.gravityModifier) * Game.DISPLAY_RATIO) * -1
                    self.yvel = self.gravity
                    self.frameCount += 1
                else:
                    self.frameCount += 1

            self.securityTime -= 1
            if self.check_fall(TileManager.environment_group):
                self.left = not self.left
                self.right = not self.right

                if self.left:
                    self.xvel -= 1 * Game.DISPLAY_RATIO
                elif self.right:
                    self.xvel += 1 * Game.DISPLAY_RATIO

            self.maskcollide()

            self.rect.left += math.floor(self.xvel) * Game.settings["30_FPS"]
            self.rect.top -= math.floor(self.yvel) * Game.settings["30_FPS"]

            if self.lastx == self.rect.x:
                self.left = not self.left
                self.right = not self.right

            self.animation()

            self.check_void()

    def animation(self):
        if self.moveCount >= self.animFrameTime * self.lenAnim:
            self.moveCount = 0
        if self.left:
            self.mask = self.CONSTMASK
            self.image = self.anim[self.moveCount // self.animFrameTime]
        elif self.right:
            self.mask = self.maskReverse
            self.image = self.animReverse[self.moveCount // self.animFrameTime]

        self.moveCount += 1

    def check_void(self):
        if self.rect.top > 2000:
            self.kill()

    def kill(self):
        if not TileEditor.is_editing and not TileManager.is_loading_level:
            DeadBody(self.rect.x, self.rect.y, self.rect.width, self.rect.height, WormIceSprite.dead_texture, WormIceSprite.mask)
        pygame.sprite.Sprite.kill(self)

    def check_fall(self, platforms):
        if self.securityTime < 0:
            if self.right:
                neg = 1
            else:
                neg = -1
            self.rect.x += self.width * Game.DISPLAY_RATIO * neg
            self.rect.y += self.height * Game.DISPLAY_RATIO
            for i in platforms:
                if pygame.sprite.collide_rect(self, i):
                    self.rect.x -= self.width * Game.DISPLAY_RATIO * neg
                    self.rect.y -= self.height * Game.DISPLAY_RATIO
                    return False
            self.rect.x -= self.width * Game.DISPLAY_RATIO * neg
            self.rect.y -= self.height * Game.DISPLAY_RATIO
            self.securityTime = 60
            return True

    def maskcollide(self):
        for i in TileManager.environment_group:
            if i.rect.colliderect(Game.display_rect):
                rx = i.rect.x - (self.rect.x + math.floor(self.xvel) * Game.settings["30_FPS"])
                ry = i.rect.y - (self.rect.y - math.floor(self.yvel) * Game.settings["30_FPS"])

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
                                self.gravityCount = 0
                                self.isJump = False
                                self.frameCount = 0
                            break

                    crx = i.rect.x - self.rect.x
                    mask = self.mask.overlap_mask(i.mask, (crx, ry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.y < i.rect.y:
                            dy = rect.height + math.floor(self.yvel) * Game.settings["30_FPS"]
                            self.yvel = 0
                            self.gravityCount = 0
                            self.isJump = False
                            self.frameCount = 0
                        elif self.rect.y > i.rect.y:
                            dy = - rect.height + math.floor(self.yvel) * Game.settings["30_FPS"]
                            self.yvel = 0
                            self.isJump = False
                        break

                    self.rect.y -= dy

                    cry = (i.rect.y - self.rect.y)
                    mask = self.mask.overlap_mask(i.mask, (rx, cry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        Game.add_debug_info("dx = " + str(dx))
                        if self.rect.x > i.rect.x:
                            dx = rect.width + math.floor(self.xvel) * Game.settings["30_FPS"]
                            self.xvel = 0
                        elif self.rect.x < i.rect.x:
                            dx = - rect.width + math.floor(self.xvel) * Game.settings["30_FPS"]
                            self.xvel = 0
                        break

                    self.rect.x += dx
