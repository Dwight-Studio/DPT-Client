import pygame
import math
import pygame
from dpt.engine.gui.editor.editorPanel import EditorPanel
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.game import Game


class TileEditor:
    opushed = False
    spushed = False
    npushed = False
    tpushed = False
    mousePushedL = False
    mousePushedR = False
    panelOpen = False
    inEditor = False
    mousePosX = None
    mousePosY = None
    lastMousePosX = None
    lastMousePosY = None
    ghostBlockGroup = pygame.sprite.Group()
    createdLevel = {}

    @classmethod
    def update(cls):
        from dpt.engine.tileManager import TileManager
        if cls.inEditor:
            Game.isPlayerDead = True
            TileManager.editorCamera.enableGrid()
            # Gestion des fichiers (raccourcis)
            mouseButtons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            keysmods = pygame.key.get_mods()
            for key in keys:
                # Ouvrir un fichier
                if keysmods == 4160 or keysmods == 4224:
                    if keys[pygame.K_o] and not cls.opushed:
                        cls.opushed = True
                        from dpt.engine.fileManager import FileManager
                        FileManager.importFile()
                    elif not keys[pygame.K_o] and cls.opushed:
                        cls.opushed = False
                    # Sauvegarder un fichier
                    if keys[pygame.K_s] and not cls.spushed:
                        cls.spushed = True
                        from dpt.engine.fileManager import FileManager
                        FileManager.saveFile(cls.createdLevel)
                    elif not keys[pygame.K_s] and cls.spushed:
                        cls.spushed = False
                    if keys[pygame.K_n] and not cls.npushed:
                        cls.npushed = True
                        TileManager.environmentGroup.empty()
                        TileManager.entityGroup.empty()
                        cls.createdLevel = {}
                    elif not keys[pygame.K_n] and cls.npushed:
                        cls.npushed = False
                    if keys[pygame.K_t] and not cls.tpushed and not cls.panelOpen:
                        cls.tpushed = True
                        cls.panelOpen = True
                        TileManager.openTilePanel()
                    elif keys[pygame.K_t] and not cls.tpushed and cls.panelOpen:
                        cls.tpushed = True
                        TileManager.editorPanelGroup.empty()
                        Checkbox.checkboxGroup.empty()
                        cls.panelOpen = False
                    elif not keys[pygame.K_t] and cls.tpushed:
                        cls.tpushed = False
            # Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            cls.mousePosX = math.floor((mouse[0] - TileManager.editorCamera.last_x) / Game.TILESIZE)
            cls.mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            Game.add_debug_info("MOUSE INFORMATIONS")
            Game.add_debug_info("Mouse X: " + str(mouse[0]))
            Game.add_debug_info("Mouse Y: " + str(mouse[1]))
            Game.add_debug_info("")
            Game.add_debug_info("Mouse AbsX: " + str(cls.mousePosX))
            Game.add_debug_info("Mouse AbsY: " + str(cls.mousePosY))
            Game.add_debug_info("----------")

            if cls.mousePosX != cls.lastMousePosX or cls.mousePosY != cls.lastMousePosY:
                cls.lastMousePosX = None
                cls.lastMousePosY = None
                TileEditor.ghostBlockGroup.empty()
                TileManager.ghostBlock((cls.mousePosX * Game.TILESIZE) + TileManager.editorCamera.last_x, cls.mousePosY * Game.TILESIZE, Game.selectedItem)

            if mouseButtons[0] == 1 or mouseButtons[1] == 1 or mouseButtons[2] == 1:
                for btn in Button.buttonsGroup:
                    if btn.rect.collidepoint(mouse[0], mouse[1]):
                        return

            if mouseButtons[0] == 1 and not cls.mousePushedL:
                cls.mousePushedL = True
                if not cls.panelOpen or cls.mousePosX <= math.floor(((Game.surface.get_size()[0] / 4 * 3 - Game.TILESIZE) - TileManager.editorCamera.last_x) / Game.TILESIZE):
                    cls.lastMousePosX = cls.mousePosX
                    cls.lastMousePosY = cls.mousePosY
                    if not TileManager.checkBack:
                        if str(cls.mousePosX) + ", " + str(cls.mousePosY) in cls.createdLevel:
                            cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)]["class"] = Game.selectedItem
                        else:
                            cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)] = {"class": Game.selectedItem}
                        TileManager.placeBlock(cls.mousePosX, cls.mousePosY, Game.selectedItem)
                    elif TileManager.checkBack:
                        if str(cls.mousePosX) + ", " + str(cls.mousePosY) in cls.createdLevel:
                            cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)]["backgroundClass"] = Game.selectedItem
                        else:
                            cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)] = {"backgroundClass": Game.selectedItem}
                        TileManager.placeBackBlock(cls.mousePosX, cls.mousePosY, Game.selectedItem)
            elif mouseButtons[0] != 1 and cls.mousePushedL:
                cls.mousePushedL = False
            elif mouseButtons[0] == 1 and cls.mousePosX != cls.lastMousePosX or cls.mousePosY != cls.lastMousePosY and cls.mousePushedL:
                cls.mousePushedL = False
            if mouseButtons[2] == 1 and not cls.mousePushedR:
                cls.mousePushedR = True
                if not cls.panelOpen or cls.mousePosX <= math.floor(((Game.surface.get_size()[0] / 4 * 3 - Game.TILESIZE) - TileManager.editorCamera.last_x) / Game.TILESIZE):
                    cls.lastMousePosX = cls.mousePosX
                    cls.lastMousePosY = cls.mousePosY
                    try:
                        for blocks in TileManager.backgroundBlocks:
                            if math.floor(blocks.rect.centerx / Game.TILESIZE) == cls.mousePosX and math.floor(blocks.rect.centery / Game.TILESIZE) == cls.mousePosY:
                                blocks.kill()
                                del blocks
                        for blocks in TileManager.environmentGroup:
                            if math.floor(blocks.rect.centerx / Game.TILESIZE) == cls.mousePosX and math.floor(blocks.rect.centery / Game.TILESIZE) == cls.mousePosY:
                                blocks.kill()
                                del blocks
                        for entity in TileManager.entityGroup:
                            if math.floor(entity.rect.centerx / Game.TILESIZE) == cls.mousePosX and math.floor(entity.rect.centery / Game.TILESIZE) == cls.mousePosY:
                                entity.kill()
                                del entity
                        del cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)]
                    except KeyError:
                        pass
            elif mouseButtons[1] != 1 and cls.mousePushedR:
                cls.mousePushedR = False
            elif mouseButtons[1] == 1 and cls.mousePosX != cls.lastMousePosX or cls.mousePosY != cls.lastMousePosY and cls.mousePushedR:
                cls.mousePushedR = False