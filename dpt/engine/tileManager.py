import math
import pygame
from dpt.engine.gui.editor.editorPanel import EditorPanel
from dpt.engine.gui.editor.panelFakeEntities import PanelFakeEntity
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.backgroundFakeBlocks import BackgroundFakeBlocks
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game


#          {"x, y": {"blockClass": Classe}}
class TileManager:
    deadlyObjectGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    environmentGroup = pygame.sprite.Group()
    entityGroup = pygame.sprite.Group()
    editorPanelGroup = pygame.sprite.Group()
    backgroundBlocks = pygame.sprite.Group()
    foregroundBlocks = pygame.sprite.Group()

    log = Game.get_logger("TileManager")
    levelName = None
    maxWidthSize = 0
    maxHeightSize = 0
    count = 0
    alreadyDefined = False
    nbPerLineCount = 0
    nbPerLine = 0
    nbSkip = 0
    checkBack = False
    coords = None
    camera = None
    editorCamera = None
    Game.availableTiles = []
    Game.availableTiles.extend(RessourceLoader.select_entries("dpt.blocks.*"))
    print(Game.availableTiles)
    Game.availableTiles.remove("dpt.blocks.notfound")
    Game.availableTiles.extend(RessourceLoader.select_entries("dpt.entities.*"))

    @classmethod
    def loadLevel(cls, levelName):
        Checkbox.checkboxGroup.empty()
        TileManager.editorPanelGroup.empty()
        Game.playerGroup.empty()
        TileManager.backgroundBlocks.empty()
        TileManager.entityGroup.empty()
        TileEditor.ghostBlockGroup.empty()
        TileManager.deadlyObjectGroup.empty()
        TileManager.foregroundBlocks.empty()

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
            if "class" in level[keys]:
                try:
                    RessourceLoader.get(level[keys]["class"])(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE)
                    cls.log.debug("Tile " + level[keys]["class"] + " placed at " + keys)
                except UnreachableRessourceError:
                    cls.log.warning("Invalid class name : " + level[keys]["class"] + " for tile : " + keys)
            if "backgroundClass" in level[keys]:
                try:
                    BackgroundFakeBlocks(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE,
                                         level[keys]["backgroundClass"])
                    cls.log.debug("Background tile " + level[keys]["backgroundClass"] + " placed at " + keys)
                except UnreachableRessourceError:
                    cls.log.warning("Invalid class name : " + level[keys]["backgroundClass"] + " for tile : " + keys)
        cls.backgroundBlocks.draw(Game.surface)
        cls.environmentGroup.draw(Game.surface)
        cls.entityGroup.draw(Game.surface)
        cls.enemyGroup.draw(Game.surface)
        cls.deadlyObjectGroup.draw(Game.surface)
        if not TileEditor.inEditor:
            from dpt.engine.characters.PlayerSprite import PlayerSprite
            Game.playerSprite = PlayerSprite(300, Game.surface.get_size()[1] - 500)
            Game.playerGroup.add(Game.playerSprite)
            cls.camera = Camera(TileManager.maxWidthSize, TileManager.maxHeightSize)
        elif TileEditor.inEditor:
            from dpt.engine.gui.editor.charEntity import CharEntity
            Game.playerSprite = CharEntity()
            Game.playerGroup.add(Game.playerSprite)
            cls.editorCamera = EditorCamera(TileManager.maxWidthSize, TileManager.maxHeightSize)
        TileEditor.createdLevel = level
        cls.levelName = levelName
        cls.log.info("Done")

    @classmethod
    def ghostBlock(cls, xTile, yTile, item):
        from dpt.engine.ghostFakeEntities import GhostFakeEntity
        ghostBlock = GhostFakeEntity(xTile, yTile, 80, item)

    @classmethod
    def placeBlock(cls, xTile, yTile, item):
        RessourceLoader.get(item)(xTile * Game.TILESIZE, yTile * Game.TILESIZE)
        cls.log.debug("Tile " + item + " placed at " + str(xTile) + ", " + str(yTile))

    @classmethod
    def placeBackBlock(cls, xTile, yTile, item):
        BackgroundFakeBlocks(xTile * Game.TILESIZE, yTile * Game.TILESIZE, item)
        cls.log.debug("Background tile " + item + " placed at " + str(xTile) + ", " + str(yTile))

    @classmethod
    def openTilePanel(cls):
        TileManager.editorPanelGroup.empty()
        Game.editorTileRegistry.clear()
        value = bool(cls.checkBack)
        Checkbox.checkboxGroup.empty()
        cls.checkBack = Checkbox(Game.surface.get_size()[0] // 4 * 3 + Game.TILESIZE // 4, Game.TILESIZE // 4)
        cls.checkBack.value = value
        cls.count = 0
        panel = EditorPanel((255, 255, 255), Game.surface.get_size()[0] / 4 * 3, 0, Game.surface.get_size()[0] / 4, Game.surface.get_size()[1], 120)
        TileManager.editorPanelGroup.add(panel)
        startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
        starty = 0 + Game.TILESIZE
        for element in Game.availableTiles:
            if cls.count == cls.nbSkip:
                sprite = PanelFakeEntity(startx, starty, 255, element)
                Game.editorTileRegistry[str(math.floor(startx / Game.TILESIZE)) + ", " + str(math.floor(starty / Game.TILESIZE))] = {"class": element}
                startx += Game.TILESIZE
                cls.nbPerLineCount += 1
                if math.floor(startx) >= Game.surface.get_size()[0] - Game.TILESIZE:
                    startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
                    starty += Game.TILESIZE
                    if not cls.alreadyDefined:
                        cls.nbPerLine = cls.nbPerLineCount
                        cls.alreadyDefined = True
            else:
                cls.count += 1
                continue

    @classmethod
    def scrollDown(cls):
        cls.nbSkip += cls.nbPerLine
        TileManager.openTilePanel()

    @classmethod
    def scrollUp(cls):
        TileManager.editorPanelGroup.empty()
        Checkbox.checkboxGroup.empty()
        Game.editorTileRegistry.clear()
        if cls.nbSkip > 0:
            cls.nbSkip -= cls.nbPerLine
        TileManager.openTilePanel()

    @classmethod
    def outOfWindow(cls):
        for enemy in TileManager.enemyGroup:
            if enemy.rect.centery >= 3000:
                enemy.kill()
                del enemy

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
        Game.add_debug_info("CAMERA INFORMATIONS")
        Game.add_debug_info("Scrolling: " + str(-self.last_x))
        Game.add_debug_info("Right: " + str(Game.playerSprite.right))
        Game.add_debug_info("Left: " + str(Game.playerSprite.left))
        Game.add_debug_info("Player X:" + str(target.rect.centerx))
        Game.add_debug_info("Player Y: " + str(target.rect.centery))
        Game.add_debug_info("----------")

        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        calcul = (self.width * Game.TILESIZE) - Game.surface.get_size()[0]
        x = min(0, self.last_x, x)
        x = max(-calcul, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        for sprite in TileManager.backgroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.entityGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        if Game.DISPLAY_RECT:
            pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(Game.playerSprite), width=2)
        for sprite in TileManager.deadlyObjectGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foregroundBlocks:
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
        Game.add_debug_info("CAMERA INFORMATIONS")
        Game.add_debug_info("Scrolling: " + str(-self.last_x))
        Game.add_debug_info("Nb Enemies: " + str(len(TileManager.enemyGroup)))
        Game.add_debug_info("----------")
        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)
        x = min(0, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        for sprite in TileManager.backgroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.entityGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        if Game.DISPLAY_RECT:
            pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(Game.playerSprite), width=2)
        for sprite in TileManager.deadlyObjectGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foregroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x

    def enableGrid(self):
        for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
        for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))
