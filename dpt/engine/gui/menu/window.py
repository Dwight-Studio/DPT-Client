import pygame
import math

from dpt.engine.gui.menu.window_item import WindowItem
from dpt.game import Game


class Window:
    window_group = pygame.sprite.Group()

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

        self.sprites = []
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
                self.sprites.append(WindowItem(self.rect.x + (rx * 122 * Game.DISPLAY_RATIO), self.rect.y + (ry * 64 * Game.DISPLAY_RATIO) - ry, item_type))
        Game.get_logger("Menu.Window").debug("Window created")

    @classmethod
    def main_loop(cls):
        """Actualise toutes les fenêtres"""
        Window.window_group.update()
        Window.window_group.draw(Game.surface)
