from dpt.engine.loader import RessourceLoader
from dpt.game import Game

import pygame
import math


class TransitionStar:
    textures = ("dpt.images.gui.ui.UI_STAR_EMTPY", "dpt.images.gui.ui.UI_STAR_NORMAL")

    def __init__(self, x, y, filled, anim, run=True):
        """Crée une étoile

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int
        :param filled: Étoile remplie
        :type filled: bool
        :param anim: Étoile animée
        :type anim: bool
        :param run: Animation en fonctionnement
        :type run: bool

        :rtype: TransitionStar
        """
        self.anim = anim
        self.filled = filled
        self.star = (pygame.transform.smoothscale(RessourceLoader.get(self.textures[0]), (math.floor(50 * Game.DISPLAY_RATIO), math.floor(50 * Game.DISPLAY_RATIO))),
                     RessourceLoader.get(self.textures[1]))
        self.images = []
        self.run = filled and run and anim
        self.image = pygame.transform.smoothscale(RessourceLoader.get(self.textures[1]), (math.floor(50 * Game.DISPLAY_RATIO), math.floor(50 * Game.DISPLAY_RATIO)))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.i = 0

        if anim:
            for i in range(0, math.floor(500 * Game.DISPLAY_RATIO), math.floor((500 * Game.DISPLAY_RATIO) / 30)):
                self.images.append(pygame.transform.smoothscale(self.star[1], (math.floor(550 * Game.DISPLAY_RATIO) - i, math.floor(550 * Game.DISPLAY_RATIO) - i)))
            self.images.append(self.image)

        self.max = len(self.images) - 1

    def update(self):
        """Actualise l'étoile"""
        if not self.anim:
            if self.filled:
                Game.surface.blit(self.image, self.rect)
            else:
                Game.surface.blit(self.star[0], (self.x - math.floor(25 * Game.DISPLAY_RATIO), self.y - math.floor(25 * Game.DISPLAY_RATIO)))
        else:
            Game.surface.blit(self.star[0], (self.x - math.floor(25 * Game.DISPLAY_RATIO), self.y - math.floor(25 * Game.DISPLAY_RATIO)))

        if self.run and self.i < self.max:
            self.image = self.images[self.i]
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y
            self.i += 1
            Game.surface.blit(self.image, self.rect)
        elif not self.i < self.max and self.run:
            sound = RessourceLoader.get("dpt.sounds.sfx.sfx_score_impact")
            sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            sound.play()
            self.run = False
            self.anim = False
            self.filled = True
            self.update()
