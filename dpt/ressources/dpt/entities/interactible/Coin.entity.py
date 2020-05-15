import pygame
import random

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Coin(pygame.sprite.Sprite):
    texture = "dpt.images.environment.coins.00"
    textures = "dpt.images.environment.coins.*"
    sounds = ["dpt.sounds.sfx.sfx_stone", "dpt.sounds.sfx.sfx_coin_picked"]
    screen_width, screen_height = (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
    width = Game.TILESIZE // 2
    height = Game.TILESIZE // 2
    offset_x = Game.TILESIZE // 4
    offset_y = Game.TILESIZE // 4

    coin_checkpoint_list = []

    def __init__(self, x, y):
        self.id = int(str(int(x)) + str(int(y)))
        if self.id in Coin.coin_checkpoint_list and not TileEditor.enabled_editor:
            del self
            return
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.frames = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(
            self.textures)]
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.animCount = 0
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(Coin.sounds[0])
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def update(self):
        self.animation()
        self.collide()

    def animation(self):
        self.image = self.frames[Game.anim_count_coins // 4]

    def collide(self):
        for i in Game.player_group:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                self.sound = RessourceLoader.get(Coin.sounds[1])
                self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                self.sound.play()
                if "coins" not in Game.temp:
                    Game.temp.update({"coins": 1})
                else:
                    Game.temp["coins"] += 1
                Coin.coin_checkpoint_list.append(self.id)
                del self
                return
