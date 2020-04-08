import pygame
import math
from dpt.engine.fileManager import *


class TileEditor:
    def __init__(self):
        self.file = FileManager()
        self.pushed = False
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
                    if keys[pygame.K_o] and not self.pushed:
                        self.pushed = True
                        self.file.openFile()
                    elif not keys[pygame.K_o] and self.pushed:
                        self.pushed = False
                # Sauvegarder un fichier
                    if keys[pygame.K_s] and not self.pushed:
                        self.pushed = True
                        self.file.saveFile(self.createdLevel)
                    elif not keys[pygame.K_s] and self.pushed:
                        self.pushed = False
            #Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            self.mousePosX = math.floor(mouse[0] / Game.TILESIZE)
            self.mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            self.lastMousePosX = None
            self.lastMousePosY = None
            if self.mousePosX != self.lastMousePosX and self.mousePosY != self.lastMousePosY:
                Game.ghostBlock.empty()
                pushed = False
                Game.tile.ghostBlock(self.mousePosX, self.mousePosY, "Block")
                self.lastMousePosX = self.mousePosX
                self.lastMousePosY = self.mousePosY
                if mouseButtons[0] == 1 and not pushed:
                    pushed = True
                    Game.tile.placeBlock(self.mousePosX, self.mousePosY, "Block")
                    self.createdLevel[str(self.mousePosX) + (", ") + str(self.mousePosY)] = {"blockClass": "Block"}

