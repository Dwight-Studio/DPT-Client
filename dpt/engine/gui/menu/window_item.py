import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class WindowItem(pygame.sprite.Sprite):
    type = {
        "MM": "dpt.images.gui.ui.UI_WINDOW_1",
        "DL": "dpt.images.gui.ui.UI_WINDOW_2",
        "DM": "dpt.images.gui.ui.UI_WINDOW_3",
        "DR": "dpt.images.gui.ui.UI_WINDOW_4",
        "MR": "dpt.images.gui.ui.UI_WINDOW_5",
        "ML": "dpt.images.gui.ui.UI_WINDOW_6",
        "UR": "dpt.images.gui.ui.UI_WINDOW_7",
        "UL": "dpt.images.gui.ui.UI_WINDOW_8",
        "UM": "dpt.images.gui.ui.UI_WINDOW_9"
    }

    def __init__(self, x, y, item_type):
        """Crée une partie de fenêtre

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type x: int
        :param item_type: Type
        :type item_type: str

        :rtype: WindowItem
        """
        from dpt.engine.gui.menu.window import Window
        pygame.sprite.Sprite.__init__(self, Window.window_group)
        self.image = pygame.transform.smoothscale(RessourceLoader.get(WindowItem.type[item_type]), (math.ceil(122 * Game.DISPLAY_RATIO), math.ceil(64 * Game.DISPLAY_RATIO)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
