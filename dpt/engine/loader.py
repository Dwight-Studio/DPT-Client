import math
import os
import sys
import traceback
import json

import psutil
import pygame
import runpy
import gc

from dpt.game import Game

RESSOURCES_DIRECTORY = Game.ROOT_DIRECTORY + "/ressources/"


class UnreachableRessourceError(Exception):
    def __init__(self, val):
        if val:
            self.message = f"'{val}'"
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "No specified value"


def make_entries(path):
    """Génère une liste formatée des fichiers et sous-dossiers d'un dossier.

    :param path: Chemin à utiliser
    :type path: str
    :return: Liste des fichiers et dossiers formatés
    :rtype: list
    """
    rlist = []
    for item in os.listdir(path):
        if os.path.isdir(path + "/" + item):
            for item2 in make_entries(path + "/" + item):
                if os.path.basename(path) == '':
                    rlist.append((item2[0].lower(), item2[1]))
                else:
                    rlist.append((os.path.basename(path).lower() + "." + item2[0], item2[1]))
        elif os.path.isfile(path + "/" + item):
            if os.path.basename(path) == '':
                rlist.append((os.path.splitext(item)[0].lower(), path + "/" + item))
            else:
                rlist.append((os.path.basename(path).lower() + "." + os.path.splitext(item)[0], path + "/" + item))
    return rlist


class RessourceLoader:
    """Gestionnaire des ressources"""
    RESSOURCES = {}
    pending_ressources = {}
    loaded_ressources_entries = None
    loaded_ressources = {}
    logger = Game.get_logger(__name__)

    @classmethod
    def init(cls):
        """Initialise le module RessourceLoader"""
        cls.logger.info("Initializing registries")

        cls.logger.info("Building RESSOURCES registry")
        cls.RESSOURCES = {}
        for entry in make_entries(RESSOURCES_DIRECTORY):
            key = entry[0]
            if key.split(".")[-1] == "level":
                key = ".".join(key.split(".")[:-1])
            elif key.split(".")[-1] == "block":
                key = ".".join(key.split(".")[:-1])
            elif key.split(".")[-1] == "entity":
                key = ".".join(key.split(".")[:-1])
            elif key.split(".")[-1] == "music":
                key = ".".join(key.split(".")[:-1])
            cls.RESSOURCES[key] = entry[1]
        cls.logger.info("Registered " + str(len(cls.RESSOURCES)) + " entries")

        cls.logger.info("Building pending_ressources registry")
        cls.pending_ressources = {}
        cls.logger.info("Registered " + str(len(cls.pending_ressources)) + " entries")

        cls.logger.info("Building loaded_ressources registry")
        cls.loaded_ressources = {}
        cls.logger.info("Registered " + str(len(cls.loaded_ressources)) + " entries")
        if len(cls.loaded_ressources) > 0:
            cls.logger.warning("Bad registration: no ressources must be loaded at startup")

        cls.logger.info("Initialization done")

    @classmethod
    def reload(cls):
        """Recharge les ressources"""
        cls.logger.info("Reloading ressources")
        if cls.loaded_ressources_entries is None:
            cls.logger.warning("Can't reload: no loaded entries found")
            return
        cls.unload()
        cls.init()
        cls.pending_ressources = cls.loaded_ressources_entries.copy()
        cls.loaded_ressources_entries = {}
        cls.load()

    @classmethod
    def load(cls):
        """Charge toutes les ressources préalablement ajouté avec `RessourceLoader.add_pending()`"""
        from dpt.engine.gui.menu.progressbar import ProgressBar
        from dpt.engine.webCommunications import WebCommunication

        before_load_nb = len(cls.loaded_ressources)
        cls.logger.info("Starting loading ressources")
        cls.pending_ressources = {key: value for key, value in cls.pending_ressources.items() if
                                  key not in cls.loaded_ressources}
        current = 0
        total = len(cls.pending_ressources)
        pbar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_BARFRAME.png")
        bar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_COLORBAR_2.png")
        bg = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/environment/background/default_sky.png").convert_alpha()
        bg = pygame.transform.smoothscale(bg, (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        width = min(Game.WINDOW_WIDTH - 50, 1115)
        height = min(math.floor(52 / 1115 * width), 52)
        pb = ProgressBar(math.floor(Game.WINDOW_WIDTH / 2 - width / 2),
                         math.floor(Game.WINDOW_HEIGHT - height), width, height, pbar, bar, total)
        font = pygame.font.SysFont("arial", math.floor(20 * Game.DISPLAY_RATIO))

        for entry in cls.pending_ressources:
            ext = cls.pending_ressources[entry].split("/")[-1].split(".")
            try:
                if ext[-1] == "png":
                    cls.loaded_ressources[entry] = pygame.image.load(cls.pending_ressources[entry]).convert_alpha()
                elif ext[-2] == "level" and ext[-1] == "json":
                    table = None
                    file = open(cls.pending_ressources[entry], "r")
                    table = json.loads(file.read())
                    file.close()
                    cls.loaded_ressources[entry] = table
                elif ext[-2] == "block" and ext[-1] == "py":
                    module = runpy.run_path(cls.pending_ressources[entry])
                    try:
                        cls.loaded_ressources[entry] = module[ext[-3]]
                    except KeyError:
                        cls.logger.warning("Can't find class " + module[ext[-3]])
                        cls.logger.warning("Can't load entry " + entry)
                        continue
                elif ext[-2] == "entity" and ext[-1] == "py":
                    module = runpy.run_path(cls.pending_ressources[entry])
                    cls.loaded_ressources[entry] = module[ext[-3]]
                elif ext[-1] == "ogg" and ext[-2] == "music":
                    cls.loaded_ressources[entry] = cls.pending_ressources[entry]
                elif ext[-1] == "ogg" and ext[-2] != "music":
                    cls.loaded_ressources[entry] = pygame.mixer.Sound(cls.pending_ressources[entry])
                elif ext[-1] == "otf":
                    cls.loaded_ressources[entry] = cls.pending_ressources[entry]
                else:
                    cls.logger.warning("Entry " + entry + " invalid")
                    continue
                cls.logger.debug("Entry " + entry + " loaded")

            except Exception as ex:
                cls.logger.warning("Can't load entry " + entry)
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                for ms in trace.split("\n"):
                    cls.logger.warning(ms)

            current += 1
            pb.value = current

            Game.surface.blit(bg, (0, 0))

            ProgressBar.progress_bar_group.update()
            ProgressBar.bar_group.update()
            ProgressBar.bar_group.draw(Game.surface)
            ProgressBar.progress_bar_group.draw(Game.surface)

            text = font.render(entry, True, (0, 0, 0))
            rect = text.get_rect()
            rect.centerx = Game.WINDOW_WIDTH // 2
            rect.centery = math.floor(Game.WINDOW_HEIGHT - height / 2)
            Game.surface.blit(text, rect)

            Game.events = pygame.event.get()
            Game.add_debug_info("PERFORMANCES INFORMATIONS")
            Game.add_debug_info("CPU load: " + str(psutil.cpu_percent()) + "%")
            Game.add_debug_info("Memory usage: " + str(psutil.virtual_memory().percent) + "%")
            Game.add_debug_info(str(math.floor(Game.clock.get_fps())) + " FPS")
            Game.add_debug_info("----------")

            WebCommunication.update()

            Game.display_debug_info()
            Game.window.update()

        pb.bar.kill()
        pb.kill()
        cls.logger.info("Loaded " + str(len(cls.loaded_ressources) - before_load_nb) + " entries (" + str(len(cls.pending_ressources)) + " were requested)")
        cls.logger.info("Loading done")
        cls.loaded_ressources_entries = cls.pending_ressources.copy()
        cls.pending_ressources = {}

    @classmethod
    def unload(cls):
        """Décharge toutes les ressources actuellement chargées"""
        bf = str(psutil.virtual_memory().percent)
        del cls.loaded_ressources
        gc.collect()
        cls.loaded_ressources = {}
        cls.logger.info("Unloaded all ressources")
        cls.logger.debug("Memory: " + bf + "% before, " + str(psutil.virtual_memory().percent) + "% after")

    @classmethod
    def select_entries(cls, path):
        """Génère une liste d'entrées correspondantes à un chemin

        :param path: Chemin à utiliser
        :type path: str, list

        :return: Liste d'entrées correspondantes au chemin
        :rtype: list
        """
        if isinstance(path, list):
            r = []
            for i in path:
                r.extend(cls.select_entries(i))
            return r

        if path[-1] == "*":
            path = path[:-1]
        entries = []
        for entry in cls.RESSOURCES:
            if entry[:len(path)] == path:
                entries.append(entry)
                entries.sort()
        return entries

    @classmethod
    def get_multiple(cls, path):
        """Permet de récuper plusieurs ressources

        :param path: Chemin à utiliser
        :type path: str, list

        :raise UnreachableRessourceError: Les ressources ne peuvent être atteintes (non chargée / manquante)

        :return: Liste de ressources correspondantes sans arrangement particulier
        :rtype: list
        """
        try:
            rlist = []

            if isinstance(path, list):
                for i in range(len(path)):
                    path[i] = path[i].lower()
            else:
                path = path.lower()

            entries = cls.select_entries(path)
            for path in entries:
                rlist.append(cls.loaded_ressources[path])
            return rlist
        except KeyError:
            cls.logger.critical(f"Ressources for path {str(path)} can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(path.lower())

    @classmethod
    def get(cls, entry):
        """Permet de récuper plusieurs ressources

        :param entry: Nom de l'entrée
        :type entry: str

        :raise UnreachableRessourceError: La ressource ne peut être atteinte (non chargée / manquante)

        :return: Ressource correspondante
        """
        try:
            return cls.loaded_ressources[entry.lower()]
        except KeyError:
            cls.logger.critical(f"Ressource for entry {entry.lower()} can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry.lower())

    @classmethod
    def add_pending(cls, path):
        """Ajoute une entrée (ou plusieurs, selon le chemin donné)

        :param path: Chemin à utiliser
        :type path: str

        :raise UnreachableRessourceError: Le chemin ne renvois aucune entrée
        """
        try:
            rlist = []

            if isinstance(path, list):
                for i in range(len(path)):
                    path[i] = path[i].lower()
            else:
                path = path.lower()

            entries = cls.select_entries(path)
            if len(entries) == 0:
                if isinstance(path, list):
                    cls.logger.warning("The requested selector (" + ", ".join(path) + ") did not find any entries, it may cause exceptions but ignoring")
                else:
                    cls.logger.warning("The requested selector (" + path + ") did not find any entries, it may cause exceptions but ignoring")
            for path in entries:
                cls.pending_ressources[path] = cls.RESSOURCES[path]
        except KeyError:
            cls.logger.critical("Ressource can't be added to pending ressources (path doesn't exist)")
            raise UnreachableRessourceError(path)
