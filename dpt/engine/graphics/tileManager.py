from dpt.engine.graphics.blocks import *
from dpt.engine.graphics.enemies import *
from dpt.engine.graphics.gui.editor import *
from dpt.game import Game
import pygame


#          {"x, y": {"blockClass": Classe}}
class TileManager:

    def __init__(self):

        self.log = Game.get_logger("TileManager")
        self.levelName = None
        self.maxWidthSize = 0
        self.maxHeightSize = 0
        self.coords = None
        Game.availableTiles = {"blockClass": ["Block", "CeciEstUnBlock"],
                               "enemyClass": ["EnemySprite"]}

    def loadLevel(self, levelName):
        TileManager.LISTE = []
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
            for key, data in level[keys].items():
                if key == "blockClass":
                    try:
                        block = eval(data + "(coords[0] * Game.TILESIZE, coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
                        self.log.debug("Tile " + data + " placed at " + keys)
                        Game.environment.add(block)
                    except NameError:
                        self.log.warning("Invalid class name : " + data + " for tile : " + keys)
                elif key == "enemyClass":
                    try:
                        enemy = eval(data + "(coords[0] * Game.TILESIZE, coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE)")
                        self.log.debug("Tile " + data + " placed at " + keys)
                        Game.enemyGroup.add(enemy)
                    except NameError:
                        self.log.warning("Invalid class name : " + data + " for tile : " + keys)
        Game.environment.draw(Game.surface)
        Game.enemyGroup.draw(Game.surface)
        self.log.info("Done")

    def ghostBlock(self, xTile, yTile, itemClass, classType):
        if classType == "blockClass":
            ghostBlock = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 80)")
            Game.ghostBlock.add(ghostBlock)
        elif classType == "enemyClass":
            ghostBlock = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 80)")
            Game.ghostBlock.add(ghostBlock)

    def placeBlock(self, xTile, yTile, itemClass, classType):
        if classType == "blockClass":
            block = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
            self.log.debug("Tile " + itemClass + " placed at " + str(xTile) + ", " + str(yTile))
            Game.platformsList.append(block)
            Game.environment.add(block)
        elif classType == "enemyClass":
            enemy = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
            self.log.debug("Tile " + itemClass + " placed at " + str(xTile) + ", " + str(yTile))
            Game.enemyList.append(enemy)
            Game.enemyGroup.add(enemy)

    def openTilePanel(self):
        panel = EditorPanel((255, 255, 255), Game.surface.get_size()[0] / 4 * 3, 0, Game.surface.get_size()[0] / 4, Game.surface.get_size()[1], 120)
        Game.editorPanel.add(panel)
        startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
        starty = Game.surface.get_size()[1] + 32
        for tiles in Game.availableTiles.values():
            for element in tiles:
                sprite = eval(element + "(0, 0, Game.TILESIZE, Game.TILESIZE, 255)")

class Camera:
    def __init__(self, width, height):
        self.userConfirm = True
        self.camera = None
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
        for sprite in Game.environment:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x

    def enableGrid(self):
        if self.userConfirm:
            for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
                pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
            for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
                pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))