import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class BoxRedR(pygame.sprite.Sprite):
    texture = "dpt.images.environment.blocks.Block_empty_Red"
    textures = "dpt.images.environment.blocks.Block_Red"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = height = Game.TILESIZE
    offset_x = 0
    offset_y = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group,
                                      TileManager.interactible_blocks_group)
        self.image_original = pygame.transform.smoothscale(RessourceLoader.get(self.texture), (self.width, self.height))
        self.image_other = pygame.transform.smoothscale(RessourceLoader.get(self.textures), (self.width, self.height))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image_other)

    def activate(self):
        from dpt.engine.tileManager import TileManager
        self.image = self.image_other
        TileManager.environment_group.add(self)
        TileManager.entity_group.remove(self)

    def deactivate(self):
        from dpt.engine.tileManager import TileManager
        self.image = self.image_original
        TileManager.environment_group.remove(self)
        TileManager.entity_group.add(self)
