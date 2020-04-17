import math
import os
import sys
import traceback
import json

import psutil
import pygame
import runpy
import gc

from dpt.engine.gui.menu.bar import Bar
from dpt.engine.gui.menu.progressbar import ProgressBar
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
    RESSOURCES = {}
    pending_ressources = {}
    loaded_ressources_entries = None
    loaded_ressources = {}
    logger = Game.get_logger("Loader")

    @classmethod
    def init(cls):
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
        before_load_nb = len(cls.loaded_ressources)
        cls.logger.info("Starting loading ressources")
        cls.pending_ressources = {key: value for key, value in cls.pending_ressources.items() if key not in cls.loaded_ressources}
        current = 0
        total = len(cls.pending_ressources)
        pbar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_BARFRAME.png")
        bar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_COLORBAR_2.png")
        bg = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/environment/background/default_sky.png")
        bg = pygame.transform.scale(bg, Game.surface.get_size())
        width = min(Game.surface.get_size()[0] - 50, 1115)
        height = min(math.floor(52 / 1115 * width), 52)
        pb = ProgressBar(math.floor(Game.surface.get_size()[0] / 2 - width / 2),
                         math.floor(Game.surface.get_size()[1] - height), width, height, pbar, bar, total)
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

            ProgressBar.progressbarGroup.update()
            Bar.barGroup.update()
            Bar.barGroup.draw(Game.surface)
            ProgressBar.progressbarGroup.draw(Game.surface)

            text = font.render(entry, True, (0, 0, 0))
            rect = text.get_rect()
            rect.centerx = Game.surface.get_size()[0] // 2
            rect.centery = math.floor(Game.surface.get_size()[1] - height / 2)
            Game.surface.blit(text, rect)

            Game.events = pygame.event.get()
            Game.add_debug_info("PERFORMANCES INFORMATIONS")
            Game.add_debug_info("CPU load: " + str(psutil.cpu_percent()) + "%")
            Game.add_debug_info("Memory usage: " + str(psutil.virtual_memory().percent) + "%")
            Game.add_debug_info(str(math.floor(Game.clock.get_fps())) + " FPS")
            Game.add_debug_info("----------")

            for event in Game.events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

            Game.display_debug_info()
            Game.draw_cursor()
            Game.window.update()

        pb.bar.kill()
        pb.kill()
        cls.logger.info("Loaded " + str(len(cls.loaded_ressources) - before_load_nb) + " entries (" + str(len(cls.pending_ressources)) + " were requested)")
        cls.logger.info("Loading done")
        cls.loaded_ressources_entries = cls.pending_ressources.copy()
        cls.pending_ressources = {}

    @classmethod
    def unload(cls):
        bf = str(psutil.virtual_memory().percent)
        del cls.loaded_ressources
        gc.collect()
        cls.loaded_ressources = {}
        cls.logger.info("Unloaded all ressources")
        cls.logger.debug("Memory: " + bf + "% before, " + str(psutil.virtual_memory().percent) + "% after")

    @classmethod
    def select_entries(cls, path):
        if path[-1] == "*":
            path = path[:-1]
        entries = []
        for entry in cls.RESSOURCES:
            if entry[:len(path)] == path:
                entries.append(entry)
                entries.sort()
        return entries

    @classmethod
    def get_multiple(cls, entry):
        try:
            rlist = []
            entries = cls.select_entries(entry.lower())
            for entry in entries:
                rlist.append(cls.loaded_ressources[entry.lower()])
            return rlist
        except KeyError:
            cls.logger.critical(f"Ressource for entry {entry.lower()} can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry.lower())

    @classmethod
    def get(cls, entry):
        try:
            return cls.loaded_ressources[entry.lower()]
        except KeyError:
            cls.logger.critical(f"Ressource for entry {entry.lower()} can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry.lower())

    @classmethod
    def add_pending(cls, entry):
        try:
            rlist = []
            entries = cls.select_entries(entry.lower())
            if len(entries) == 0:
                cls.logger.warning("The requested selector (" + entry + ") did not find any entries, it may cause exceptions but ignoring")
            for entry in entries:
                cls.pending_ressources[entry] = cls.RESSOURCES[entry]
        except KeyError:
            cls.logger.critical("Ressource can't be added to pending ressources (path doesn't exist)")
            raise UnreachableRessourceError(entry)
