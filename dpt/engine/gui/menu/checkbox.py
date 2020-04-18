import math

import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Checkbox(pygame.sprite.Sprite):
    checkboxGroup = pygame.sprite.Group()

    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self, self.checkboxGroup)  # Sprite's constructor called
        self.false_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_OUT").copy()
        self.true_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_IN").copy()
        self.image = self.false_image
        self.size = size
        self.rect = self.image.get_rect()
        self.width = math.floor(self.rect.width * self.size * Game.DISPLAY_RATIO)
        self.height = math.floor(self.rect.height * self.size * Game.DISPLAY_RATIO)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        del self.rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.value = False
        Game.get_logger("Checkbox").debug("Checkbox created")

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
            self.rect.y = math.floor(self.y - 5 * self.size * Game.DISPLAY_RATIO)
        else:
            self.image = self.false_image
            self.update_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.image = pygame.transform.smoothscale(self.image, (
        math.floor(self.width * Game.DISPLAY_RATIO), math.floor(self.height * Game.DISPLAY_RATIO)))

    @classmethod
    def main_loop(cls):
        Checkbox.checkboxGroup.update()
        Checkbox.checkboxGroup.draw(Game.surface)
