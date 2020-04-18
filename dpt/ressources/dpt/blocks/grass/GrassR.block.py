import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class GrassR(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Grass_Tile_Flat_r"
    width = height = Game.TILESIZE
    offset_x = 0
    offset_y = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.environment_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        pygame.mixer_music.load(Game.ROOT_DIRECTORY + "/ressources/dpt/sounds/sfx/sfx_grass.ogg")
        pygame.mixer_music.play()