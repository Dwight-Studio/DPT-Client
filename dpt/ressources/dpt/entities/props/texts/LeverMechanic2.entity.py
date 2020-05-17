import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class LeverMechanic2(pygame.sprite.Sprite):
    texture = "dpt.images.text.000_lever_mechanic_2"
    sounds = "dpt.sounds.sfx.sfx_stone"
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
