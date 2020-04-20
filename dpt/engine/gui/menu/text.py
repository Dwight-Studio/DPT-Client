import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Text:
    text_list = []

    def __init__(self, x, y, text, size, color, font):
        self.font = pygame.font.Font(RessourceLoader.get(font), size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y
        Text.text_list.append(self)
        Game.get_logger("Text").debug("Text created")

    def draw(self, surface):
        surface.blit(self.text, self.rect)

    @classmethod
    def main_loop(cls):
        for t in Text.text_list:
            t.draw(Game.surface)
