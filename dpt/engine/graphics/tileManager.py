from dpt.engine.graphics.blocks import *
from dpt.game import Game
import pygame


#          {"x, y": {"blockClass": Classe}}
class TileManager:
    LISTE = []

    def __init__(self):

        self.log = Game.get_logger("TileManager")
        self.levelName = None
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        self.coords = None

    def loadLevel(self, levelName):
        if type(levelName) == str:
            self.log.info("Loading level " + levelName)
            level = Game.ressources.get(levelName)
        else:
            self.log.info("Loading unknown level")
            level = levelName
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        if level is None:
            self.log.critical("The level can't be loaded")
        for keys in level:
            coords = tuple(map(int, keys.split(", ")))
            if coords[0] > self.maxWidthSize:
                self.maxWidthSize = coords[0]
            elif coords[1] > self.maxHeightSize:
                self.maxHeightSize = coords[1]
            if coords[0] < 0 or coords[1] < 0:
                self.log.warning("The tile position can't be negative : " + keys)
                continue
            for data in level[keys].values():
                try:
                    sprite = eval(data + "((255, 0, 0), coords[0] * Game.TILESIZE, coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE)")
                    self.log.debug("Tile " + data + " placed at " + keys)
                    self.LISTE.append(sprite)
                    Game.platforms.add(sprite)
                except:
                    self.log.warning("Invalid class name : " + data + " for tile : " + keys)
        self.log.info("Done")


class Camera:
    def __init__(self, width, height):
        self.userConfirm = True

        self.width = width
        self.height = height
        self.log = Game.get_logger("Camera")
        self.last_x = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        Game.add_debug_info("Right : " + str(Game.playerSprite.right))
        Game.add_debug_info("Left : " + str(Game.playerSprite.left))
        Game.add_debug_info("Player X :" + str(target.rect.centerx))
        Game.add_debug_info("Player Y : " + str(target.rect.centery))

        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        calcul = (self.width * Game.TILESIZE) - Game.surface.get_size()[0]
        x = min(self.last_x, x)
        x = max(-calcul, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        for sprite in Game.platforms:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x


    def enableGrid(self):
        if self.userConfirm:
            for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
                pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
            for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
                pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))

    def disableGrid(self):
        pass
