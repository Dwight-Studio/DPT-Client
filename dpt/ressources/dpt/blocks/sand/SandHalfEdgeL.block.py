import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class SandHalfEdgeL(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Sand_Tile_Half_Round_L-01"
    width = Game.TILESIZE
    height = Game.TILESIZE // 2
    offset_x = 0
    offset_y = height

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.environmentGroup)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y