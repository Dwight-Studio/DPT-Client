import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Cloud(pygame.sprite.Sprite):
    textures = "dpt.images.environment.background.Cloud_full_*"
    i = 0

    def __init__(self, x, y, speed):
        """Crée un nuage

        :param x: Abscice
        :type x: int
        :param y: Ordonnée
        :type y: int
        :param speed: Vitesse
        :type speed: int
        """
        from dpt.engine.tileManager import TileManager
        from random import choice
        import math

        pygame.sprite.Sprite.__init__(self, TileManager.clouds_group)
        self.image = choice(RessourceLoader.get_multiple(self.textures))
        self.rect = self.image.get_rect()

        self.height = Game.TILESIZE
        self.width = math.floor(Game.TILESIZE * (self.rect.width / self.rect.height))

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Déplace le nugae de speed par frame"""
        self.rect.move_ip(-self.speed, 0)
