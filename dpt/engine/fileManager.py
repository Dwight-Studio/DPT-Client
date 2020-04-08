import tkinter as tk
import json
import pygame
from dpt.game import Game
from tkinter import filedialog


class FileManager:
    def __init__(self):
        self.log = Game.get_logger("FileManager")
    def openFile(self):
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(parent=root, title="Sélectionner un niveau",
                                               filetypes=[("Fichier de niveau DPT", "*.level.json"),
                                                          ("Tous les fichiers", "*")])
        try:
            with open(file) as f:
                data = json.load(f)
                Game.platforms.empty()
                #Game.camera.enableGrid()
                Game.tile.loadLevel(data)
                self.log.info("Successfully loaded : " + str(file))
                root.destroy()
        except:
            self.log.warning("Unable to load file : " + str(file))
            root.destroy()

    def saveFile(self, level):
        root = tk.Tk()
        root.withdraw()
        file = filedialog.asksaveasfilename(parent=root, title="Sauvegarder un niveau",
                                                filetypes=[("Fichier de niveau DPT", "*.level.json")])
        try:
            with open(file + ".level.json", "w") as f:
                data = json.dumps(level, indent=4)
                f.write(data)
                self.log.info("Level saved at : " + str(file + ".level.json"))
                root.destroy()
        except:
            self.log.warning("Unable to save file : " + str(file + ".level.json"))
            root.destroy()