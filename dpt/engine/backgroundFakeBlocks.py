import pygame
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError


class BackgroundFakeBlocks(pygame.sprite.Sprite):
    def __init__(self, x, y, block):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.background_blocks)
        try:
            self.block = RessourceLoader.get(block)
            self.image = RessourceLoader.get(self.block.texture).copy()
        except UnreachableRessourceError:
            self.block = RessourceLoader.get("dpt.blocks.NotFound")
            self.image = RessourceLoader.get(self.block.texture)
        self.image.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_SUB)
        self.image = pygame.transform.scale(self.image, (self.block.width, self.block.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.block.offset_x
        self.rect.y = y + self.block.offset_y
