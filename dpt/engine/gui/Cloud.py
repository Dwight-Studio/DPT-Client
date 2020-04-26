import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Cloud(pygame.sprite.Sprite):
    texture = "dpt.images.environment.background.Cloud_1_full"
    width = Game.TILESIZE + 75
    height = Game.TILESIZE
    i = 0

    def __init__(self, x, y, speed=1):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.clouds_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.i == 3:
            self.i = 0
            self.image = RessourceLoader.get(self.texture)
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            self.rect.move_ip(self.speed, 0)
        else:
            self.i += 1
