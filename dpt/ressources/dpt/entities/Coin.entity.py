import pygame
import math

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Coin(pygame.sprite.Sprite):
    texture = "dpt.images.environment.coins.00"
    textures = "dpt.images.environment.coins.*"
    screen_width, screen_height = Game.surface.get_size()

    def __init__(self, x, y, width, height, alpha):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = RessourceLoader.get_multiple(self.textures)
        self.image.set_alpha(alpha)
        self.alpha = alpha
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.animCount = 0

    def update(self):
        from dpt.engine.graphics.tileManager import TileManager
        self.animation()
        self.collide()
        self.image.set_alpha(self.alpha)

    def animation(self):
        if self.animCount + 1 >= 72:
            self.animCount = 0
        else:
            self.animCount += 1

        self.image = self.frames[self.animCount//2]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def collide(self):
        for i in Game.playerGroup:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                del self
                return
