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
    def __init__(self):
        self.logger = Game.get_logger("Loader")

        self.logger.info("Initializing registries")

        self.logger.info("Building RESSOURCES registry")
        self.RESSOURCES = {}
        for entry in make_entries(RESSOURCES_DIRECTORY):
            self.RESSOURCES[entry[0]] = entry[1]
        self.logger.info("Registered " + str(len(self.RESSOURCES)) + " entries")

        self.logger.info("Building pending_ressources registry")
        self.pending_ressources = {}
        self.logger.info("Registered " + str(len(self.pending_ressources)) + " entries")

        self.logger.info("Building loaded_ressources registry")
        self.loaded_ressources = {}
        self.logger.info("Registered " + str(len(self.loaded_ressources)) + " entries")
        if len(self.loaded_ressources) > 0:
            self.logger.warning("Bad registration: no ressources must be loaded at startup")

        self.logger.info("Initialization done.")

    def load(self):
        self.logger.info("Starting loading ressources")
        for entry in self.pending_ressources:
            ext = self.pending_ressources[entry].split("/")[-1].split(".")
            try:
                if ext[-1] == "png":
                    self.loaded_ressources[entry] = pygame.image.load(self.pending_ressources[entry])
                    self.logger.debug("Entry " + entry + " loaded")

                if ext[-2] == "level" and ext[-1] == "json":
                    table = None
                    file = open(self.pending_ressources[entry], "r")
                    table = json.loads(file.read())
                    file.close()
                    self.loaded_ressources[entry] = table
                    self.logger.debug("Entry " + entry + " loaded")
                    self.logger.info("Loaded " + str(len(self.pending_ressources)) + " entries")
                    self.logger.info("Loading done")
                    self.pending_ressources = []

            except Exception as ex:
                self.logger.warning("Can't load entry " + entry)
                exc_type, exc_value, exc_tb = sys.exc_info()
                trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                for ms in trace.split("\n"):
                    self.logger.warning(ms)

    def select_entries(self, path):
        if "*" in path:
            if path[-1] == "*":
                path = path[:-1]
                entries = []
                for entry in self.RESSOURCES:
                    if entry[:len(path)] == path:
                        entries.append(entry)
                return entries
            else:
                raise InvalidRessourcePathError(path)
        else:
            return [path]

    def get_multiple(self, entry):
        try:
            rlist = []
            entries = self.select_entries(entry)
            for entry in entries:
                rlist.append(self.loaded_ressources[entry])
            return rlist
        except KeyError:
            self.logger.critical("Ressources can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry)

    def get(self, entry):
        try:
            return self.loaded_ressources[entry]
        except KeyError:
            self.logger.critical("Ressource can't be reached (Are ressources loaded ?)")
            raise UnreachableRessourceError(entry)

    def add_pending(self, entry):
        try:
            rlist = []
            entries = self.select_entries(entry)
            for entry in entries:
                self.pending_ressources[entry] = self.RESSOURCES[entry]
        except KeyError:
            self.logger.critical("Ressource can't be added to pending ressources (path doesn't exist)")
            raise UnreachableRessourceError(entry)
