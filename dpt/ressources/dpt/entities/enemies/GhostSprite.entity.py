import math

import pygame

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.effectsManagement import EffectsManagement
from dpt.game import Game


class GhostSprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.player.standing"
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
        self.up = False
        self.down = True
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
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

    def update(self):
        if not TileEditor.is_editing:
            from dpt.engine.tileManager import TileManager
            if not Game.freeze_game:

                Game.add_debug_info("Enemy.left = " + str(self.up))
                Game.add_debug_info("Enemy.right = " + str(self.down))

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

                if self.up:
                    if self.yvel > 0:
                        self.yvel = 0
                    if self.yvel > -self.maxvelocity * Game.DISPLAY_RATIO:
                        self.yvel -= (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.up = True
                    self.down = False
                elif self.down:
                    if self.yvel < 0:
                        self.yvel = 0
                    if self.yvel < self.maxvelocity * Game.DISPLAY_RATIO:
                        self.yvel += (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.up = False
                    self.down = True
                else:
                    self.yvel = 0

            self.distance += abs(self.yvel)
            self.rect.top += math.floor(self.yvel)

            self.animation()

            if self.distance > 500 * Game.DISPLAY_RATIO:
                self.distance = 0
                self.up = not self.up
                self.down = not self.down

    def animation(self):
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)
        pass