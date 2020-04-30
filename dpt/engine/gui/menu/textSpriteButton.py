import math
import pygame
from dpt.engine.gui.menu.button import Button
from dpt.game import Game


class TextSpriteButton(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        """Crée un sprite (simple image dessinée)

        :param width: Largeur
        :type width: int
        :param height: Hauteur
        :type height: int
        :param image: Image
        :type image: pygame.Surface

        :rtype: TextSpriteButton
        """
        pygame.sprite.Sprite.__init__(self, Button.text_sprite_buttonsGroup)  # Sprite's constructor called
        self.image = image
        self.width = math.floor(width)
        self.height = math.floor(height)
        self.image = pygame.transform.smoothscale(self.image, (math.floor(width),
                                                               math.floor(height)))
        self.rect = self.image.get_rect()
