#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.game import Game


class MainMenuEntity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Game.player_group)  # Sprite's constructor called
        self.image = pygame.Surface((Game.TILESIZE, Game.TILESIZE))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = Game.WINDOW_WIDTH / 2
        self.rect.y = Game.WINDOW_HEIGHT / 2
        self.width = Game.TILESIZE
        self.height = Game.TILESIZE
        self.right = True
        self.left = False

    def update(self):
        self.rect.x += math.ceil(4 * Game.DISPLAY_RATIO * Game.settings["30_FPS"])
