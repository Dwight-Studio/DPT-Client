import math

import pygame

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.effectsManagement import EffectsManagement
from dpt.game import Game


class BeeSprite(pygame.sprite.Sprite):
    texture = "dpt.images.characters.player.standing"
    screen_width, screen_height = (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
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
        self.cosx = 0

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

            self.rect.left += math.floor(self.xvel)
            self.distance += abs(self.xvel)
            self.rect.top += math.floor(math.cos(self.cosx) * 20 * Game.DISPLAY_RATIO)
            self.cosx += 0.05

            self.animation()

            if self.distance > 1200 * Game.DISPLAY_RATIO:
                self.distance = 0
                self.left = not self.left
                self.right = not self.right

    def animation(self):
        # pygame.draw.rect(Game.surface, (255, 0, 0), self.rect, 2)
        pass
