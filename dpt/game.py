import datetime
import logging
import math
import os
import sys
import tarfile
import traceback
import pygame
import time


def get_root():
    cwd = os.path.abspath(os.getcwd())
    if os.path.exists(cwd + "/dpt"):
        return cwd + "/dpt"
    else:
        return cwd


class Game(object):
    # Constantes
    DEBUG = False
    VERSION = "ALPHA-0.1.0"
    PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
    PYGAME_VERSION = pygame.version.ver
    PLATFORM = sys.platform
    ROOT_DIRECTORY = get_root()
    SERVER_ADDRESS = "localhost"
    VOTE_TIMEOUT = 80
    TILESIZE = 90
    DISPLAY_RATIO = 1
    LINUX_USER = True
    DISPLAY_RECT = False

    # Variable à définir
    run = True
    display_rect = None
    isPlayerDead = False
    window = None
    clock = None
    playerGroup = None
    ressources = None
    availableTiles = None
    platformsList = []
    enemyList = []
    selectedItem = "dpt.blocks.grass.Grass"
    editorTileRegistry = {}
    surface = None
    playerSprite = None
    button = None
    events = []

    animCountLava = 0
    animCountWater = 0
    animCountCoins = 0

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
    if not os.path.exists(ROOT_DIRECTORY + "/logs"):
        os.mkdir(ROOT_DIRECTORY + "/logs")
    file_handler = logging.FileHandler(ROOT_DIRECTORY + "/logs/latest.log")
    file_handler.setFormatter(logging_format)

    # Stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging_format)

    @classmethod
    def play(cls, debug):
        try:
            # /!\ ZONE SECURISÉE /!\
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
            main_logger.debug("CWD: " + cls.ROOT_DIRECTORY)

            pygame.init()
            cls._debug_infos = []

            cls.window = pygame.display
            if Game.LINUX_USER:
                cls.surface = cls.window.set_mode((0, 0), pygame.NOFRAME, pygame.SCALED)
            else:
                cls.surface = cls.window.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)

            w, h = cls.surface.get_size()
            main_logger.debug("Window size: " + str(w) + "x" + str(h))
            cls.DISPLAY_RATIO = h / 1080
            cls.TILESIZE = math.floor(cls.DISPLAY_RATIO * cls.TILESIZE)
            main_logger.debug("Tile size: " + str(cls.TILESIZE))
            pygame.display.set_caption("Don't play together")
            cls.clock = pygame.time.Clock()

            pygame.mixer.init()

            # Groupes Pygame
            cls.playerGroup = pygame.sprite.Group()

            # Evenements persos
            cls.BUTTONEVENT = pygame.event.custom_type()

            # Initialisation du RessourceLoader
            from dpt.engine.loader import RessourceLoader
            RessourceLoader.init()

            # Séquence d'intro
            pygame_logo = pygame.image.load(cls.ROOT_DIRECTORY + "/ressources/dpt/images/pygame_logo.png").convert_alpha()
            logo = pygame.image.load(cls.ROOT_DIRECTORY + "/ressources/dpt/images/logo_dw.png").convert_alpha()
            game_by = pygame.image.load(cls.ROOT_DIRECTORY + "/ressources/dpt/images/game_by.png").convert_alpha()

            rect = pygame_logo.get_rect()
            rect.width *= cls.DISPLAY_RATIO
            rect.height *= cls.DISPLAY_RATIO
            pygame_logo = pygame.transform.scale(pygame_logo, (rect.width, rect.height))
            rect.centerx = w // 2
            rect.centery = h // 2

            for alpha in range(0, 256, 4):
                pygame.time.delay(1)
                pygame.draw.rect(Game.surface, (0, 0, 0), rect)
                pygame_logo.set_alpha(alpha)
                cls.surface.blit(pygame_logo, rect)
                cls.window.update()

            pygame.time.delay(1000)

            for alpha in range(0, 256, 4):
                pygame.time.delay(1)
                pygame.draw.rect(Game.surface, (0, 0, 0), pygame.Rect(0, 0, w, h))
                pygame_logo.set_alpha(255 - alpha)
                cls.surface.blit(pygame_logo, rect)
                cls.window.update()

            pygame.time.delay(1000)

            pygame.mixer_music.set_volume(0.5)
            pygame.mixer_music.load(cls.ROOT_DIRECTORY + "/ressources/dpt/sounds/musics/intro_sequence.music.ogg")
            pygame.mixer_music.play()

            rect = logo.get_rect()
            rect.width *= 0.8 * cls.DISPLAY_RATIO
            rect.height *= 0.8 * cls.DISPLAY_RATIO
            logo = pygame.transform.scale(logo, (rect.width, rect.height))
            rect.centerx = w // 2
            rect.centery = h // 2

            for alpha in range(0, 256, 2):
                log = logo.copy()
                pygame.time.delay(5)
                pygame.draw.rect(Game.surface, (alpha, alpha, alpha), pygame.Rect(0, 0, w, h))
                log.set_alpha(alpha)
                color = min((255 - alpha) * 2, 255)
                log.fill((color, color, color), special_flags=pygame.BLEND_RGB_ADD)
                cls.surface.blit(log, rect)
                cls.window.update()

            rect2 = game_by.get_rect()
            rect2.width *= 0.3 * cls.DISPLAY_RATIO
            rect2.height *= 0.3 * cls.DISPLAY_RATIO
            game_by = pygame.transform.scale(game_by, (rect2.width, rect2.height))
            rect2.centerx = w // 2 - rect.width // 2 - math.floor(100 * cls.DISPLAY_RATIO)
            rect2.centery = rect.centery

            for alpha in range(0, 256, 10):
                pygame.time.delay(20)
                pygame.draw.rect(Game.surface, (255, 255, 255), rect2)
                game_by.set_alpha(alpha)
                cls.surface.blit(game_by, rect2)
                cls.window.update()

            pygame.time.delay(2000)

            for alpha in range(0, 256, 2):
                pygame.time.delay(3)
                pygame.draw.rect(Game.surface, (255, 255, 255), pygame.Rect(0, 0, w, h))
                logo.set_alpha(255 - alpha)
                game_by.set_alpha(255 - alpha)
                cls.surface.blit(logo, rect)
                cls.surface.blit(game_by, rect2)
                cls.window.update()

            pygame.mixer_music.fadeout(1000)
            pygame.time.delay(1000)

            # Initialisation du TileManager
            from dpt.engine.tileManager import TileManager
            from dpt.engine.gui.editor.tileEditor import TileEditor
            TileEditor.inEditor = False
            RessourceLoader.add_pending("dpt.images.gui.buttons.BTN_GREEN_RECT_*")
            RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
            TileManager.loadLevel("dpt.levels.leveltest")

            # Initialisation des webComs
            from dpt.engine.webCommunications import Communication
            # com = Communication()
            # com.create()
            # time.sleep(10)
            # com.createVoteEvent(0, 0)
            # time.sleep(40)
            # com.voteResult()

            # Ajout du bouton d'éditeur
            from dpt.engine.gui.menu.button import Button
            cls.button = Button(0, Game.surface.get_size()[1] - 50, 127, 46, RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"), pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Editeur")

            # Loops
            from dpt.engine.mainLoop import level_loop
            cls.loop = level_loop

            while cls.run:
                cls.loop()
            pygame.quit()

        except Exception:
            main_logger = cls.get_logger(None)
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
