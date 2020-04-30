import math
import pygame
from dpt.engine.gui.menu.bar import Bar
from dpt.game import Game


class ProgressBar(pygame.sprite.Sprite):
    progress_bar_group = pygame.sprite.Group()
    bar_group = pygame.sprite.Group()

    def __init__(self, x, y, width, height, image, image2, max_value):
        """Crée une barre de progression

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int
        :param width: Largeur
        :type width: int
        :param height: Hauteur
        :type height: int
        :param image: Image du cadre
        :type image: pygame.Surface
        :param image2: Image de la barre
        :type image2: pygame.Surface
        :param max_value: Valeur maximale de la barre
        :type max_value: float

        :rtype: ProgressBar
        """
        pygame.sprite.Sprite.__init__(self, self.progress_bar_group)  # Sprite's constructor called
        self.width = width
        self.height = height
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bar = Bar(x, y, width, height, image2)
        self.max_value = max_value
        self.value = 0
        Game.get_logger("ProgressBar").debug("ProgressBar created")

    def update(self):
        """Actualise la barre de progression"""
        if self.value > self.max_value:
            self.value = self.max_value
        self.bar.progress = max(math.floor(self.width * (self.value / self.max_value)), 0)

    @classmethod
    def main_loop(cls):
        """Actualise toutes les barres de progression"""
        ProgressBar.progress_bar_group.update()
        ProgressBar.bar_group.update()
        ProgressBar.bar_group.draw(Game.surface)
        ProgressBar.progress_bar_group.draw(Game.surface)
