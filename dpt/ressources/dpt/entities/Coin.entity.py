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
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(
            self.textures)]
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.animCount = 0

    def update(self):
        self.animation()
        self.collide()

    def animation(self):
        self.image = self.frames[Game.anim_count_coins // 4]

    def collide(self):
        for i in Game.player_group:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                del self
                return
