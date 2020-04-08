import pygame
import math
from dpt.engine.fileManager import *


class TileEditor:
    def __init__(self):
        self.file = FileManager()
        self.opushed = False
        self.spushed = False
        self.npushed = False
        self.inEditor = False
        self.mousePosX = None
        self.mousePosY = None
        self.lastMousePosX = None
        self.lastMousePosY = None
        self.createdLevel = {}
        self.itemClass = "EnemySprite"
        self.classType = "enemyClass"

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
                        Game.platforms.empty()
                        self.createdLevel = {}
                    elif not keys[pygame.K_n] and self.npushed:
                        self.npushed = False
            #Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            self.mousePosX = math.floor(mouse[0] / Game.TILESIZE)
            self.mousePosY = math.floor(mouse[1] / Game.TILESIZE)
            self.lastMousePosX = None
            self.lastMousePosY = None
            if self.mousePosX != self.lastMousePosX and self.mousePosY != self.lastMousePosY:
                Game.ghostBlock.empty()
                pushed = False
                Game.tile.ghostBlock(self.mousePosX, self.mousePosY, self.itemClass, self.classType)
                self.lastMousePosX = self.mousePosX
                self.lastMousePosY = self.mousePosY
                if mouseButtons[0] == 1 and not pushed:
                    pushed = True
                    Game.tile.placeBlock(self.mousePosX, self.mousePosY, self.itemClass, self.classType)
                    self.createdLevel[str(self.mousePosX) + ", " + str(self.mousePosY)] = {self.classType: self.itemClass}