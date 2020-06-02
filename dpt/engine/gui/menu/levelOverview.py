#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.engine.gui.menu import Text
from dpt.game import Game
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.engine.gui.menu.score_stars import TransitionStar
from dpt.engine.gui.menu.simpleSprite import SimpleSprite
from dpt.engine.scenes import Scenes
import dpt.engine.gui.menu as menu


class LevelOverview:
    level_overview_list = []

    def __init__(self, x, y, level_name, size):
        """Crée un résumé de niveau

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int
        :param level_name: Nom du niveau
        :type level_name: str
        :param size: Taille (relative)
        :type size: float

        :rtype: LevelOverview
        """
        self.x = x
        self.y = y
        self.size = size * Game.DISPLAY_RATIO
        self.width = math.floor(130 * self.size)
        self.height = math.floor(130 * self.size)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.level_name = level_name

        try:
            self.level = RessourceLoader.get(level_name)["infos"]
        except UnreachableRessourceError:
            self.level = {}
        except KeyError:
            self.level = {}

        try:
            self.image = pygame.transform.smoothscale(RessourceLoader.get(self.level["image"]), (self.width, self.height))
        except UnreachableRessourceError:
            self.image = pygame.transform.smoothscale(RessourceLoader.get("dpt.images.not_found"), (self.width, self.height))
        except KeyError:
            self.image = pygame.transform.smoothscale(RessourceLoader.get("dpt.images.not_found"), (self.width, self.height))

        try:
            self.locked = not Game.stars >= self.level["required_stars"]
            self.required_stars = self.level["required_stars"]
        except KeyError:
            self.locked = False
            self.required_stars = 0

        try:
            scores = {k: int(v) for k, v in Game.saves[level_name].items()}
            k, v = max(scores.items(), key=lambda val: val[1])
            self.score = v
        except KeyError:
            self.score = 0
        except ValueError:
            self.score = 0

        self.star_1 = TransitionStar(self.rect.centerx - math.floor(40 * self.size),
                                     self.rect.bottom,
                                     self.score >= 1000,
                                     False, False, math.floor(35))

        self.star_2 = TransitionStar(self.rect.centerx,
                                     self.rect.bottom,
                                     self.score >= 2000,
                                     False, False, math.floor(35))

        self.star_3 = TransitionStar(self.rect.centerx + math.floor(40 * self.size),
                                     self.rect.bottom,
                                     self.score >= 3000,
                                     False, False, math.floor(35))
        Game.stars += self.score // 1000

        if self.locked:
            self.lock = SimpleSprite(math.floor(48 * self.size),
                                     math.floor(64 * self.size),
                                     RessourceLoader.get("dpt.images.gui.ui.ui_lock"),
                                     centerx=self.rect.right,
                                     centery=self.rect.top)

            width, height = self.image.get_size()
            for x in range(width):
                for y in range(height):
                    red, green, blue, alpha = self.image.get_at((x, y))
                    average = (red + green + blue) // 3
                    gs_color = (average, average, average, alpha)
                    self.image.set_at((x, y), gs_color)

            self.text = Text(self.rect.centerx - math.floor(35 * Game.DISPLAY_RATIO),
                             0,
                             str(self.required_stars) + "×",
                             math.floor(40 * Game.DISPLAY_RATIO),
                             (0, 0, 0),
                             "dpt.fonts.DINOT_CondBlack",
                             centery=self.rect.centery)

            self.star_req = TransitionStar(self.rect.centerx + math.floor(20 * Game.DISPLAY_RATIO),
                                           self.rect.centery,
                                           True,
                                           False, False, math.floor(35))



        elif level_name not in Game.saves:
            self.lock = SimpleSprite(math.floor(74 * self.size),
                                     math.floor(66 * self.size),
                                     RessourceLoader.get("dpt.images.gui.ui.ui_lock_open"),
                                     centerx=self.rect.right,
                                     centery=self.rect.top)

        LevelOverview.level_overview_list.append(self)
        Game.get_logger(LevelOverview.__name__).debug("LevelOverview created")

    def update(self):
        """Actualise le résumé de niveau"""
        Game.surface.blit(self.image, self.rect)
        if hasattr(self, "lock"):
            Game.surface.blit(self.lock.image, self.lock.rect)

        self.star_1.update()
        self.star_2.update()
        self.star_3.update()

        if self.locked:
            self.text.draw(Game.surface)
            self.star_req.update()

        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.locked and self.rect.collidepoint(pygame.mouse.get_pos()):
                    sound = RessourceLoader.get("dpt.sounds.sfx.switch6")
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()

                    menu.delete_items()
                    Game.levels_list = None
                    Game.selected_level = self.level_name
                    Scenes.level_selector_detail()

        if not self.locked and self.rect.collidepoint(pygame.mouse.get_pos()):
            Game.cursor_on_button = True

    def kill(self, del_bool=True):
        """Tue le résumé de niveau

        :param del_bool: Supprime de la liste
        :type del_bool: bool
        """
        if hasattr(self, "lock"):
            self.lock.kill()
        if del_bool:
            LevelOverview.level_overview_list.remove(self)
            del self

    @classmethod
    def main_loop(cls):
        """Actualise tous les résumés de niveau"""
        for lo in LevelOverview.level_overview_list:
            lo.update()
