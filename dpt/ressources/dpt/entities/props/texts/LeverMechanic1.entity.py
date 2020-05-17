import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class LeverMechanic1(pygame.sprite.Sprite):
    texture = "dpt.images.text.lever_mechanic_1"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = Game.TILESIZE
    height = Game.TILESIZE
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
