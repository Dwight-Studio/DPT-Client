import math

import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Checkbox(pygame.sprite.Sprite):
    checkboxGroup = pygame.sprite.Group()

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.checkboxGroup)  # Sprite's constructor called
        self.false_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_OUT")
        self.true_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_IN")
        self.image = self.false_image
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.value = False

    def __bool__(self):
        return self.value

    def update(self):
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.value = not self.value

        if self.value:
            self.image = self.true_image
            self.update_rect()
            self.rect.x = self.x
            self.rect.y = self.y - 5
        else:
            self.image = self.false_image
            self.update_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.image = pygame.transform.scale(self.image, (math.floor(self.width * Game.DISPLAY_RATIO), math.floor(self.height * Game.DISPLAY_RATIO)))
