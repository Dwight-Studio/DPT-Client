import pygame

from dpt.game import Game


class Block(pygame.sprite.Sprite):
    game = Game.get_instance()

    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y