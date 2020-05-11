import math
import pygame
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class Inversion(pygame.sprite.Sprite):
    """Effet inversion"""
    inversion = "dpt.images.effects.inversion"

    def __init__(self):
        """Crée l'effet inversion"""
        pygame.sprite.Sprite.__init__(self, TileManager.effects_group)
        self.full_heart = pygame.transform.smoothscale(RessourceLoader.get(Inversion.inversion), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.image = self.full_heart
        self.rect = [0, 970 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO]

    def update(self):
        """Affiche l'effet"""
        Game.surface.blit(self.image, self.rect)
