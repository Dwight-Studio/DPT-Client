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
    usedResources = []
    coords = None
    camera = None
    editorCamera = None
    Game.availableTiles = []
    Game.availableTiles.extend(RessourceLoader.select_entries("dpt.blocks.*"))
    Game.availableTiles.remove("dpt.blocks.notfound")
    Game.availableTiles.extend(RessourceLoader.select_entries("dpt.entities.*"))

    @classmethod
    def loadLevel(cls, levelName):
        Game.playerGroup.empty()
        TileManager.editorPanelGroup.empty()
        TileEditor.ghostBlockGroup.empty()

        for entity in TileManager.entityGroup:
            entity.kill()

        for block in TileManager.environmentGroup:
            block.kill()

        for block in TileManager.backgroundBlocks:
            block.kill()

        if TileEditor.inEditor:
            RessourceLoader.add_pending("*")
            RessourceLoader.load()

        if type(levelName) == str:
            cls.log.info("Loading level " + levelName)
            if not TileEditor.inEditor:
                cls.log.debug("Loading level main file")
                RessourceLoader.add_pending(levelName)
                RessourceLoader.load()
            level = RessourceLoader.get(levelName)
        else:
            cls.log.info("Loading unknown level")
            level = levelName
        cls.maxWidthSize = 0
        cls.maxHeightSize = 0
        if level is None:
            cls.log.critical("The level can't be loaded")

        if not TileEditor.inEditor:
            cls.log.debug("Loading level blocks and entities")
            for keys in level:
                if "class" in level[keys]:
                    RessourceLoader.add_pending(level[keys]["class"])
                if "backgroundClass" in level[keys]:
                    RessourceLoader.add_pending(level[keys]["backgroundClass"])
            RessourceLoader.load()

        if not TileEditor.inEditor:
            cls.log.debug("Loading textures")
            for keys in level:
                if "class" in level[keys]:
                    obj = RessourceLoader.get(level[keys]["class"])
                    RessourceLoader.add_pending(obj.texture)
                    if hasattr(obj, "textures"):
                        RessourceLoader.add_pending(obj.textures)
                if "backgroundClass" in level[keys]:
                    obj = RessourceLoader.get(level[keys]["backgroundClass"])
                    RessourceLoader.add_pending(obj.texture)
                    if hasattr(obj, "textures"):
                        RessourceLoader.add_pending(obj.textures)

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
                if "customPlace" in level[keys]:
                    try:
                        RessourceLoader.get(level[keys]["class"])(cls.coords[0], cls.coords[1])
                        cls.log.debug("Tile " + level[keys]["class"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["class"] + " for tile : " + keys)
                else:
                    try:
                        RessourceLoader.get(level[keys]["class"])(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE)
                        cls.log.debug("Tile " + level[keys]["class"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["class"] + " for tile : " + keys)
            if "backgroundClass" in level[keys]:
                if "customPlace" in level[keys]:
                    try:
                        BackgroundFakeBlocks(cls.coords[0], cls.coords[1], level[keys]["backgroundClass"])
                        cls.log.debug("Background tile " + level[keys]["backgroundClass"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["backgroundClass"] + " for tile : " + keys)
                else:
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
        Game.isPlayerDead = False
        cls.log.info("Done")

    @classmethod
    def ghostBlock(cls, xTile, yTile, item):
        from dpt.engine.ghostFakeEntities import GhostFakeEntity
        ghostBlock = GhostFakeEntity(xTile, yTile, 80, item)

    @classmethod
    def placeBlock(cls, xTile, yTile, item):
        if not TileEditor.customTilePlacement:
            RessourceLoader.get(item)(xTile * Game.TILESIZE, yTile * Game.TILESIZE)
            cls.log.debug("Tile " + item + " placed at " + str(xTile) + ", " + str(yTile))
        elif TileEditor.customTilePlacement:
            RessourceLoader.get(item)(xTile, yTile)
            cls.log.debug("Tile " + item + " placed at " + str(xTile) + ", " + str(yTile))
    @classmethod
    def placeBackBlock(cls, xTile, yTile, item):
        if not TileEditor.customTilePlacement:
            BackgroundFakeBlocks(xTile * Game.TILESIZE, yTile * Game.TILESIZE, item)
            cls.log.debug("Background tile " + item + " placed at " + str(xTile) + ", " + str(yTile))
        elif TileEditor.customTilePlacement:
            BackgroundFakeBlocks(xTile, yTile, item)
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
        if TileEditor.panelOpen:
            cls.nbSkip += cls.nbPerLine
            TileManager.openTilePanel()

    @classmethod
    def scrollUp(cls):
        if TileEditor.panelOpen:
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

    @classmethod
    def get_sprite_count(cls):
        return len(cls.backgroundBlocks) + len(cls.entityGroup) + len(cls.environmentGroup)

class Camera:
    def __init__(self, width, height):
        self.userConfirm = True
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("Camera")
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.sprite_count = 0
        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        calcul = (self.width * Game.TILESIZE) - Game.surface.get_size()[0]
        x = min(0, self.last_x, x)
        x = max(-calcul, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        for sprite in TileManager.backgroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.entityGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        self.sprite_count += len(Game.playerGroup)
        self.sprite_count += 1
        if Game.DISPLAY_RECT:
            pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(Game.playerSprite), width=2)
        for sprite in TileManager.deadlyObjectGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foregroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x

        Game.add_debug_info("CAMERA INFORMATIONS")
        Game.add_debug_info("Scrolling: " + str(-self.last_x))
        Game.add_debug_info("Right: " + str(Game.playerSprite.right))
        Game.add_debug_info("Left: " + str(Game.playerSprite.left))
        Game.add_debug_info("Player X:" + str(target.rect.centerx))
        Game.add_debug_info("Player Y: " + str(target.rect.centery))
        Game.add_debug_info("Displaying " + str(self.sprite_count) + " sprites")
        Game.add_debug_info("   " + str(len(Game.playerGroup)) + " players")
        Game.add_debug_info("   " + str(len(TileManager.entityGroup)) + " entities")
        Game.add_debug_info("   " + str(len(TileManager.environmentGroup)) + " blocks")
        Game.add_debug_info("   " + str(len(TileManager.backgroundBlocks)) + " background blocks")
        Game.add_debug_info("   (" + str(len(TileManager.foregroundBlocks)) + " foreground blocks)")
        Game.add_debug_info("   (" + str(len(TileManager.deadlyObjectGroup)) + " deadly objects)")
        Game.add_debug_info("----------")


class EditorCamera:
    def __init__(self, width, height):
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("EditorCamera")
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.sprite_count = 0
        x = -target.rect.x + int(Game.surface.get_size()[0] / 2)
        x = min(0, x)
        self.camera = pygame.Rect(x, 0, self.width, self.height)
        for sprite in TileManager.backgroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.environmentGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.entityGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        Game.surface.blit(Game.playerSprite.image, self.apply(Game.playerSprite))
        self.sprite_count += len(Game.playerGroup)
        if Game.DISPLAY_RECT:
            pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(Game.playerSprite), width=2)
        for sprite in TileManager.deadlyObjectGroup:
            Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foregroundBlocks:
            Game.surface.blit(sprite.image, self.apply(sprite))
        self.last_x = x

        Game.add_debug_info("CAMERA INFORMATIONS")
        Game.add_debug_info("Scrolling: " + str(-self.last_x))
        Game.add_debug_info("Nb Enemies: " + str(len(TileManager.enemyGroup)))
        Game.add_debug_info("Displaying " + str(self.sprite_count) + " sprites")
        Game.add_debug_info("   " + str(len(Game.playerGroup)) + " players")
        Game.add_debug_info("   " + str(len(TileManager.entityGroup)) + " entities")
        Game.add_debug_info("   " + str(len(TileManager.environmentGroup)) + " blocks")
        Game.add_debug_info("   " + str(len(TileManager.backgroundBlocks)) + " background blocks")
        Game.add_debug_info("   (" + str(len(TileManager.foregroundBlocks)) + " foreground blocks)")
        Game.add_debug_info("   (" + str(len(TileManager.deadlyObjectGroup)) + " deadly objects)")
        Game.add_debug_info("----------")

    def enableGrid(self):
        for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
        for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))
