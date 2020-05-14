import math
import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class ParallaxSky:
    bg = None
    images = None
    plains = "dpt.images.environment.background.plains.*"

    @classmethod
    def init(cls):
        cls.plains_surfaces = [pygame.transform.smoothscale(i, (Game.SCREEN_WIDTH, Game.WINDOW_HEIGHT)) for i in RessourceLoader.get_multiple(ParallaxSky.plains)]

        cls.images = cls.plains_surfaces
        cls.bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
        cls.bg = pygame.transform.smoothscale(cls.bg, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))

    @classmethod
    def update(cls):
        Game.surface.blit(cls.bg, (0, 0))

        Game.surface.blit(cls.images[1], (TileManager.camera.last_x // 2, 0))

        if Game.player_sprite.right:
            Game.surface.blit(cls.images[0], (-TileManager.camera.last_x, 0))
            Game.surface.blit(cls.images[0], (-TileManager.camera.last_x + Game.SCREEN_WIDTH, 0))

            Game.surface.blit(cls.images[1], ((-TileManager.camera.last_x // 4) + Game.SCREEN_WIDTH, 0))
            Game.surface.blit(cls.images[1], (-TileManager.camera.last_x // 4, 0))

            Game.surface.blit(cls.images[2], ((-TileManager.camera.last_x // 8) + Game.SCREEN_WIDTH, 0))
            Game.surface.blit(cls.images[2], (-TileManager.camera.last_x // 8, 0))
        else:
            Game.surface.blit(cls.images[0], (-TileManager.camera.last_x, 0))
            Game.surface.blit(cls.images[0], (-TileManager.camera.last_x - Game.SCREEN_WIDTH, 0))

            Game.surface.blit(cls.images[1], ((-TileManager.camera.last_x // 4) - Game.SCREEN_WIDTH, 0))
            Game.surface.blit(cls.images[1], (-TileManager.camera.last_x // 4, 0))

            Game.surface.blit(cls.images[2], ((-TileManager.camera.last_x // 8) - Game.SCREEN_WIDTH, 0))
            Game.surface.blit(cls.images[2], (-TileManager.camera.last_x // 8, 0))
