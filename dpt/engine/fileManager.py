import json
import os
import tkinter as tk
from tkinter import filedialog

from dpt.engine.scenes import Scenes
from dpt.engine.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game
from dpt.engine.loader import UnreachableRessourceError


class FileManager:
    log = Game.get_logger(__name__)
    defaultDir = os.path.join(Game.ROOT_DIRECTORY, "ressources", "user", "levels")

    @classmethod
    def import_file(cls):
        """Permet de charger un fichier .level.json"""
        try:
            root = tk.Tk()
            root.withdraw()
            rfile = filedialog.askopenfilename(parent=root, title="Sélectionner un niveau", filetypes=[("Fichier de niveau DPT", "*.level.json"), ("Tous les fichiers", "*")], initialdir=cls.defaultDir)
            try:
                with open(rfile) as f:
                    data = json.load(f)
                    wfile = str(cls.defaultDir) + "/" + str(os.path.basename(rfile))
                    with open(wfile, "w") as fw:
                        data2 = json.dumps(data, indent=4)
                        fw.write(data2)
                    RessourceLoader.RESSOURCES["user.levels." + str(os.path.basename(rfile)).split(".")[0]] = wfile
                    RessourceLoader.add_pending("user.levels." + str(os.path.basename(rfile)).split(".")[0])
                    RessourceLoader.load()
                    TileManager.load_level("user.levels." + str(os.path.basename(rfile)).split(".")[0])
                    cls.log.info("Successfully loaded : " + str(rfile))
                    root.destroy()
            except UnreachableRessourceError and FileNotFoundError:
                cls.log.warning("Unable to load file : " + str(rfile))
                root.destroy()
        except json.decoder.JSONDecodeError as ex:
            Scenes.return_error("Impossible de charger le niveau", "Détails :", "json.decoder.JSONDecodeError: ", str(ex))

    @classmethod
    def save_file(cls, level):
        """Permet de sauvegarder un niveau

        :param level: Niveau
        :type level: dict
        """
        root = tk.Tk()
        root.withdraw()

        file = filedialog.asksaveasfilename(parent=root, title="Sauvegarder un niveau", filetypes=[("Fichier de niveau DPT", "*.level.json")], defaultextension=".level.json", initialdir=cls.defaultDir)
        print(file)
        try:
            with open(file, "w") as f:
                data = json.dumps(level, indent=4)
                f.write(data)
                cls.log.info("Level saved at : " + str(file))
                root.destroy()
        except:
            cls.log.warning("Unable to save file : " + str(file))
            root.destroy()
