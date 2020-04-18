import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class GrassSlopeConnectorL(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Grass_Tile_Slope_Connector_l"
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
        if not TileManager.loadlevel:
            pygame.mixer_music.set_volume(0.5)
            pygame.mixer_music.load(Game.ROOT_DIRECTORY + "/ressources/dpt/sounds/sfx/sfx_grass.ogg")
            pygame.mixer_music.play()