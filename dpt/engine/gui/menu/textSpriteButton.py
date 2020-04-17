import math
import pygame
from dpt.engine.gui.menu.button import Button
from dpt.game import Game


class TextSpriteButton(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        pygame.sprite.Sprite.__init__(self, Button.text_sprite_buttonsGroup)  # Sprite's constructor called
        self.image = image
        self.width = math.floor(width * Game.DISPLAY_RATIO)
        self.height = math.floor(height * Game.DISPLAY_RATIO)
        self.image = pygame.transform.scale(self.image, (math.floor(width * Game.DISPLAY_RATIO),
                                                         math.floor(height * Game.DISPLAY_RATIO)))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
