import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class SnowEdgeL(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Snow_Tile_Flat_Edge_l"
    def __init__(self, x, y, width, height, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (Game.TILESIZE, Game.TILESIZE))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height