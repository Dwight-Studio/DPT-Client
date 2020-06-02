#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame

from dpt.engine.loader import RessourceLoader
from dpt.game import Game
from dpt.engine.gui.editor.tileEditor import TileEditor


class Invisible(pygame.sprite.Sprite):
    texture = "dpt.images.environment.invisible"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = height = Game.TILESIZE
    offset_x = 0
    offset_y = 0

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.environment_group)
        if TileEditor.is_editing:
            self.image = RessourceLoader.get(self.texture)
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        else:
            self.image = pygame.surface.Surface((Game.TILESIZE, Game.TILESIZE)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.Mask((Game.TILESIZE, Game.TILESIZE), True)
