import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class SnowEdgeA(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Snow_Tile_Flat_Edge_a"

    def __init__(self, x, y, width, height, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
