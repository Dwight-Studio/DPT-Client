from dpt.engine.graphics.platforms.Block import *
from dpt.game import Game
import pygame
import json

#          {"x, y": {"blockClass": Classe}}
levelTest = {"0, 32": {"blockClass": "Block"},
             "1, 32": {"blockClass": "Block"},
             "2, 32": {"blockClass": "Block"},
             "3, 32": {"blockClass": "Block"},
             "4, 32": {"blockClass": "Block"},
             "5, 32": {"blockClass": "Block"},
             "6, 32": {"blockClass": "Block"},
             "7, 32": {"blockClass": "Block"},
             "8, 32": {"blockClass": "Block"},
             "9, 32": {"blockClass": "CeciEstUnBlock"},
             "10, 32": {"blockClass": "Block"},
             "11, 32": {"blockClass": "Block"},
             "12, 32": {"blockClass": "Block"},
             "13, 31": {"blockClass": "Block"},
             "14, 30": {"blockClass": "Block"},
             "15, 30": {"blockClass": "Block"},
             "16, 30": {"blockClass": "Block"},
             "15, 28": {"blockClass": "Block"},
             "17, 30": {"blockClass": "Block"},
             "18, 31": {"blockClass": "Block"},
             "19, 32": {"blockClass": "Block"},
             "20, 32": {"blockClass": "Block"},
             "21, 32": {"blockClass": "Block"},
             "22, 32": {"blockClass": "Block"},
             "23, 32": {"blockClass": "Block"},
             "24, 32": {"blockClass": "Block"},
             "25, 32": {"blockClass": "Block"},
             "26, 32": {"blockClass": "Block"},
             "27, 32": {"blockClass": "Block"},
             "28, 32": {"blockClass": "Block"},
             "29, 32": {"blockClass": "Block"},
             "30, 32": {"blockClass": "Block"},
             "31, 32": {"blockClass": "Block"},
             "32, 32": {"blockClass": "Block"},
             "33, 32": {"blockClass": "Block"},
             "34, 32": {"blockClass": "Block"},
             "35, 32": {"blockClass": "Block"},
             "36, 32": {"blockClass": "Block"},
             "37, 32": {"blockClass": "Block"},
             "38, 32": {"blockClass": "Block"},
             "39, 32": {"blockClass": "Block"},
             "40, 32": {"blockClass": "Block"},
             "41, 32": {"blockClass": "Block"},
             "42, 32": {"blockClass": "Block"},
             "43, 32": {"blockClass": "Block"},
             "44, 32": {"blockClass": "Block"},
             "45, 32": {"blockClass": "Block"},
             "46, 32": {"blockClass": "Block"},
             "47, 32": {"blockClass": "Block"},
             "48, 32": {"blockClass": "Block"},
             "49, 32": {"blockClass": "Block"},
             "50, 32": {"blockClass": "Block"},
             "51, 32": {"blockClass": "Block"},
             "52, 32": {"blockClass": "Block"},
             "53, 32": {"blockClass": "Block"},
             "54, 32": {"blockClass": "Block"},
             "55, 32": {"blockClass": "Block"},
             "56, 32": {"blockClass": "Block"},
             "57, 32": {"blockClass": "Block"},
             "58, 32": {"blockClass": "Block"},
             "60, 32": {"blockClass": "Block"},
             "61, 32": {"blockClass": "Block"},
             "62, 32": {"blockClass": "Block"},
             "63, 32": {"blockClass": "Block"},
             "64, 32": {"blockClass": "Block"},
             "65, 32": {"blockClass": "Block"},
             "66, 32": {"blockClass": "Block"},
             "67, 32": {"blockClass": "Block"},
             "68, 32": {"blockClass": "Block"}}

print(json.dumps(levelTest))

class TileManager:
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
        for keys in levelTest:
            coords = tuple(map(int, keys.split(", ")))
            self.log.debug(coords)
            if coords[0] > self.maxWidthSize:
                self.maxWidthSize = coords[0]
                self.log.debug(self.maxWidthSize)
            elif coords[1] > self.maxHeightSize:
                self.maxHeightSize = coords[1]
            if coords[0] < 0 or coords[1] < 0:
                self.log.warning("The tile position can't be negative : " + keys)
                continue
            for data in levelTest[keys].values():
                try:
                    sprite = eval(data + "((255, 0, 0), coords[0] * self.tileSize, coords[1] * self.tileSize, self.tileSize, self.tileSize)")
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
        x = max(-self.width, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
