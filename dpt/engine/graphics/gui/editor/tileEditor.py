import pygame
import math
from dpt.engine.fileManager import *


class TileEditor:
    def __init__(self):
        self.file = FileManager()
        self.opushed = False
        self.spushed = False
        self.npushed = False
        self.tpushed = False
        self.panelOpen = False
        self.inEditor = False
        self.mousePosX = None
        self.mousePosY = None
        self.lastMousePosX = None
        self.lastMousePosY = None
        self.createdLevel = {}

    def update(self):
        if self.inEditor:
            Game.camera.enableGrid()
            # Gestion des fichiers (raccourcis)
            mouseButtons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            keysmods = pygame.key.get_mods()
            for key in keys:
                # Ouvrir un fichier
                if keysmods == 4160 or keysmods == 4224:
                    if keys[pygame.K_o] and not self.opushed:
                        self.opushed = True
                        self.file.importFile()
                    elif not keys[pygame.K_o] and self.opushed:
                        self.opushed = False
                # Sauvegarder un fichier
                    if keys[pygame.K_s] and not self.spushed:
                        self.spushed = True
                        self.file.saveFile(self.createdLevel)
                    elif not keys[pygame.K_s] and self.spushed:
                        self.spushed = False
                    if keys[pygame.K_n] and not self.npushed:
                        self.npushed = True
                        Game.environment.empty()
                        self.createdLevel = {}
                    elif not keys[pygame.K_n] and self.npushed:
                        self.npushed = False
                    if keys[pygame.K_t] and not self.tpushed and not self.panelOpen:
                        self.tpushed = True
                        self.panelOpen = True
                        Game.tile.openTilePanel()
                    elif keys[pygame.K_t] and not self.tpushed and self.panelOpen:
                        self.tpushed = True
                        Game.editorPanel.empty()
                        self.panelOpen = False
                    elif not keys[pygame.K_t] and self.tpushed:
                        self.tpushed = False
            #Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            self.mousePosX = math.floor(mouse[0] / Game.TILESIZE)
            self.mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            self.lastMousePosX = None
            self.lastMousePosY = None
            if self.mousePosX != self.lastMousePosX and self.mousePosY != self.lastMousePosY:
                Game.ghostBlock.empty()
                lpushed = False
                Game.tile.ghostBlock(self.mousePosX, self.mousePosY, Game.itemClass, Game.classType)
                self.lastMousePosX = self.mousePosX
                self.lastMousePosY = self.mousePosY
                if mouseButtons[0] == 1 and not lpushed:
                    lpushed = True
                    if not self.panelOpen or self.mousePosX <= math.floor((Game.surface.get_size()[0] / 4 * 3 - Game.TILESIZE) / Game.TILESIZE):
                        Game.tile.placeBlock(self.mousePosX, self.mousePosY, Game.itemClass, Game.classType)
                        self.createdLevel[str(self.mousePosX) + ", " + str(self.mousePosY)] = {Game.classType: Game.itemClass}