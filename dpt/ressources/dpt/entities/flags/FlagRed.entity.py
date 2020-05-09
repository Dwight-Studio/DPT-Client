import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class FlagRed(pygame.sprite.Sprite):
    texture = "dpt.images.environment.flag.Flag_Red"
    sounds = "dpt.sounds.sfx.sfx_stone"
    screen_width, screen_height = (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
    width = Game.TILESIZE
    height = Game.TILESIZE * 2
    offset_x = 0
    offset_y = -Game.TILESIZE

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group, TileManager.interactible_blocks_group, TileManager.foreground_blocks_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        FlagRed.spawn_flag = self

    def update(self):
        for i in Game.player_group:
            if pygame.sprite.collide_mask(self, i):
                from dpt.engine.scenes import Scenes
                Scenes.end_level()