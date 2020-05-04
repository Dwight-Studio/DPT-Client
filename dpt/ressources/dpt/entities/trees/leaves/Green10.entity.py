import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Green10(pygame.sprite.Sprite):
    texture = "dpt.images.environment.plants.trees.Tree_Leaves_Green_10"
    sounds = "dpt.sounds.sfx.sfx_leaves"
    width = height = math.floor(208 / 748 * Game.TILESIZE)
    offset_x = -(width // 2)
    offset_y = -(height // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
