import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Cloud(pygame.sprite.Sprite):
    texture = "dpt.images.environment.background.Cloud_1_full"
    width = Game.TILESIZE + 75
    height = Game.TILESIZE
    i = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.interactible_blocks_group, TileManager.deadly_object_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.i == 8:
            self.i = 0
            self.image = RessourceLoader.get(self.texture)
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            self.rect.move_ip(-1, 0)
            self.rect.x -= 1
        else:
            self.i += 1
