import math

import pygame

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager
from dpt.game import Game


class DeadBody(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, texture, mask):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemy_group, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(texture)
        self.yvel = 0
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.maskSurface = pygame.transform.scale(RessourceLoader.get(mask),
                                                  (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.maskSurface)
        self.rect = self.image.get_rect()
        self.onPlatform = False
        self.gravityCount = 0
        self.gravity = 0
        self.gravityModifier = 0

    def update(self):
        if not TileEditor.is_editing:
            from dpt.engine.tileManager import TileManager
            if not Game.freeze_game:

            self.maskcollide()
            self.rect.top -= math.floor(self.yvel)

            self.check_void()

    def check_void(self):
        if self.rect.top > 2000:
            self.kill()

    def maskcollide(self):
        for i in TileManager.environment_group:
            if i.rect.colliderect(Game.display_rect):
                rx = i.rect.x - (self.rect.x + math.floor(self.xvel))
                ry = i.rect.y - (self.rect.y - math.floor(self.yvel))

                if self.mask.overlap(i.mask, (rx, ry)):
                    dx = 0
                    dy = 0

                    crx = i.rect.x - self.rect.x
                    mask = self.mask.overlap_mask(i.mask, (crx, ry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.y < i.rect.y:
                            dy = rect.height + math.floor(self.yvel)
                            self.yvel = 0
                            self.onPlatform = True
                            self.gravityCount = 0
                        elif self.rect.y > i.rect.y:
                            dy = - rect.height + math.floor(self.yvel)
                            self.yvel = 0
                        break

                    self.rect.y -= dy
