import pygame
from dpt.engine.fileManager import *


class TileEditor:
    def __init__(self):
        self.file = FileManager()
        self.pushed = False

    def update(self):
        # Gestion des fichiers (raccourcis)
        keys = pygame.key.get_pressed()
        keysmods = pygame.key.get_mods()
        for key in keys:
            # Ouvrir un fichier
            if keysmods == 4160 or keysmods == 4224:
                if keys[pygame.K_o] and not self.pushed:
                    print("pressed")
                    self.file.openFile()
                    self.pushed = True
                elif not keys[pygame.K_o] and self.pushed:
                    self.pushed = False
            # Sauvegarder un fichier