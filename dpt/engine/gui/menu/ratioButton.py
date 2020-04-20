import math
import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class RatioButton(pygame.sprite.Sprite):
    ratio_button_group = pygame.sprite.Group()

    def __init__(self, x, y, size, btn_list):
        pygame.sprite.Sprite.__init__(self, self.ratio_button_group)  # Sprite's constructor called
        self.false_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_RADIO_OUT").copy()
        self.true_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_RADIO_IN").copy()
        self.image = self.false_image
        self.size = size
        self.rect = self.image.get_rect()
        self.width = math.floor(self.rect.width * self.size * Game.DISPLAY_RATIO)
        self.height = math.floor(self.rect.height * self.size * Game.DISPLAY_RATIO)
        self.true_image = pygame.transform.smoothscale(self.true_image, (self.width, self.height))
        self.false_image = pygame.transform.smoothscale(self.false_image, (self.width, self.height))
        del self.rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.value = False
        self.list = btn_list
        self.list.append(self)
        Game.get_logger("RatioButton").debug("RatioButton created")

    def __bool__(self):
        return self.value

    def update(self):
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    for btn in self.list:
                        btn.value = False
                        self.value = True

        if self.value:
            self.image = self.true_image
        else:
            self.image = self.false_image

    @classmethod
    def main_loop(cls):
        RatioButton.ratio_button_group.update()
        RatioButton.ratio_button_group.draw(Game.surface)