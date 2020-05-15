import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Spike(pygame.sprite.Sprite):
    texture = "dpt.images.environment.traps.Obstacle_Spike_Up"
    textures = ["dpt.images.environment.traps.Obstacle_Spike_*", "dpt.images.environment.traps.spike"]
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = Game.TILESIZE
    height = Game.TILESIZE // 2
    offset_x = 0
    offset_y = -height
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.interactible_blocks_group, TileManager.entity_group, TileManager.deadly_object_group)
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
        self.anim_texture = None
        self.i = 0
        self.done = True
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image)

    def deactivate(self):
        from dpt.engine.tileManager import TileManager
        self.down = False
        self.i = 0
        self.done = False
        TileManager.deadly_object_group.add(self)
        self.anim_texture = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple("dpt.images.environment.traps.Spike.Obstacle_Spike_Up_*")]

    def activate(self):
        self.up = False
        self.i = -1
        self.done = False
        from dpt.engine.tileManager import TileManager
        TileManager.deadly_object_group.remove(self)
        self.anim_texture = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple("dpt.images.environment.traps.Spike.Obstacle_Spike_Up_*")]
        self.anim_texture.reverse()

    def update(self):
        if not self.down and not self.done:
            self.image = self.anim_texture[self.i * Game.settings["30_FPS"]]
            self.rect = self.image.get_rect()
            self.rect.x = self.x + self.offset_x
            self.rect.y = self.y + self.offset_y
            self.i += 1
            if self.i == len(self.anim_texture) // Game.settings["30_FPS"]:
                self.done = True
        elif not self.up and not self.done:
            self.image = self.anim_texture[self.i * Game.settings["30_FPS"]]
            self.rect = self.image.get_rect()
            self.rect.x = self.x + self.offset_x
            self.rect.y = self.y + self.offset_y
            self.i += 1
            if self.i == len(self.anim_texture) // Game.settings["30_FPS"]:
                self.done = True
