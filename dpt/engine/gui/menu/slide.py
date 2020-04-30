import pygame
import math

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Slide(pygame.sprite.Sprite):
    def __init__(self, slider, normal_image, pushed_image):
        """Crée un bouton de glissière

        :param slider: Glissière parente
        :type slider: dpt.engine.gui.menu.Slider
        :param normal_image: Image
        :type normal_image: pygame.Surface
        :param pushed_image: Image utilisée lorque le bouton est pressé
        :type pushed_image: pygame.Surface
        """

        from dpt.engine.gui.menu import Slider
        pygame.sprite.Sprite.__init__(self, Slider.slide_group)  # Sprite's constructor called
        self.slider = slider
        self.normal_image = normal_image
        self.pushed_image = pushed_image
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.width = math.floor(slider.height * (self.rect.width / self.rect.height))
        self.height = slider.height
        self.pushed_image = pygame.transform.smoothscale(self.pushed_image, (self.width, self.height))
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.slider.rect.centerx
        self.rect.centery = self.slider.rect.centery
        self.pushed = False

    def update(self):
        """Actualise le bouton de glissière"""
        prev = self.pushed
        self.pushed = False

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pushed = True

        if not prev and self.pushed:
            sound = RessourceLoader.get("dpt.sounds.sfx.switch6")
            sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            sound.play()

        if self.pushed:
            self.image = self.pushed_image
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x
            self.apply_x()
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                Game.cursor_on_button = True
            else:
                self.image = self.normal_image

    def apply_x(self):
        """Applique de modification en abscisse pour limiter son déplacement"""
        new_x = max(self.rect.x, self.slider.left.rect.right)
        new_x = min(new_x, self.slider.right.rect.left - self.rect.width)
        self.rect.x = new_x
