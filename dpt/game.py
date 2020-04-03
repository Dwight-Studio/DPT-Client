import datetime
import logging
import os
import sys
import tarfile
import traceback
import pygame
import time


class Game(object):
    VERSION = "ALPHA-0.0.1"
    PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
    PYGAME_VERSION = pygame.version.ver
    PLATFORM = sys.platform
    ROOT_DIRECTORY = os.path.abspath("../")
    SERVER_ADDRESS = "localhost"
    VOTE_TIMEOUT = 80

    @classmethod
    def play(cls, debug):
        cls.DEBUG = debug

        # Gère les fichiers de logs
        if os.path.isfile(cls.ROOT_DIRECTORY + "/logs/latest.log"):
            file = tarfile.open(cls.ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz", mode="x:gz", )
            file.add(cls.ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
            file.close()
            os.remove(cls.ROOT_DIRECTORY + "/logs/latest.log")

        # Initialisation des logs
        # Logs des autres modules
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)

        # Formatter
        logging_format = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")

        # File handler
        if not os.path.isdir(cls.ROOT_DIRECTORY + "/logs/"):
            os.mkdir(cls.ROOT_DIRECTORY + "/logs/")

        cls.file_handler = logging.FileHandler(cls.ROOT_DIRECTORY + "/logs/latest.log")
        cls.file_handler.setFormatter(logging_format)

        # Stream handler
        cls.stream_handler = logging.StreamHandler(sys.stdout)
        cls.stream_handler.setFormatter(logging_format)

        if cls.DEBUG:
            cls.file_handler.setLevel(logging.DEBUG)
            cls.stream_handler.setLevel(logging.DEBUG)
        else:
            cls.file_handler.setLevel(logging.INFO)
            cls.stream_handler.setLevel(logging.INFO)

        # Variable à définir
        cls.window = None
        cls.clock = None
        cls.player = None
        cls.ressources = None

        main_logger = cls.get_logger(None)
        main_logger.info("--- Starting Don't Play Together. ---")
        main_logger.debug("Version: " + cls.VERSION)
        main_logger.debug("Python version: " + cls.PYTHON_VERSION)
        main_logger.debug("Pygame version: " + cls.PYGAME_VERSION)
        main_logger.debug("OS: " + cls.PLATFORM)

        pygame.init()
        cls.joueur = pygame.sprite.Group()
        cls.platforms = pygame.sprite.Group()
        cls.window = pygame.display
        cls.surface = cls.window.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        w, h = cls.surface.get_size()
        main_logger.debug("Window size: " + str(w) + "x" + str(h))
        pygame.display.set_caption("Don't play together")
        cls.clock = pygame.time.Clock()

        try:
            # /!\ ZONE SECURISÉE /!\
            from dpt.engine.loader import RessourceLoader
            cls.ressources = RessourceLoader()
            cls.ressources.add_pending("*")
            cls.ressources.load()
            from dpt.engine.graphics.tileManager import TileManager
            from dpt.engine.graphics.tileManager import levelTest
            tile = TileManager()
            tile.enableGrid()
            tile.loadLevel(levelTest)
            # from dpt.engine.webCommunications import Communication
            # com = Communication()
            # com.create()
            # time.sleep(10)
            # com.createVoteEvent(0, 0)
            #time.sleep(40)
            # com.voteResult()

            from dpt.engine.mainLoop import loop
            loop()
        except Exception:
            main_logger.critical("Unexpected error has occurred. Following informations has been gathered:")
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            for ms in trace.split("\n"):
                main_logger.critical(ms)

    @classmethod
    def get_logger(cls, name):

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            logger.addHandler(cls.stream_handler)
            logger.addHandler(cls.file_handler)

        return logger
