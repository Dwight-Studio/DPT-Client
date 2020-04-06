import tkinter as tk
import json
import pygame
from dpt.game import Game
from tkinter import filedialog


class FileManager:
    def __init__(self):
        self.file = None

    def openFile(self):
        root = tk.Tk()
        root.withdraw()
        self.file = filedialog.askopenfilename(parent=root, title="Sélectionner un niveau",
                                               filetypes=[("Fichier de niveau DPT", "*.level.json"),
                                                          ("Tous les fichiers", "*")])
        try:
            with open(self.file) as f:
                data = json.load(f)
                print(data)
                Game.platforms.empty()
                #Game.camera.enableGrid()
                Game.tile.loadLevel(data)
        except:
            root.destroy()
