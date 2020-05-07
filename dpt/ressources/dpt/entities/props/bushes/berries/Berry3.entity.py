import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Berry3(pygame.sprite.Sprite):
    texture = "dpt.images.environment.plants.Berry_3"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = Game.TILESIZE // 4
    height = Game.TILESIZE // 4
    offset_x = -(Game.TILESIZE // 4)
    offset_y = -(Game.TILESIZE // 4)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
