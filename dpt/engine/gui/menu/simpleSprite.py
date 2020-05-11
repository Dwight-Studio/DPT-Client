import math
import pygame

from dpt.engine.gui.menu.button import Button


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, image, **kwargs):
        """Crée un sprite (simple image dessinée)

        :param width: Largeur
        :type width: int
        :param height: Hauteur
        :type height: int
        :param image: Image
        :type image: pygame.Surface

        :keyword x: Abscisse
        :keyword y: Ordonnée
        :keyword centerx: Abscisse centrée
        :keyword centery: Ordonnée centrée

        :rtype: SimpleSprite
        """
        pygame.sprite.Sprite.__init__(self, Button.text_sprite_buttonsGroup)  # Sprite's constructor called
        self.image = image
        self.width = math.floor(width)
        self.height = math.floor(height)
        self.image = pygame.transform.smoothscale(self.image, (math.floor(width),
                                                               math.floor(height)))
        self.rect = self.image.get_rect()

        if "x" in kwargs:
            self.rect.x = kwargs["x"]

        if "y" in kwargs:
            self.rect.y = kwargs["y"]

        if "centerx" in kwargs:
            self.rect.centerx = kwargs["centerx"]

        if "centery" in kwargs:
            self.rect.centerx = kwargs["centery"]
