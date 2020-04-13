import pygame
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError


class BackgroundFakeBlocks(pygame.sprite.Sprite):
    def __init__(self, x, y, block):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.backgroundBlocks)
        try:
            self.block = RessourceLoader.get(block)
            self.image = RessourceLoader.get(self.block.texture)
        except UnreachableRessourceError:
            self.image = RessourceLoader.get("dpt.images.not_found")
        self.image = pygame.transform.scale(self.image, (self.block.width, self.block.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.block.offset_x
        self.rect.y = y + self.block.offset_y