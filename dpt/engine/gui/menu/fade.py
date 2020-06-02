#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.game import Game


class FadeOut:

    def __init__(self, time_in_millis):
        self.time = time_in_millis
        self.done = False
        self.rect = Game.surface.get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0

    def update(self):
        if not self.done:
            self.image.fill((0, 0, 0, self.alpha))
            self.alpha += math.ceil(255 / ((self.time / 1000) * 60))
            self.alpha = min(self.alpha, 255)
            if self.alpha == 255:
                self.done = True

    def draw(self, sur):
        sur.blit(self.image, self.rect)


class FadeIn:

    def __init__(self, time_in_millis):
        self.time = time_in_millis
        self.done = False
        self.rect = Game.surface.get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 255

    def update(self):
        if not self.done:
            self.alpha -= math.ceil(60 / self.time)
            self.alpha = max(self.alpha, 255)
            if self.alpha == 0:
                self.done = True
            self.image.fill((0, 0, 0, self.alpha))

    def draw(self, sur):
        sur.blit(self.image, self.rect)
