#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.engine.gui.menu import Button
from dpt.engine.gui.menu.slide import Slide
from dpt.game import Game


class Slider(object):
    slide_group = pygame.sprite.Group()
    slider_list = []

    def __init__(self, x, y, width, height, value, **kwargs):
        """Crée une glissière

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type x: int
        :param width: Largeur
        :type width: int
        :param height: Hauteur
        :type height: int
        :param value: Valeur par défaut (relative)
        :type value: float

        :keyword image_left: Image du bouton de gauche
        :keyword image_left_pushed: Image du bouton de gauche une fois pressé
        :keyword image_right: Image du bouton de gauche
        :keyword image_right_pushed: Image du bouton de gauche une fois pressé
        :keyword image_slide: Image du bouton de glissière
        :keyword image_slide_pushed: Image du bouton de glissière une fois pressé
        :keyword image_progress_bar_frame: Image du cadre de la bar de progression
        :keyword image_progress_bar_bar: Image de la bar de progression

        :rtype: Slider
        """
        from dpt.engine.gui.menu.progressbar import ProgressBar
        Slider.slider_list.append(self)

        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height

        image_left = kwargs["image_left"]
        self.image_left = pygame.transform.smoothscale(image_left, (
            math.floor((image_left.get_rect().width / image_left.get_rect().height) * height), height))

        if "image_left_pushed" in kwargs:
            image_left_pushed = kwargs["image_left_pushed"]
            self.image_left_pushed = pygame.transform.smoothscale(image_left_pushed, (
                math.floor((image_left_pushed.get_rect().width / image_left_pushed.get_rect().height) * height),
                height))
        else:
            self.image_left_pushed = self.image_left

        self.left = Button(self.rect.x,
                           self.rect.y,
                           self.image_left.get_rect().width,
                           self.image_left.get_rect().height,
                           self.image_left,
                           pushed_image=self.image_left_pushed)

        image_right = kwargs["image_right"]
        self.image_right = pygame.transform.smoothscale(image_right, (
            math.floor((image_right.get_rect().width / image_right.get_rect().height) * height),
            height))

        if "image_right_pushed" in kwargs:
            image_right_pushed = kwargs["image_right_pushed"]
            self.image_right_pushed = pygame.transform.smoothscale(image_right_pushed, (
                math.floor((image_right_pushed.get_rect().width / image_right_pushed.get_rect().height) * height),
                height))
        else:
            self.image_right_pushed = self.image_right

        self.right = Button(self.rect.right - self.image_right.get_rect().width,
                            self.rect.y,
                            self.image_right.get_rect().width,
                            self.image_right.get_rect().height,
                            self.image_right,
                            pushed_image=self.image_right_pushed)

        image_slide = kwargs["image_slide"]
        self.image_slide = pygame.transform.smoothscale(image_slide, (
            math.floor((image_slide.get_rect().width / image_slide.get_rect().height) * height),
            height))

        if "image_slide_pushed" in kwargs:
            image_slide_pushed = kwargs["image_slide_pushed"]
            self.image_slide_pushed = pygame.transform.smoothscale(image_slide_pushed, (
                math.floor((image_slide_pushed.get_rect().width / image_slide_pushed.get_rect().height) * height),
                height))
        else:
            self.image_slide_pushed = self.image_slide

        if "image_progress_bar_frame" in kwargs:
            image_progress_bar_frame = kwargs["image_progress_bar_frame"]
            self.image_progress_bar_frame = pygame.transform.smoothscale(image_progress_bar_frame, (
                math.floor((self.rect.width - self.left.width - self.right.width)),
                height))
        else:
            self.image_progress_bar_frame = None

        try:
            image_progress_bar_bar = kwargs["image_progress_bar_bar"]
            self.image_progress_bar_bar = pygame.transform.smoothscale(image_progress_bar_bar, (
                math.floor((self.rect.width - self.left.width - self.right.width)),
                height))
        except KeyError:
            if self.image_progress_bar_frame is not None:
                raise
            else:
                self.image_progress_bar_bar = None

        if self.image_progress_bar_frame is not None:
            self.progress_bar = ProgressBar(x + self.left.width, y, self.image_progress_bar_frame.get_rect().width,
                                            self.height,
                                            self.image_progress_bar_frame, self.image_progress_bar_bar, 1)
        else:
            self.progress_bar = None

        self.slide = Slide(self, self.image_slide, self.image_slide_pushed)
        self.slide.rect.x = self.left.rect.right + (value * (self.right.rect.left - self.left.rect.right - self.slide.width))
        self.slide.apply_x()
        self.value = value
        Game.get_logger(__name__).debug("Slider created")

    def update(self):
        """Actualise la glissière"""
        self.right.update()
        self.left.update()
        self.slide.update()

        if self.right.pushed:
            self.slide.rect.x += math.floor(self.width * 0.03)
            self.slide.apply_x()
        elif self.left.pushed:
            self.slide.rect.x -= math.floor(self.width * 0.03)
            self.slide.apply_x()

        self.value = (self.slide.rect.x - self.left.rect.right) / (
                self.right.rect.left - self.left.rect.right - self.slide.width)
        if self.progress_bar is not None:
            self.progress_bar.value = self.value
        Game.add_debug_info("Slide: " + str(self.value))

    @classmethod
    def main_loop(cls):
        """Actualise toutes les glissières"""
        for slider in Slider.slider_list:
            slider.update()
            slider.draw(Game.surface)

    def kill(self):
        """Supprime la glissière"""
        self.right.kill()
        self.left.kill()
        self.slide.kill()

    def draw(self, surface):
        """Dessine la glissière"""
        surface.blit(self.right.image, self.right.rect)
        surface.blit(self.left.image, self.left.rect)
        surface.blit(self.slide.image, self.slide.rect)
