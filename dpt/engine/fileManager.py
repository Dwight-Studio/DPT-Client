import tkinter as tk
import json
import os
from dpt.game import Game
from tkinter import filedialog


class FileManager:
    def __init__(self):
        self.log = Game.get_logger("FileManager")
        self.defaultDir = os.path.join(Game.ROOT_DIRECTORY, "dpt", "ressources", "user", "levels")

    def importFile(self):
        root = tk.Tk()
        root.withdraw()
        rfile = filedialog.askopenfilename(parent=root, title="Sélectionner un niveau",
                                               filetypes=[("Fichier de niveau DPT", "*.level.json"),
                                                          ("Tous les fichiers", "*")], initialdir=self.defaultDir)
        try:
            with open(rfile) as f:
                data = json.load(f)
                # wfile = str(self.defaultDir) + "/" + str(os.path.basename(rfile))
                # with open(wfile, "w") as fw:
                #     data2 = json.dumps(data, indent=4)
                #     fw.write(data2)
                Game.environmentGroup.empty()
                #Game.camera.enableGrid()
                Game.tile.loadLevel(data)
                self.log.info("Successfully loaded : " + str(rfile))
                root.destroy()
        except:
            self.log.warning("Unable to load file : " + str(rfile))
            root.destroy()

    def saveFile(self, level):
        root = tk.Tk()
        root.withdraw()
        print(self.defaultDir)
        file = filedialog.asksaveasfilename(parent=root, title="Sauvegarder un niveau",
                                                filetypes=[("Fichier de niveau DPT", "*.level.json")], defaultextension=".level.json", initialdir=self.defaultDir)
        try:
            with open(file, "w") as f:
                data = json.dumps(level, indent=4)
                f.write(data)
                self.log.info("Level saved at : " + str(file))
                root.destroy()
        except:
            self.log.warning("Unable to save file : " + str(file))
            root.destroy()