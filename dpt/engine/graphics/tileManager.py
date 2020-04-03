from dpt.engine.graphics.platforms.Block import *
from dpt.game import Game
import pygame
import json

#          {"x, y": {"blockClass": Classe}}
class TileManager:

    LISTE = []

    def __init__(self):

        self.log = Game.get_logger("TileManager")
        self.tileSize = 32
        self.userConfirm = True
        self.levelName = None
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        self.coords = None

    def enableGrid(self):
        if self.userConfirm:
            for x in range(0, Game.surface.get_size()[0], self.tileSize):
                pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
            for y in range(0, Game.surface.get_size()[1], self.tileSize):
                pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))

    def disableGrid(self):
        pass

    def loadLevel(self, levelName):
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        if levelName is None:
            self.log.critical("The level can't be loaded")
        for keys in levelName:
            coords = tuple(map(int, keys.split(", ")))
            if coords[0] > self.maxWidthSize:
                self.maxWidthSize = coords[0]
            elif coords[1] > self.maxHeightSize:
                self.maxHeightSize = coords[1]
            if coords[0] < 0 or coords[1] < 0:
                self.log.warning("The tile position can't be negative : " + keys)
                continue
            for data in levelName[keys].values():
                try:
                    sprite = eval(data + "((255, 0, 0), coords[0] * self.tileSize, coords[1] * self.tileSize, self.tileSize, self.tileSize)")
                    self.log.debug("Tile " + data + " placed at " + keys)
                    self.LISTE.append(sprite)
                    Game.platforms.add(sprite)
                except:
                    self.log.warning("Invalid class name : " + data + " for tile : " + keys)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        x = min(0, x)
        #x = max(-self.width, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
