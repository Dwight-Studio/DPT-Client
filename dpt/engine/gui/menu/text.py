import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Text:
    text_list = []

    def __init__(self, x, y, text, size, color, font, **kwargs):
        """Crée un texte

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type x: int
        :param text: Texte
        :type text: str
        :param size: Taille de la police d'écriture
        :type size: int
        :param color: Couleur du texte
        :type color: (int, int, int, int)
        :param font: Police d'écriture
        :type font: str

        :keyword centerx: Abscisse du centre, si specifié, ignore le paramètre x original
        :keyword centery: ordonnée du centre, si specifié, ignore le paramètre y original

        :rtype: Text
        """
        if "centerx" in kwargs:
            self.centerx = kwargs["centerx"]
        else:
            self.centerx = None

        if "centery" in kwargs:
            self.centery = kwargs["centery"]
        else:
            self.centery = None

        self.color = color
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(RessourceLoader.get(font), size)
        Text.text_list.append(self)
        Game.get_logger(__name__).debug("Text created")

    def draw(self, surface):
        """Dessine le texte"""
        self.text_rendered = self.font.render(self.text, True, self.color)
        self.rect = self.text_rendered.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.centerx is not None:
            self.rect.centerx = self.centerx

        if self.centery is not None:
            self.rect.centery = self.centery

        surface.blit(self.text_rendered, self.rect)

    @classmethod
    def main_loop(cls):
        """Dessine tous les textes"""
        for t in Text.text_list:
            t.draw(Game.surface)
