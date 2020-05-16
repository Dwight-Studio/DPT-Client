import math
import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class ParallaxSky:
    bg = None
    images = None
    reversed_images = None
    plains = "dpt.images.environment.background.plains.*"
    ice = "dpt.images.environment.background.ice.*"
    goop = "dpt.images.environment.background.goop.*"
    desert = "dpt.images.environment.background.desert.*"
    gap_0 = 0
    gap_1 = 0
    gap_2 = 0
    enable_reversed = False

    @classmethod
    def init(cls, texture):
        if texture == "Ice":
            cls.images = [pygame.transform.smoothscale(i, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)) for i in RessourceLoader.get_multiple(ParallaxSky.ice)]
            cls.reversed_images = [pygame.transform.flip(i, True, False) for i in cls.images]
        elif texture == "Desert":
            cls.images = [pygame.transform.smoothscale(i, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)) for i in RessourceLoader.get_multiple(ParallaxSky.desert)]
            cls.reversed_images = [pygame.transform.flip(i, True, False) for i in cls.images]
        elif texture == "Goop":
            cls.images = [pygame.transform.smoothscale(i, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)) for i in RessourceLoader.get_multiple(ParallaxSky.goop)]
            cls.reversed_images = [pygame.transform.flip(i, True, False) for i in cls.images]
        else:
            cls.images = [pygame.transform.smoothscale(i, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)) for i in RessourceLoader.get_multiple(ParallaxSky.plains)]
            cls.reversed_images = [pygame.transform.flip(i, True, False) for i in cls.images]
        cls.bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
        cls.bg = pygame.transform.smoothscale(cls.bg, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))

        cls.gap_0 = 0
        cls.gap_1 = 0
        cls.gap_2 = 0

    @classmethod
    def update(cls):
        Game.surface.blit(cls.bg, (0, 0))

        cls.gap_0 = abs(math.ceil((TileManager.camera.last_x // 9) / Game.WINDOW_WIDTH) * Game.WINDOW_WIDTH)
        cls.gap_0_rel = abs(math.ceil((TileManager.camera.last_x // 9) / Game.WINDOW_WIDTH))

        cls.gap_1 = abs(math.ceil((TileManager.camera.last_x // 6) / Game.WINDOW_WIDTH) * Game.WINDOW_WIDTH)
        cls.gap_1_rel = abs(math.ceil((TileManager.camera.last_x // 6) / Game.WINDOW_WIDTH))

        cls.gap_2 = abs(math.ceil((TileManager.camera.last_x // 3) / Game.WINDOW_WIDTH) * Game.WINDOW_WIDTH)
        cls.gap_2_rel = abs(math.ceil((TileManager.camera.last_x // 3) / Game.WINDOW_WIDTH))

        if cls.enable_reversed:
            if -TileManager.camera.last_x > 0:
                if cls.gap_0_rel % 2 == 0:
                    Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                    Game.surface.blit(cls.reversed_images[0], ((TileManager.camera.last_x // 9) + Game.WINDOW_WIDTH + cls.gap_0, 0))
                else:
                    Game.surface.blit(cls.reversed_images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                    Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + Game.WINDOW_WIDTH + cls.gap_0, 0))

                if cls.gap_1_rel % 2 == 0:
                    Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                    Game.surface.blit(cls.reversed_images[1], ((TileManager.camera.last_x // 6) + Game.WINDOW_WIDTH + cls.gap_1, 0))
                else:
                    Game.surface.blit(cls.reversed_images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                    Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + Game.WINDOW_WIDTH + cls.gap_1, 0))

                if cls.gap_2_rel % 2 == 0:
                    Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                    Game.surface.blit(cls.reversed_images[2], ((TileManager.camera.last_x // 3) + Game.WINDOW_WIDTH + cls.gap_2, 0))
                else:
                    Game.surface.blit(cls.reversed_images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                    Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + Game.WINDOW_WIDTH + cls.gap_2, 0))
            elif -TileManager.camera.last_x < 0:
                if cls.gap_0_rel % 2 == 0:
                    Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                    Game.surface.blit(cls.reversed_images[0], ((TileManager.camera.last_x // 9) - Game.WINDOW_WIDTH + cls.gap_0, 0))
                else:
                    Game.surface.blit(cls.reversed_images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                    Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) - Game.WINDOW_WIDTH + cls.gap_0, 0))

                if cls.gap_1_rel % 2 == 0:
                    Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                    Game.surface.blit(cls.reversed_images[1], ((TileManager.camera.last_x // 6) - Game.WINDOW_WIDTH + cls.gap_1, 0))
                else:
                    Game.surface.blit(cls.reversed_images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                    Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) - Game.WINDOW_WIDTH + cls.gap_1, 0))

                if cls.gap_2_rel % 2 == 0:
                    Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                    Game.surface.blit(cls.reversed_images[2], ((TileManager.camera.last_x // 3) - Game.WINDOW_WIDTH + cls.gap_2, 0))
                else:
                    Game.surface.blit(cls.reversed_images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                    Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) - Game.WINDOW_WIDTH + cls.gap_2, 0))
            else:
                if cls.gap_0_rel % 2 == 0:
                    Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                else:
                    Game.surface.blit(cls.reversed_images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))

                if cls.gap_1_rel % 2 == 0:
                    Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                else:
                    Game.surface.blit(cls.reversed_images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))

                if cls.gap_2_rel % 2 == 0:
                    Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                else:
                    Game.surface.blit(cls.reversed_images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
        else:
            if -TileManager.camera.last_x > 0:
                Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + Game.WINDOW_WIDTH + cls.gap_0, 0))

                Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + Game.WINDOW_WIDTH + cls.gap_1, 0))

                Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + Game.WINDOW_WIDTH + cls.gap_2, 0))

            elif -TileManager.camera.last_x < 0:
                Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))
                Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) - Game.WINDOW_WIDTH + cls.gap_0, 0))

                Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))
                Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) - Game.WINDOW_WIDTH + cls.gap_1, 0))

                Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
                Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) - Game.WINDOW_WIDTH + cls.gap_2, 0))
            else:
                Game.surface.blit(cls.images[0], ((TileManager.camera.last_x // 9) + cls.gap_0, 0))

                Game.surface.blit(cls.images[1], ((TileManager.camera.last_x // 6) + cls.gap_1, 0))

                Game.surface.blit(cls.images[2], ((TileManager.camera.last_x // 3) + cls.gap_2, 0))
