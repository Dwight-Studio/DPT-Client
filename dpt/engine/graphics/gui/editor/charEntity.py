import pygame
from dpt.game import Game


class CharEntity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = pygame.Surface((Game.TILESIZE, Game.TILESIZE))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = Game.surface.get_size()[0] / 2
        self.rect.y = Game.surface.get_size()[1] / 2
        self.xvel = 0
        self.yvel = 0
        self.width = Game.TILESIZE
        self.height = Game.TILESIZE

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.xvel > 0:
                self.xvel = 0
            if self.xvel > -16:
                self.xvel -= 16
            if self.rect.x < Game.surface.get_size()[0] / 2:
                self.xvel = 0
        elif keys[pygame.K_RIGHT]:
            if self.xvel < 0:
                self.xvel = 0
            if self.xvel < 16:
                self.xvel += 16
        else:
            self.xvel = 0
        self.rect.left += self.xvel
