import math

import pygame

from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.loader import RessourceLoader
from dpt.engine.effectsManagement import EffectsManagement
from dpt.game import Game


def pythagore(xa, ya, xb, yb):
    """Permet d'avoir la distance entre deux points

        :param xa: Abscisse du premier point
        :type xa: int
        :param ya: Ordonnée du premier point
        :type ya: int
        :param xb: Abscisse du second point
        :type xb: int
        :param yb: Ordonnée du second point
        :type yb: int

        :rtype: float
        """
    return math.sqrt((xb-xa)**2 + (yb-ya)**2)


class GhostSpriteLight(pygame.sprite.Sprite):
    """Classe sur les fantômes clairs et leur physique"""
    texture = "dpt.images.characters.ghosts.Ghost_Light_1"
    textures = "dpt.images.characters.ghosts.Ghost_Light*"
    width = math.floor(92.4 * Game.DISPLAY_RATIO)
    height = math.floor(76.8 * Game.DISPLAY_RATIO)
    offset_x = (Game.TILESIZE - width) // 2
    offset_y = (Game.TILESIZE - height) // 2
    mask = "dpt.images.characters.ghosts.mask"

    def __init__(self, x, y):
        """Crée un fantôme clair

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int

        :rtype: GhostSpriteLight
        """
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.enemy_group, TileManager.entity_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.boo = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(self.textures)]
        self.booReverse = [pygame.transform.flip(i, True, False) for i in self.boo]
        self.xvel = 0
        self.yvel = 0
        self.up = False
        self.down = True
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.CONSTHEIGT = self.height
        self.CONSTWIDTH = self.width
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.CONSTRECT2 = self.rect[2]
        self.CONSTRECT3 = self.rect[3]
        self.lastx = 0
        self.lasty = 0
        self.maxvelocity = 2
        self.big = False
        self.distance = 0
        self.mask = pygame.mask.from_surface(pygame.transform.scale(RessourceLoader.get(GhostSpriteLight.mask),
                                                                    (self.width, self.height)))

    def update(self):
        """Actualise le déplacement, les effets, les collisions"""
        if not TileEditor.is_editing:
            from dpt.engine.tileManager import TileManager
            if not Game.freeze_game:

                Game.add_debug_info("Enemy.left = " + str(self.up))
                Game.add_debug_info("Enemy.right = " + str(self.down))

                if EffectsManagement.dico_current_effects["Slow"]:
                    self.maxvelocity = 1
                else:
                    self.maxvelocity = 2

                if EffectsManagement.dico_current_effects["monsterimmortal"] and not self.big:
                    self.height = math.floor(self.height * 1.4)
                    self.width = math.floor(self.width * 1.4)
                    self.big = True
                    self.rect[2] //= 0.71
                    self.rect[3] //= 0.71
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                elif not EffectsManagement.dico_current_effects["monsterimmortal"]:
                    self.height = self.CONSTHEIGT
                    self.width = self.CONSTWIDTH
                    self.big = False
                    self.rect[2] = self.CONSTRECT2
                    self.rect[3] = self.CONSTRECT3
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

                if self.up:
                    if self.yvel > 0:
                        self.yvel = 0
                    if self.yvel > -self.maxvelocity * Game.DISPLAY_RATIO:
                        self.yvel -= (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.up = True
                    self.down = False
                elif self.down:
                    if self.yvel < 0:
                        self.yvel = 0
                    if self.yvel < self.maxvelocity * Game.DISPLAY_RATIO:
                        self.yvel += (self.maxvelocity / 2) * Game.DISPLAY_RATIO
                    self.up = False
                    self.down = True
                else:
                    self.yvel = 0

            self.distance += abs(self.yvel) * Game.settings["30_FPS"]
            self.rect.top += math.floor(self.yvel) * Game.settings["30_FPS"]

            self.animation()

            if self.distance > 500 * Game.DISPLAY_RATIO:
                self.distance = 0
                self.up = not self.up
                self.down = not self.down
        else:
            pygame.draw.line(Game.surface, (193, 39, 45), self.rect.center, (self.rect.centerx, self.rect.centery + math.floor(500 * Game.DISPLAY_RATIO)), 5)

    def animation(self):
        """Donne l'illusion de déplacement"""
        xb = Game.player_sprite.rect.x
        yb = Game.player_sprite.rect.y
        if pythagore(self.rect.x, self.rect.y, xb, yb) < 400:
            if self.rect.x - xb > 0:
                self.image = self.boo[1]
            else:
                self.image = self.booReverse[1]
        else:
            if self.rect.x - xb > 0:
                self.image = self.boo[0]
            else:
                self.image = self.booReverse[0]
