import math

import pygame

from dpt.engine.effectsManagement import EffectsManagement
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager
from dpt.game import Game


class DeadBody(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, texture, mask):
        self.frameCount = 0
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(texture)
        self.yvel = 0
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.o_image = self.image
        self.maskSurface = pygame.transform.scale(RessourceLoader.get(mask), (width, height))
        self.mask = pygame.mask.from_surface(self.maskSurface)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.onPlatform = False
        self.gravityCount = 0
        self.gravity = 0
        self.gravityModifier = 0
        self.c = 0
        self.blink = False

    def update(self):
        if not TileEditor.is_editing:
            from dpt.engine.tileManager import TileManager
            if not Game.freeze_game:
                if not EffectsManagement.dico_current_effects["Slow"] or (EffectsManagement.dico_current_effects["Slow"] and self.frameCount % 3) == 0:
                    self.gravityCount += 1
                    self.gravity = math.floor((self.gravityCount ** 2) * (0.05 - self.gravityModifier) * Game.DISPLAY_RATIO) * -1
                    self.yvel = self.gravity
                    self.frameCount += 1
                else:
                    self.frameCount += 1

                self.maskcollide()
                self.rect.top -= math.floor(self.yvel)

                self.check_void()
        self.c += 1
        if self.c > 120 and self.c % 7 == 0:
            self.blink = not self.blink
            if self.c > 300:
                self.kill()
                del self
                return

        if self.blink:
            self.image = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
        else:
            self.image = self.o_image

    def check_void(self):
        if self.rect.top > 2000:
            self.kill()

    def maskcollide(self):
        for i in TileManager.environment_group:
            if i.rect.colliderect(Game.display_rect):
                rx = i.rect.x - self.rect.x
                ry = i.rect.y - (self.rect.y - math.floor(self.yvel))

                if self.mask.overlap(i.mask, (rx, ry)):
                    dy = 0

                    mask = self.mask.overlap_mask(i.mask, (rx, ry))
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
