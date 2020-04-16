import math
import pygame
from dpt.game import Game


class EditorPanel(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, alpha):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.editor_panel_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def update(self):
        mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] == 1:
            mouse_pos_x = math.floor(mouse[0] / Game.TILESIZE)
            mouse_pos_y = math.floor(mouse[1] / Game.TILESIZE)
            key = str(mouse_pos_x) + ", " + str(mouse_pos_y)
            if key in Game.editor_tile_registry:
                Game.selected_item = Game.editor_tile_registry[key]["class"]
            else:
                pass
