import pygame


class CeciEstUnBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
