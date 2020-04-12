import math
import pygame
from dpt.engine.gui.menu.bar import Bar
from dpt.game import Game


class ProgressBar(pygame.sprite.Sprite):
    progressbarGroup = pygame.sprite.Group()

    def __init__(self, x, y, width, height, image, image2, max_value):
        pygame.sprite.Sprite.__init__(self, self.progressbarGroup)  # Sprite's constructor called
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.bar = Bar(x, y, width, height, image2)
        self.max_value = max_value
        self.value = 0

    def update(self):
        if self.value > self.max_value:
            self.value = self.max_value

        Game.add_debug_info(str(self.bar.progress))
        self.bar.progress = math.floor(self.width * (self.value / self.max_value))
