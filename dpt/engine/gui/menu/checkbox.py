import math
import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Checkbox(pygame.sprite.Sprite):
    checkbox_group = pygame.sprite.Group()

    def __init__(self, x, y, size):
        """Crée une case à cocher

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int
        :param size: Taille (relative)
        :type size: float

        :rtype: Checkbox
        """
        pygame.sprite.Sprite.__init__(self, self.checkbox_group)  # Sprite's constructor called
        self.false_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_OUT").copy()
        self.true_image = RessourceLoader.get("dpt.images.gui.Buttons.BTN_CHECKBOX_IN").copy()
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
        Game.get_logger(__name__).debug("Checkbox created")

    def __bool__(self):
        return self.value

    def update(self):
        """Actualise la case à cocher"""
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.value = not self.value
                    sound = RessourceLoader.get("dpt.sounds.sfx.switch6")
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()

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
        """Actualise le rectange"""
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.image = pygame.transform.smoothscale(self.image, (
        math.floor(self.width * Game.DISPLAY_RATIO), math.floor(self.height * Game.DISPLAY_RATIO)))

    @classmethod
    def main_loop(cls):
        """Actualise toutes les cases à cocher"""
        Checkbox.checkbox_group.update()
        Checkbox.checkbox_group.draw(Game.surface)
