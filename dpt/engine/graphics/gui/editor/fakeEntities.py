import pygame
from dpt.engine.graphics.gui.editor import EditorPanel
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class FakeEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, alpha, block):
        pygame.sprite.Sprite.__init__(self, EditorPanel.editorPanelGroup)
        self.texture = RessourceLoader.get(block).texture
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (Game.TILESIZE, Game.TILESIZE))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height