from dpt.game import Game
import pygame
import sys
from dpt.engine.graphics.platforms.Block import *

#          {x, y: {"blockClass": Classe}}
levelTest ={"11": {"blockClass": Block},
            "12": {"blockClass": Block}}

class TileManager():
    def __init__(self):
        self.game = Game.get_instance()
        self.log = self.game.get_logger("TileManager")
        self.tileSize = 32
        self.userConfirm = True
        self.levelName = levelTest

    def enableGrid(self):
        if self.userConfirm:
            for x in range(0, self.game.surface.get_size()[0], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (x, 0), (x, self.game.surface.get_size()[1]))
            for y in range(0, self.game.surface.get_size()[1], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (0, y), (self.game.surface.get_size()[0], y))

    def disableGrid(self):
        pass

    def loadLevel(self, levelName):
        i = 0
        for keys in levelTest:
            blockx = int(tuple(keys)[0]) * self.tileSize
            blocky = int(tuple(keys)[1]) * self.tileSize
            i += 1
            for data in levelTest[keys].values():
                self.game.platforms.add(data((255, 0, 0), blockx, blocky, self.tileSize, self.tileSize))

