import datetime
import logging
import os
import sys
import tarfile
import traceback
import pygame


class Game(object):
    _instance = None
    VERSION = "ALPHA-0.0.1"
    PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
    PYGAME_VERSION = pygame.version.ver
    PLATFORM = sys.platform
    ROOT_DIRECTORY = os.path.abspath("../")

    def __init__(self, debug):
        self.DEBUG = debug

        # Gère les fichiers de logs
        if os.path.isfile(self.ROOT_DIRECTORY + "/logs/latest.log"):
            file = tarfile.open(self.ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz", mode="x:gz", )
            file.add(self.ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
            file.close()
            os.remove(self.ROOT_DIRECTORY + "/logs/latest.log")

        # Initialisation des logs
        # Formatter
        logging_format = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")

        # File handler
        if not os.path.isdir(self.ROOT_DIRECTORY + "/logs/"):
            os.mkdir(self.ROOT_DIRECTORY + "/logs/")

        self.file_handler = logging.FileHandler(self.ROOT_DIRECTORY + "/logs/latest.log")
        self.file_handler.setFormatter(logging_format)

        # Stream handler
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(logging_format)

        if self.DEBUG:
            self.file_handler.setLevel(logging.DEBUG)
            self.stream_handler.setLevel(logging.DEBUG)
        else:
            self.file_handler.setLevel(logging.INFO)
            self.stream_handler.setLevel(logging.INFO)

        # Undefined for now
        self.window = None
        self.clock = None
        self.player = None
        self.ressources = None

    def play(self):
        main_logger = self.get_logger(None)
        main_logger.info("--- Starting Don't Play Together. ---")
        main_logger.debug("Version: " + self.VERSION)
        main_logger.debug("Python version: " + self.PYTHON_VERSION)
        main_logger.debug("Pygame version: " + self.PYGAME_VERSION)
        main_logger.debug("OS: " + self.PLATFORM)

        pygame.init()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        w, h = self.window.get_size()
        main_logger.debug("Window size: " + str(w) + "x" + str(h))
        pygame.display.set_caption("Don't play together")
        self.clock = pygame.time.Clock()

        try:
            from dpt.engine.loader import RessourceLoader
            self.ressources = RessourceLoader()
            self.ressources.load()

            from dpt.engine.mainLoop import loop
            loop()
        except Exception:
            main_logger.critical("Unexpected error has occurred. Following informations has been gathered:")
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            for ms in trace.split("\n"):
                main_logger.critical(ms)

    def get_logger(self, name):

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            logger.addHandler(self.stream_handler)
            logger.addHandler(self.file_handler)

        return logger

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def set_instance(cls, instance):
        cls._instance = instance
