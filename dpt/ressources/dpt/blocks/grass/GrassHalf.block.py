import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class GrassHalf(pygame.sprite.Sprite):
    texture = "dpt.images.environment.terrain.Grass_Tile_Half_Flat-01"
    sounds = "dpt.sounds.sfx.sfx_grass"
    width = Game.TILESIZE
    height = Game.TILESIZE // 2
    offset_x = 0
    offset_y = height

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.environment_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.loadlevel:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image)
