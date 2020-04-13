import pygame
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game


class GhostFakeEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha, block):
        pygame.sprite.Sprite.__init__(self, TileEditor.ghostBlockGroup)
        try:
            self.block = RessourceLoader.get(block)
            self.image = RessourceLoader.get(self.block.texture)
        except UnreachableRessourceError:
            self.block = RessourceLoader.get("dpt.blocks.NotFound")
            self.image = RessourceLoader.get(self.block.texture)
        self.image = pygame.transform.scale(self.image, (self.block.width, self.block.height))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x + self.block.offset_x
        self.rect.y = y + self.block.offset_y
