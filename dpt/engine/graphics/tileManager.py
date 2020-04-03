from dpt.engine.graphics.platforms.Block import *
from dpt.game import Game
import pygame
import json

#          {"x, y": {"blockClass": Classe}}
class TileManager:

    LISTE = []

    def __init__(self):

        self.log = Game.get_logger("TileManager")
        self.userConfirm = True
        self.levelName = None
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        self.coords = None

    def enableGrid(self):
        if self.userConfirm:
            for x in range(0, Game.surface.get_size()[0], Game.TILESIZE):
                pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
            for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
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
                    sprite = eval(data + "((255, 0, 0), coords[0] * Game.TILESIZE, coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE)")
                    self.log.debug("Tile " + data + " placed at " + keys)
                    self.LISTE.append(sprite)
                    Game.platforms.add(sprite)
                except:
                    self.log.warning("Invalid class name : " + data + " for tile : " + keys)

    def update(self):
        self.enableGrid()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.log = Game.get_logger("Camera")

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = None
        if Game.playerSprite.right and Game.playerSprite.rect.right >= int(Game.surface.get_size()[0] / 4 * 3):
            x = -target.rect.x + int(Game.surface.get_size()[0] / 4 * 3)
        elif Game.playerSprite.left and Game.playerSprite.rect.left <= int(Game.surface.get_size()[0] / 4):
            self.log.debug("surface : " + str(int(Game.surface.get_size()[0] / 4)))
            self.log.debug("sprite : " + str(Game.playerSprite.rect.centerx))
            x = -target.rect.x + int(Game.surface.get_size()[0] / 4)
        if x is None:
            Game.surface.blit(Game.playerSprite.image, Game.playerSprite.rect)
            for sprite in Game.platforms:
                Game.surface.blit(sprite.image, sprite)
            print("Bonjour, je vient à l'instant de m'éxecuter.")
            return
        calcul = (self.width * Game.TILESIZE)-Game.surface.get_size()[0]
        x = min(0, x)
        x = max(-calcul, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        for sprite in Game.platforms:
            Game.surface.blit(sprite.image, self.apply(sprite))