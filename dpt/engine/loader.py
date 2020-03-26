import os

import pygame

from dpt.game import Game

RESSOURCES_DIRECTORY = Game.ROOT_DIRECTORY + "/dpt/ressources/"


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


class RessourceLoader:
    def __init__(self):
        game = Game.get_instance()
        self.logger = game.get_logger("Loader")

        self.logger.info("Initializing registries")

        self.logger.info("Building RESSOURCES registry")
        self.RESSOURCES = make_entries(RESSOURCES_DIRECTORY)
        self.logger.info("Registered " + str(len(self.RESSOURCES)) + " entries")

        self.logger.info("Building pending_ressources registry")
        self.pending_ressources = {}
        for entry in make_entries(RESSOURCES_DIRECTORY):
            self.pending_ressources[entry[0]] = entry[1]
        self.logger.info("Registered " + str(len(self.pending_ressources)) + " entries")

        self.logger.info("Building loaded_ressources regisrty")
        self.loaded_ressources = {}
        self.logger.info("Registered " + str(len(self.loaded_ressources)) + " entries")
        if len(self.loaded_ressources) > 0:
            self.logger.warning("Bad registration: no ressources must be loaded at startup")

        self.logger.info("Initialization done.")

    def load(self):
        self.logger.info("Starting loading ressources")
        for entry in self.pending_ressources:
            if os.path.splitext(self.pending_ressources[entry])[1] == ".png":
                self.loaded_ressources[entry] = pygame.image.load(self.pending_ressources[entry])
                self.logger.debug("Entry " + entry + " loaded")
        self.logger.info("Loading done")

    def get(self, entry):
        try:
            return self.loaded_ressources[entry]
        except KeyError:
            self.logger.critical("Ressource can't be reached (Is ressources loaded ?)")
            raise UnreachableRessourceError(entry)
