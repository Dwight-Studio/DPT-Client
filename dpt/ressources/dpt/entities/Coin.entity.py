import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Coin(pygame.sprite.Sprite):
    texture = "dpt.images.environment.coins.00"
    textures = "dpt.images.environment.coins.*"
    screen_width, screen_height = Game.surface.get_size()
    width = Game.TILESIZE // 2
    height = Game.TILESIZE // 2
    offset_x = Game.TILESIZE // 4
    offset_y = Game.TILESIZE // 4

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entityGroup)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = RessourceLoader.get_multiple(self.textures)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.animCount = 0

    def update(self):
        self.animation()
        self.collide()

    def animation(self):
        if self.animCount + 1 >= 144:
            self.animCount = 0
        else:
            self.animCount += 1

        self.image = self.frames[self.animCount // 4]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def collide(self):
        for i in Game.playerGroup:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                del self
                return
