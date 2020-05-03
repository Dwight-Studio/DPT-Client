import pygame
import math

from dpt.engine.gui.menu.window_item import WindowItem
from dpt.game import Game


class Window:
    window_list = []

    def __init__(self, x, y, width_number, height_number, **kwargs):
        """Crée une fenêtre

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type x: int
        :param width_number: Largeur (en nombre de sprites)
        :type width_number: int
        :param height_number: Hauteur (en nombre de sprites)
        :type height_number: int

        :keyword centerx: Abscisse du centre, si specifié, ignore le paramètre x original
        :keyword centery: ordonnée du centre, si specifié, ignore le paramètre y original

        :rtype: Window
        """
        self.rect = pygame.rect.Rect(x, y, width_number * 122 * Game.DISPLAY_RATIO, height_number * 64 * Game.DISPLAY_RATIO)

        if "centerx" in kwargs:
            self.rect.centerx = kwargs["centerx"]

        if "centery" in kwargs:
            self.rect.centery = kwargs["centery"]

        self.sprites = pygame.sprite.Group()
        for rx in range(width_number):
            for ry in range(height_number):
                item_type = ["M", "M"]
                if rx == 0:
                    item_type[1] = "L"
                elif rx == width_number - 1:
                    item_type[1] = "R"

                if ry == 0:
                    item_type[0] = "U"
                elif ry == height_number - 1:
                    item_type[0] = "D"

                item_type = item_type[0] + item_type[1]
                self.sprites.add(WindowItem(self.rect.x + (rx * 122 * Game.DISPLAY_RATIO), self.rect.y + (ry * 64 * Game.DISPLAY_RATIO) - ry, item_type))
        Window.window_list.append(self)
        Game.get_logger(__name__).debug("Window created")

    def kill(self):
        for sprite in self.sprites:
            sprite.kill()
        Window.window_list.remove(self)

    @classmethod
    def main_loop(cls):
        """Actualise toutes les fenêtres"""
        for win in Window.window_list:
            win.sprites.update()
            win.sprites.draw(Game.surface)
