from dpt.engine.graphics.gui.editor.editorPanel import EditorPanel
from dpt.engine.graphics.gui.editor.tileEditor import TileEditor
from dpt.engine.graphics.blocks import *
from dpt.engine.graphics.enemies import *
from dpt.engine.loader import RessourceLoader
from dpt.game import Game
import pygame
import math


#          {"x, y": {"blockClass": Classe}}
class TileManager:
    enemyGroup = pygame.sprite.Group()
    environmentGroup = pygame.sprite.Group()
    ghostBlockGroup = pygame.sprite.Group()

    log = Game.get_logger("TileManager")
    levelName = None
    maxWidthSize = 0
    maxHeightSize = 0
    coords = None
    camera = None
    editorCamera = None
    Game.availableTiles = {"blockClass": ["Block", "CeciEstUnBlock"], "enemyClass": ["EnemySprite"]}

    @classmethod
    def loadLevel(cls, levelName):
        if type(levelName) == str:
            cls.log.info("Loading level " + levelName)
            level = RessourceLoader.get(levelName)
        else:
            cls.log.info("Loading unknown level")
            level = levelName
        cls.maxWidthSize = 0
        cls.maxHeightSize = 0
        if level is None:
            cls.log.critical("The level can't be loaded")
        for keys in level:
            cls.coords = tuple(map(int, keys.split(", ")))
            if cls.coords[0] > cls.maxWidthSize:
                cls.maxWidthSize = cls.coords[0]
            elif cls.coords[1] > cls.maxHeightSize:
                cls.maxHeightSize = cls.coords[1]
            if cls.coords[0] < 0 or cls.coords[1] < 0:
                cls.log.warning("The tile position can't be negative : " + keys)
                continue
            for key, data in level[keys].items():
                if key == "blockClass":
                    try:
                        block = eval(data + "(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
                        cls.log.debug("Tile " + data + " placed at " + keys)
                        cls.environmentGroup.add(block)
                    except NameError:
                        cls.log.warning("Invalid class name : " + data + " for tile : " + keys)
                elif key == "enemyClass":
                    try:
                        enemy = eval(data + "(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
                        cls.log.debug("Entity " + data + " placed at " + keys)
                        cls.enemyGroup.add(enemy)
                    except NameError:
                        cls.log.warning("Invalid class name : " + data + " for tile : " + keys)
        cls.environmentGroup.draw(Game.surface)
        cls.enemyGroup.draw(Game.surface)
        if not TileEditor.inEditor:
            from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
            Game.playerSprite = PlayerSprite(300, Game.surface.get_size()[1] - 500, 64, 64)
            Game.playerGroup.add(Game.playerSprite)
            cls.camera = Camera(TileManager.maxWidthSize, TileManager.maxHeightSize)
        elif TileEditor.inEditor:
            from dpt.engine.graphics.gui.editor.charEntity import CharEntity
            Game.playerSprite = CharEntity()
            Game.playerGroup.add(Game.playerSprite)
            cls.editorCamera = EditorCamera(TileManager.maxWidthSize, TileManager.maxHeightSize)
        cls.log.info("Done")

    @classmethod
    def ghostBlock(cls, xTile, yTile, itemClass, classType):
        if classType == "blockClass":
            ghostBlock = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 80)")
            TileEditor.ghostBlockGroup.add(ghostBlock)
        elif classType == "enemyClass":
            ghostBlock = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 80)")
            TileEditor.ghostBlockGroup.add(ghostBlock)

    @classmethod
    def placeBlock(cls, xTile, yTile, itemClass, classType):
        if classType == "blockClass":
            block = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
            cls.log.debug("Tile " + itemClass + " placed at " + str(xTile) + ", " + str(yTile))
            cls.environmentGroup.add(block)
        elif classType == "enemyClass":
            enemy = eval(itemClass + "(xTile * Game.TILESIZE, yTile * Game.TILESIZE, Game.TILESIZE, Game.TILESIZE, 255)")
            cls.log.debug("Tile " + itemClass + " placed at " + str(xTile) + ", " + str(yTile))
            cls.enemyGroup.add(enemy)

    @classmethod
    def openTilePanel(cls):
        panel = EditorPanel((255, 255, 255), Game.surface.get_size()[0] / 4 * 3, 0, Game.surface.get_size()[0] / 4, Game.surface.get_size()[1], 120)
        EditorPanel.editorPanelGroup.add(panel)
        startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
        starty = 0 + 32
        for key, value in Game.availableTiles.items():
            for element in value:
                sprite = eval(element + "(startx, starty, Game.TILESIZE, Game.TILESIZE, 255)")
                Game.editorTileRegistry[str(math.floor(startx / Game.TILESIZE)) + ", " + str(math.floor(starty / Game.TILESIZE))] = {"itemClass": element, "classType": key}
                startx += Game.TILESIZE
                if math.floor(startx) >= Game.surface.get_size()[0] - Game.TILESIZE:
                    startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
                    starty += Game.TILESIZE
                EditorPanel.editorPanelGroup.add(sprite)

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
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x



class EditorCamera:
    def __init__(self, width, height):
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("EditorCamera")
        self.last_x = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)
        x = min(0, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.enemyGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x

    def enableGrid(self):
        for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
        for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))