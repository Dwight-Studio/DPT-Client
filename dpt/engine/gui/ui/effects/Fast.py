import pygame
import math
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class Fast(pygame.sprite.Sprite):
    fast = "dpt.images.effects.fast"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, TileManager.effects_group)
        self.full_heart = pygame.transform.smoothscale(RessourceLoader.get(Fast.fast), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.image = self.full_heart
        self.rect = [0, 970 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO]

    def update(self):
        Game.surface.blit(self.image, self.rect)
