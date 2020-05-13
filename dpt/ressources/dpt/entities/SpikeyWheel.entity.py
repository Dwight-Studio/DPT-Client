import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class SpikeyWheel(pygame.sprite.Sprite):
    texture = "dpt.images.environment.traps.SpikeyWheel"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = height = Game.TILESIZE
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True
    i = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group, TileManager.deadly_object_group, TileManager.interactible_blocks_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.original_rest = self.rect
        self.x = x
        self.y = y
        self.active = True
        self.rotate = 1
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.active:
            if self.i == 2:
                self.i = 0
                self.image = RessourceLoader.get(self.texture)
                self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                self.image = pygame.transform.rotate(self.image, self.rotate)
                if self.rotate == 360:
                    self.rotate = 0
                self.rotate += 5
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.i += 1

    def activate(self):
        self.active = False

    def deactivate(self):
        self.active = True
