import os
import sys
import traceback
import json
import pygame

from dpt.game import Game

RESSOURCES_DIRECTORY = Game.ROOT_DIRECTORY + "/dpt/ressources/"


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


class InvalidRessourcePathError(Exception):
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
                    rlist.append((item2[0], item2[1]))
                else:
                    rlist.append((os.path.basename(path) + "." + item2[0], item2[1]))
        elif os.path.isfile(path + "/" + item):
            if os.path.basename(path) == '':
                rlist.append((os.path.splitext(item)[0], path + "/" + item))
            else:
                rlist.append((os.path.basename(path) + "." + os.path.splitext(item)[0], path + "/" + item))
    return rlist


class RessourceLoader:
    RESSOURCES = {}
    pending_ressources = {}
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

        cls.logger.info("Initialization done.")

    @classmethod
    def load(cls):
        cls.logger.info("Starting loading ressources")
        for entry in cls.pending_ressources:
            ext = cls.pending_ressources[entry].split("/")[-1].split(".")
            try:
                if ext[-1] == "png":
                    cls.loaded_ressources[entry] = pygame.image.load(cls.pending_ressources[entry])
                    cls.logger.debug("Entry " + entry + " loaded")

                if ext[-2] == "level" and ext[-1] == "json":
                    table = None
                    file = open(cls.pending_ressources[entry], "r")
                    table = json.loads(file.read())
                    file.close()
                    cls.loaded_ressources[entry] = table
                    cls.logger.debug("Entry " + entry + " loaded")
            except Exception as ex:
                cls.logger.warning("Can't load entry " + entry)
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                for ms in trace.split("\n"):
                    cls.logger.warning(ms)
        cls.logger.info("Loaded " + str(len(cls.pending_ressources)) + " entries")
        cls.logger.info("Loading done")
        cls.pending_ressources = []

    @classmethod
    def select_entries(cls, path):
        if "*" in path:
            if path[-1] == "*":
                path = path[:-1]
                entries = []
                for entry in cls.RESSOURCES:
                    if entry[:len(path)] == path:
                        entries.append(entry)
                return entries
            else:
                raise InvalidRessourcePathError(path)
        else:
            return [path]

    @classmethod
    def get_multiple(cls, entry):
        try:
            rlist = []
            entries = cls.select_entries(entry)
            for entry in entries:
                rlist.append(cls.loaded_ressources[entry])
            return rlist
        except KeyError:
            cls.logger.critical("Ressources can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry)

    @classmethod
    def get(cls, entry):
        try:
            return cls.loaded_ressources[entry]
        except KeyError:
            cls.logger.critical("Ressource can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry)

    @classmethod
    def add_pending(cls, entry):
        try:
            rlist = []
            entries = cls.select_entries(entry)
            for entry in entries:
                cls.pending_ressources[entry] = cls.RESSOURCES[entry]
        except KeyError:
            cls.logger.critical("Ressource can't be added to pending ressources (path doesn't exist)")
            raise UnreachableRessourceError(entry)
