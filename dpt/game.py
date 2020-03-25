import datetime
import logging
import os
import sys
import tarfile
import traceback
import weakref

import pygame
import dpt.engine.mainLoop


class Game(object):
    _instance = None

    def __init__(self, debug):
        self.VERSION = "ALPHA-0.0.1"
        self.PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
        self.PYGAME_VERSION = pygame.version.ver
        self.PLATFORM = sys.platform
        self.ROOT_DIRECTORY = os.path.abspath("../")
        self.DEBUG = debug

        # Undefined for now
        self.window = None
        self.clock = None
        self.player = None

        if os.path.isfile(self.ROOT_DIRECTORY + "/logs/latest.log"):
            file = tarfile.open(self.ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz", mode="x:gz", )
            file.add(self.ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
            file.close()
            os.remove(self.ROOT_DIRECTORY + "/logs/latest.log")

    def play(self):
        main_logger = self.get_logger(None, self.DEBUG)
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
            dpt.engine.mainLoop.loop()
        except Exception as err:
            main_logger.critical("Unexpected error has occurred. Following informations has been gathered:")
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            for ms in trace.split("\n"):
                main_logger.critical(ms)

    def get_logger(self, name, debug):

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Formatter
        logging_format = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")

        # File handler
        if not os.path.isdir(self.ROOT_DIRECTORY + "/logs/"):
            os.mkdir(self.ROOT_DIRECTORY + "/logs/")

        file_handler = logging.FileHandler(self.ROOT_DIRECTORY + "/logs/latest.log")
        file_handler.setFormatter(logging_format)

        # Stream handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging_format)

        if debug:
            file_handler.setLevel(logging.DEBUG)
            stream_handler.setLevel(logging.DEBUG)
        else:
            file_handler.setLevel(logging.INFO)
            stream_handler.setLevel(logging.INFO)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        logger.debug("Logger initied.")
        return logger

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def set_instance(cls, instance):
        cls._instance = instance
