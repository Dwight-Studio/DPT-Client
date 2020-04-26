import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Text:
    text_list = []

    def __init__(self, x, y, text, size, color, font, **kwargs):
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
        Game.get_logger("Text").debug("Text created")

    def draw(self, surface):
        self.text_rendered = self.font.render(self.text, True, self.color)
        self.rect = self.text_rendered.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.centerx is not None and self.centery is not None:
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
        surface.blit(self.text_rendered, self.rect)

    @classmethod
    def main_loop(cls):
        for t in Text.text_list:
            t.draw(Game.surface)
