import pygame
import math

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
        self.width = math.floor(200 * self.size)
        self.height = math.floor(200 * self.size)
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
            self.image = RessourceLoader.get("dpt.images.not_found")
        except KeyError:
            self.image = RessourceLoader.get("dpt.images.not_found")

        try:
            self.locked = not Game.stars >= self.level["required_stars"]
        except KeyError:
            self.locked = False

        try:
            scores = Game.saves[level_name]
            self.score = int(scores[max(scores.items(), key=lambda key: scores[key])])
        except KeyError:
            self.score = 0

        self.star_1 = TransitionStar(self.rect.centerx - math.floor(60 * self.size),
                                     self.rect.bottom - math.floor(30 * self.size),
                                     self.score >= 1000,
                                     False, False)

        self.star_2 = TransitionStar(self.rect.centerx,
                                     self.rect.bottom - math.floor(30 * self.size),
                                     self.score >= 2000,
                                     False, False)

        self.star_3 = TransitionStar(self.rect.centerx + math.floor(60 * self.size),
                                     self.rect.bottom - math.floor(30 * self.size),
                                     self.score >= 3000,
                                     False, False)

        if self.locked:
            self.lock = SimpleSprite(math.floor(48 * self.size),
                                     math.floor(64 * self.size),
                                     RessourceLoader.get("dpt.images.gui.ui.ui_lock"),
                                     centerx=self.rect.right,
                                     centery=self.rect.top)
        else:
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
        Game.surface.blit(self.lock.image, self.lock.rect)
        print(self.lock.rect)
        self.star_1.update()
        self.star_2.update()
        self.star_3.update()

        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    sound = RessourceLoader.get("dpt.sounds.sfx.switch6")
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()

                    menu.delete_items()
                    Game.selected_level = self.level_name
                    Scenes.level_selector_detail()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            Game.cursor_on_button = True

    def kill(self, del_bool=True):
        """Tue le résumé de niveau

        :param del_bool: Supprime de la liste
        :type del_bool: bool
        """
        self.lock.kill()
        if del_bool:
            LevelOverview.level_overview_list.remove(self)
            del self

    @classmethod
    def main_loop(cls):
        """Actualise tous les résumés de niveau"""
        for lo in LevelOverview.level_overview_list:
            lo.update()
