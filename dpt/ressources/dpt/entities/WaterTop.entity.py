import math

import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class WaterTop(pygame.sprite.Sprite):
    texture = "dpt.images.environment.liquids.Water_Tile_Top"
    textures = "dpt.images.environment.liquids.Water_Tile_Top_*"
    screen_width, screen_height = Game.surface.get_size()
    width = Game.TILESIZE
    height = math.floor(Game.TILESIZE * (116 / 208))
    offset_x = 0
    offset_y = Game.TILESIZE - height

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group,
                                      TileManager.foreground_blocks_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(
            self.textures)]
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y

    def update(self):
        self.animation()

    def animation(self):
        self.image = self.frames[Game.anim_count_water // 4]
