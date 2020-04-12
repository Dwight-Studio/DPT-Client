import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class SnowLower(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Snow_Tile"
    width = height = Game.TILESIZE

    def __init__(self, x, y):
        from dpt.engine.graphics.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.environmentGroup)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
