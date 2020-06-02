#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game


class BackgroundFakeBlocks(pygame.sprite.Sprite):
    def __init__(self, x, y, block):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.background_blocks_group)
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
        self.offset_x = self.block.offset_x
        self.offset_y = self.block.offset_y
        if hasattr(self.block, "customPlacement"):
            self.customPlacement = True

        if not TileManager.is_loading_level:
            try:
                if isinstance(self.block.sounds, list):
                    self.sound = RessourceLoader.get(self.block.sounds[0])
                elif isinstance(self.block.sounds, str):
                    self.sound = RessourceLoader.get(self.block.sounds)
                else:
                    return
                self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                self.sound.play()
            except Exception:
                pass
