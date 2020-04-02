from dpt.game import Game
import pygame
import sys
from dpt.engine.graphics.platforms.Block import *

#          {"x, y": {"blockClass": Classe}}
levelTest ={"8, 1": {"blockClass": Block},
            "8, 2": {"blockClass": Block},
            "8, 3": {"blockClass": Block},
            "12, 1":{"blockClass": Block},
            "12, 2":{"blockClass": Block},
            "42, 3":{"blockClass": Block},}

class TileManager():
    def __init__(self):
        self.game = Game.get_instance()
        self.log = self.game.get_logger("TileManager")
        self.tileSize = 32
        self.userConfirm = True
        self.levelName = None

    def enableGrid(self):
        if self.userConfirm:
            for x in range(0, self.game.surface.get_size()[0], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (x, 0), (x, self.game.surface.get_size()[1]))
            for y in range(0, self.game.surface.get_size()[1], self.tileSize):
                pygame.draw.line(self.game.surface, (220, 220, 220), (0, y), (self.game.surface.get_size()[0], y))

    def disableGrid(self):
        pass

    def loadLevel(self, levelName):
        if levelName == None:
            self.log.critical("The level can't be loaded")
        for keys in levelTest:
            coords = tuple(map(int, keys.split(", ")))
            if coords[0] < 0 or coords[1] < 0:
                self.log.warning("The tile position can't be negative")
                continue
            elif coords[0] > self.game.surface.get_size()[0] / self.tileSize or coords[1] > self.game.surface.get_size()[1]:
                self.log.warning("The tile position can't be greater that the screen size")
                continue
            for data in levelTest[keys].values():
                self.game.platforms.add(data((255, 0, 0), coords[0] * self.tileSize, coords[1] * self.tileSize, self.tileSize, self.tileSize))

