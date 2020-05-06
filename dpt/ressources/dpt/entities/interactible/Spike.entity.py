import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Spike(pygame.sprite.Sprite):
    texture = "dpt.images.environment.traps.Obstacle_Spike_Up"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = Game.TILESIZE
    height = Game.TILESIZE // 2
    offset_x = 0
    offset_y = -height
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.interactible_blocks_group, TileManager.deadly_object_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.x = x
        self.y = y
        self.up = True
        self.down = False
        self.clicked = False
        self.is_clicked = False
        self.already = False
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def activate(self):
        self.down = False
        texture = "dpt.images.environment.traps.Obstacle_Spike_Up"
        self.image = RessourceLoader.get(texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x + self.offset_x
        self.rect.y = self.y + self.offset_y

    def deactivate(self):
        self.up = False
        texture = "dpt.images.environment.traps.Obstacle_Spike_Down"
        self.image = RessourceLoader.get(texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x + self.offset_x
        self.rect.y = self.y + self.offset_y