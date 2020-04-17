import pygame
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game


class PanelFakeEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha, block):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.editor_panel_group)
        try:
            self.block = RessourceLoader.get(block)
            self.image = RessourceLoader.get(self.block.texture)
        except UnreachableRessourceError:
            self.block = RessourceLoader.get("dpt.blocks.NotFound")
            self.image = RessourceLoader.get(self.block.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.block.width, self.block.height))
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + Game.TILESIZE // 2
        self.rect.centery = y + Game.TILESIZE // 2
