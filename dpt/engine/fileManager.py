import json
import os
import tkinter as tk
from tkinter import filedialog

from dpt.engine.graphics.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class FileManager:
    log = Game.get_logger("FileManager")
    defaultDir = os.path.join(Game.ROOT_DIRECTORY, "dpt", "ressources", "user", "levels")

    @classmethod
    def importFile(cls):
        root = tk.Tk()
        root.withdraw()
        rfile = filedialog.askopenfilename(parent=root, title="Sélectionner un niveau", filetypes=[("Fichier de niveau DPT", "*.level.json"), ("Tous les fichiers", "*")], initialdir=cls.defaultDir)
        #try:
        with open(rfile) as f:
            data = json.load(f)
            wfile = str(cls.defaultDir) + "/" + str(os.path.basename(rfile))
            with open(wfile, "w") as fw:
                data2 = json.dumps(data, indent=4)
                fw.write(data2)
            TileManager.environmentGroup.empty()
            RessourceLoader.reload()
            TileManager.loadLevel("user.levels." + str(os.path.basename(rfile)).split(".")[0])
            cls.log.info("Successfully loaded : " + str(rfile))
            root.destroy()
        #except:
        #    cls.log.warning("Unable to load file : " + str(rfile))
        #    root.destroy()

    @classmethod
    def saveFile(cls, level):
        root = tk.Tk()
        root.withdraw()
        file = filedialog.asksaveasfilename(parent=root, title="Sauvegarder un niveau", filetypes=[("Fichier de niveau DPT", "*.level.json")], defaultextension=".level.json", initialdir=cls.defaultDir)
        try:
            with open(file, "w") as f:
                data = json.dumps(level, indent=4)
                f.write(data)
                cls.log.info("Level saved at : " + str(file))
                root.destroy()
        except:
            cls.log.warning("Unable to save file : " + str(file))
            root.destroy()
