import pygame
import math
from dpt.game import Game

class EditorPanel(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.log = Game.get_logger("EditorPanel")

    def update(self):
        mouse = pygame.mouse.get_pos()
        mouseButtons = pygame.mouse.get_pressed()
        if mouseButtons[0] == 1:
            mousePosX = math.floor(mouse[0] / Game.TILESIZE)
            mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            key = str(mousePosX) + ", " + str(mousePosY)
            if key in Game.editorTileRegistry:
                for keys, values in Game.editorTileRegistry[key].items():
                    if keys == "itemClass":
                        Game.itemClass = values
                    elif keys == "classType":
                        Game.classType = values
                self.log.debug("Selected : " + str(Game.itemClass))
            else:
                pass

