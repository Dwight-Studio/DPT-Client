import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class ButtonMechanic(pygame.sprite.Sprite):
    texture = "dpt.images.text.000_button_mechanic"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = math.floor(488 * Game.DISPLAY_RATIO)
    height = math.floor(436 * Game.DISPLAY_RATIO)
    offset_x = -(width // 2)
    offset_y = -(height // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
