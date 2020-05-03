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
        from dpt.engine.tileManager import TileManager
        import math

        pygame.sprite.Sprite.__init__(self)

        self.image = choice(RessourceLoader.get_multiple(self.textures)).copy()
        self.rect = self.image.get_rect()

        self.height = Game.TILESIZE
        self.width = math.floor(Game.TILESIZE * (self.rect.width / self.rect.height))

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.layer = 5 - speed
        brightness = math.floor(speed * (30 / 5))
        self.image.fill((brightness, brightness, brightness), special_flags=pygame.BLEND_RGB_SUB)
        self.count = 0
        self.rect.x = x
        self.rect.y = y

        TileManager.clouds_group.add(self, layer=self.layer)

    def update(self):
        """Déplace le nuage"""
        if self.count == self.speed:
            self.rect.x -= 1
            self.count = 0
        self.count += 1
