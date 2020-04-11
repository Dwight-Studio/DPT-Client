import math

import pygame

from dpt.engine.graphics.gui.editor import EditorPanel
from dpt.game import Game


class TileEditor:
    opushed = False
    spushed = False
    npushed = False
    tpushed = False
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
        from dpt.engine.graphics.tileManager import TileManager
        if cls.inEditor:
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
                        EditorPanel.editorPanelGroup.empty()
                        cls.panelOpen = False
                    elif not keys[pygame.K_t] and cls.tpushed:
                        cls.tpushed = False
            # Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            cls.mousePosX = math.floor((mouse[0] - TileManager.editorCamera.last_x) / Game.TILESIZE)
            cls.mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            if cls.mousePosX != cls.lastMousePosX or cls.mousePosY != cls.lastMousePosY:
                cls.lastMousePosX = None
                cls.lastMousePosY = None
                TileEditor.ghostBlockGroup.empty()
                TileManager.ghostBlock((cls.mousePosX * Game.TILESIZE) + TileManager.editorCamera.last_x, cls.mousePosY * Game.TILESIZE, Game.selectedItem)
                if mouseButtons[0] == 1:
                    if not cls.panelOpen or cls.mousePosX <= math.floor(((Game.surface.get_size()[0] / 4 * 3 - Game.TILESIZE) - TileManager.editorCamera.last_x) / Game.TILESIZE):
                        cls.lastMousePosX = cls.mousePosX
                        cls.lastMousePosY = cls.mousePosY
                        TileManager.placeBlock(cls.mousePosX, cls.mousePosY, Game.selectedItem)
                        cls.createdLevel[str(cls.mousePosX) + ", " + str(cls.mousePosY)] = {"class": Game.selectedItem}
