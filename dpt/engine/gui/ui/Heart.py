import math
import pygame
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager


class Heart(pygame.sprite.Sprite):
    """Vie du joueur"""
    full_heart = "dpt.images.gui.ui.UI_HEART_FULL"
    half_heart = "dpt.images.gui.ui.UI_HEART_HALF"
    empty_heart = "dpt.images.gui.ui.UI_HEART_EMPTY"

    def __init__(self):
        """Crée un cœur qui se place en bas à droite"""
        pygame.sprite.Sprite.__init__(self, TileManager.heart_group)
        self.full_heart = pygame.transform.smoothscale(RessourceLoader.get(Heart.full_heart), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.half_heart = pygame.transform.smoothscale(RessourceLoader.get(Heart.half_heart), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.empty_heart = pygame.transform.smoothscale(RessourceLoader.get(Heart.empty_heart), (math.floor(100 * Game.DISPLAY_RATIO), math.floor(100 * Game.DISPLAY_RATIO)))
        self.draw = {1: self.full_heart,
                     2: self.half_heart,
                     3: self.empty_heart}
        self.image = self.full_heart
        self.rect = [Game.WINDOW_WIDTH - 100 * Game.DISPLAY_RATIO, Game.WINDOW_HEIGHT - 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO, 100 * Game.DISPLAY_RATIO]

    def update(self):
        """Change le cœur en fonction de la vie du joueur"""
        todraw = self.draw[Game.life]
        self.image = todraw
        Game.surface.blit(self.image, self.rect)
