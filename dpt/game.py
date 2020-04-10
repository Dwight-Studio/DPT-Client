import datetime
import logging
import os
import sys
import tarfile
import traceback
import pygame


class Game(object):
    # Constantes
    VERSION = "ALPHA-0.0.1"
    PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
    PYGAME_VERSION = pygame.version.ver
    PLATFORM = sys.platform
    ROOT_DIRECTORY = os.path.abspath("../")
    SERVER_ADDRESS = "localhost"
    VOTE_TIMEOUT = 80
    TILESIZE = 32
    LINUX_USER = True

    # Variable à définir
    isPlayerDead = False
    window = None
    clock = None
    player = None
    ressources = None
    enemyGroup = None
    environment = None
    ghostBlock = None
    editorPanel = None
    availableTiles = None
    surface = None
    playerSprite = None
    camera = None
    tile = None
    editor = None

    # Evenements
    BUTTONEVENT = None

    _debug_infos = None

    # Logs
    # Gère les fichiers de logs
    if os.path.isfile(ROOT_DIRECTORY + "/logs/latest.log"):
        file = tarfile.open(ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz", mode="x:gz", )
        file.add(ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
        file.close()
        os.remove(ROOT_DIRECTORY + "/logs/latest.log")

    # Initialisation des logs
    # Logs des autres modules
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    # Formatter
    logging_format = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")

    # File handler
    file_handler = logging.FileHandler(ROOT_DIRECTORY + "/logs/latest.log")
    file_handler.setFormatter(logging_format)

    # Stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging_format)

    @classmethod
    def play(cls, debug):
        cls.DEBUG = debug

        if cls.DEBUG:
            cls.file_handler.setLevel(logging.DEBUG)
            cls.stream_handler.setLevel(logging.DEBUG)
        else:
            cls.file_handler.setLevel(logging.INFO)
            cls.stream_handler.setLevel(logging.INFO)

        main_logger = cls.get_logger(None)
        main_logger.info("--- Starting Don't Play Together. ---")
        main_logger.debug("Version: " + cls.VERSION)
        main_logger.debug("Python version: " + cls.PYTHON_VERSION)
        main_logger.debug("Pygame version: " + cls.PYGAME_VERSION)
        main_logger.debug("OS: " + cls.PLATFORM)

        pygame.init()
        cls._debug_infos = []

        # Groupes Pygame
        cls.player = pygame.sprite.Group()
        cls.enemyGroup = pygame.sprite.Group()
        cls.environment = pygame.sprite.Group()
        cls.ghostBlock = pygame.sprite.Group()
        cls.editorPanel = pygame.sprite.Group()

        # Evenements persos
        cls.BUTTONEVENT = pygame.event.custom_type()

        cls.window = pygame.display
        if Game.LINUX_USER:
            cls.surface = cls.window.set_mode((0, 0), pygame.NOFRAME, pygame.RESIZABLE)
        else:
            cls.surface = cls.window.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)

        w, h = cls.surface.get_size()
        main_logger.debug("Window size: " + str(w) + "x" + str(h))
        pygame.display.set_caption("Don't play together")
        cls.clock = pygame.time.Clock()

        # Déclaration des évènements

        try:
            # /!\ ZONE SECURISÉE /!\
            from dpt.engine.loader import RessourceLoader
            cls.ressources = RessourceLoader()
            cls.ressources.add_pending("*")
            cls.ressources.load()
            from dpt.engine.graphics.tileManager import TileManager, Camera
            cls.tile = TileManager()
            cls.tile.loadLevel("dpt.levels.leveltest")
            cls.camera = Camera(cls.tile.maxWidthSize, cls.tile.maxHeightSize)
            from dpt.engine.graphics.gui.editor.tileEditor import TileEditor
            cls.editor = TileEditor()
            cls.editor.inEditor = True
            # from dpt.engine.webCommunications import Communication
            # com = Communication()
            # com.create()
            # time.sleep(10)
            # com.createVoteEvent(0, 0)
            # time.sleep(40)
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

    @classmethod
    def add_debug_info(cls, str):
        cls._debug_infos.append(str)

    @classmethod
    def display_debug_info(cls):
        if cls.DEBUG:
            font = pygame.font.SysFont("arial", 15)
            y = 0
            for text in cls._debug_infos:
                debug_text = font.render(text, True, (0, 0, 0))
                rect = debug_text.get_rect()
                rect.x = 0
                rect.y = y
                y += 15
                cls.surface.blit(debug_text, rect)
        cls._debug_infos = []
