import math

import pygame

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.effectsManagement import EffectsManagement
from dpt.engine.tileManager import TileManager
from dpt.game import Game


class BeeSprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.animals.Bee_1"
    textures = "dpt.images.characters.animals.Bee*"
    width = math.floor(112.8 * Game.DISPLAY_RATIO)
    height = math.floor(72 * Game.DISPLAY_RATIO)
    offset_x = (Game.TILESIZE - width) // 2
    offset_y = (Game.TILESIZE - height) // 2
    mask = "dpt.images.characters.animals.beeMask"

    preview_surface = None

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemy_group, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.anim = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(self.textures)]
        self.animReverse = [pygame.transform.flip(i, True, False) for i in self.anim]
        self.xvel = 0
        self.yvel = 0
        self.left = False
        self.right = True
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.maskSurface = pygame.transform.scale(RessourceLoader.get(BeeSprite.mask),
                                                  (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.maskSurface)
        self.CONSTHEIGT = self.height
        self.CONSTWIDTH = self.width
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.CONSTRECT2 = self.rect[2]
        self.CONSTRECT3 = self.rect[3]
        self.lastx = 0
        self.lasty = 0
        self.maxvelocity = 2
        self.big = False
        self.distance = 0
        self.cosx = 0
        self.horizontalStart = self.rect.top
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
                    if self.xvel > 0:
                        self.xvel = 0
                    if self.xvel > -self.maxvelocity * Game.DISPLAY_RATIO:
                        self.xvel -= (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.left = True
                    self.right = False
                elif self.right:
                    if self.xvel < 0:
                        self.xvel = 0
                    if self.xvel < self.maxvelocity * Game.DISPLAY_RATIO:
                        self.xvel += (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.left = False
                    self.right = True
                else:
                    self.xvel = 0

            self.lastx = self.rect.x

            self.yvel = math.floor(math.cos(self.cosx) * 20 * Game.DISPLAY_RATIO) - math.floor(math.cos(self.cosx - 0.05) * 20 * Game.DISPLAY_RATIO)
            self.maskcollide()

            self.distance += abs(self.xvel)
            self.rect.top += self.yvel
            self.rect.left += math.floor(self.xvel)

            self.cosx += 0.05
            if self.cosx >= math.pi * 2:
                self.cosx = 0
                self.rect.top = self.horizontalStart

            self.animation()

            if self.lastx == self.rect.x:
                self.left = not self.left
                self.right = not self.right
                self.distance = 1200 - self.distance

            if self.distance > 1200 * Game.DISPLAY_RATIO:
                self.distance = 0
                self.left = not self.left
                self.right = not self.right
        else:
            self.preview()

    def animation(self):
        if self.moveCount >= 32:
            self.moveCount = 0
        if self.left:
            self.image = self.anim[self.moveCount // 8]
        elif self.right:
            self.image = self.animReverse[self.moveCount // 8]
        self.moveCount += 1

    def preview(self):
        if BeeSprite.preview_surface is not None:
            Game.surface.blit(BeeSprite.preview_surface, (self.rect.x - TileManager.camera.last_x, self.rect.y - math.floor(50 * Game.DISPLAY_RATIO)))
        else:
            BeeSprite.preview_surface = pygame.surface.Surface((1200, 100)).convert_alpha()
            BeeSprite.preview_surface.fill((0, 0, 0, 0))

            self.distance = 0
            self.cosx = 0
            x = BeeSprite.width // 2
            y = BeeSprite.height // 2 + 50
            while self.distance < 1200 * Game.DISPLAY_RATIO:
                if self.xvel < self.maxvelocity * Game.DISPLAY_RATIO:
                    self.xvel += (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                self.distance += abs(self.xvel)
                y += math.floor(math.cos(self.cosx) * 20 * Game.DISPLAY_RATIO) - math.floor(math.cos(self.cosx - 0.05) * 20 * Game.DISPLAY_RATIO)
                x += math.floor(self.xvel)
                self.cosx += 0.05
                if self.cosx >= math.pi * 2:
                    self.cosx = 0
                    y = 50 + BeeSprite.height // 2
                pygame.draw.rect(BeeSprite.preview_surface, (193, 39, 45), (x, y, 5, 5))
                BeeSprite.preview_surface = pygame.transform.scale(BeeSprite.preview_surface, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
                Game.surface.blit(BeeSprite.preview_surface, (self.rect.x - TileManager.camera.last_x, self.rect.y - math.floor(50 * Game.DISPLAY_RATIO)))

    def maskcollide(self):
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
                            break

                    crx = i.rect.x - self.rect.x
                    mask = self.mask.overlap_mask(i.mask, (crx, ry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.y < i.rect.y:
                            dy = rect.height + math.floor(self.yvel)
                            self.yvel = 0
                        elif self.rect.y > i.rect.y:
                            dy = - rect.height + math.floor(self.yvel)
                            self.yvel = 0
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
