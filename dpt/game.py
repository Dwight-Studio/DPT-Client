import datetime
import logging
import math
import os
import sys
import tarfile
import traceback

import psutil
import pygame


def void():
    pass


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
    DISPLAY_RECT = False

    # Variable à définir
    run = True
    display_rect = None
    freeze_game = False
    window = None
    clock = None
    player_group = None
    ressources = None
    available_tiles = None
    selected_item = "dpt.blocks.grass.Grass"
    editor_tile_registry = {}
    surface = None
    player_sprite = None
    gui = {}
    events = []
    loop = void
    com = None
    cursor_on_button = False
    cursor1 = None
    cursor2 = None

    anim_count_lava = 0
    anim_count_water = 0
    anim_count_coins = 0

    # Evenements
    BUTTON_EVENT = None

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
    def play(cls, debug, skip_intro):
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
            cls.surface = cls.window.set_mode((0, 0), pygame.NOFRAME, pygame.SCALED)

            w, h = cls.surface.get_size()
            main_logger.debug("Window size: " + str(w) + "x" + str(h))
            cls.DISPLAY_RATIO = h / 1080
            cls.TILESIZE = math.floor(cls.DISPLAY_RATIO * cls.TILESIZE)
            main_logger.debug("Tile size: " + str(cls.TILESIZE))
            pygame.display.set_caption("Don't play together")
            cls.clock = pygame.time.Clock()

            pygame.mixer.init()

            # Groupes Pygame
            cls.player_group = pygame.sprite.Group()

            # Evenements persos
            cls.BUTTON_EVENT = pygame.event.custom_type()

            # Initialisation du RessourceLoader
            from dpt.engine.loader import RessourceLoader
            RessourceLoader.init()

            # Séquence d'intro
            pygame.mouse.set_visible(False)
            cls.cursor1 = pygame.transform.smoothscale(pygame.image.load(cls.ROOT_DIRECTORY +
                                                                         "/ressources/dpt/images/gui/Cursors/CRS_ARROW.png").convert_alpha(),
                                                       (32,
                                                        39))
            cls.cursor2 = pygame.transform.smoothscale(pygame.image.load(cls.ROOT_DIRECTORY +
                                                                         "/ressources/dpt/images/gui/Cursors/CRS_HAND.png").convert_alpha(),
                                                       (32,
                                                        44))
            if not skip_intro:
                pygame_logo = pygame.image.load(
                    cls.ROOT_DIRECTORY + "/ressources/dpt/images/pygame_logo.png").convert_alpha()
                logo = pygame.image.load(cls.ROOT_DIRECTORY + "/ressources/dpt/images/logo_dw.png").convert_alpha()
                game_by = pygame.image.load(cls.ROOT_DIRECTORY + "/ressources/dpt/images/game_by.png").convert_alpha()

                rect = pygame_logo.get_rect()
                rect.width *= cls.DISPLAY_RATIO
                rect.height *= cls.DISPLAY_RATIO
                pygame_logo = pygame.transform.smoothscale(pygame_logo, (rect.width, rect.height))
                rect.centerx = w // 2
                rect.centery = h // 2

                for alpha in range(0, 256, 4):
                    cls.clock.tick(60)
                    pygame.draw.rect(Game.surface, (0, 0, 0), rect)
                    pygame_logo.set_alpha(alpha)
                    cls.surface.blit(pygame_logo, rect)
                    cls.window.update()

                pygame.time.delay(1000)

                for alpha in range(0, 256, 4):
                    cls.clock.tick(60)
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
                logo = pygame.transform.smoothscale(logo, (rect.width, rect.height))
                rect.centerx = w // 2
                rect.centery = h // 2

                for alpha in range(0, 256, 1):
                    log = logo.copy()
                    cls.clock.tick(60)
                    pygame.draw.rect(Game.surface, (alpha, alpha, alpha), pygame.Rect(0, 0, w, h))
                    log.set_alpha(alpha)
                    color = min((255 - alpha) * 2, 255)
                    log.fill((color, color, color), special_flags=pygame.BLEND_RGB_ADD)
                    cls.surface.blit(log, rect)
                    cls.window.update()

                rect2 = game_by.get_rect()
                rect2.width *= 0.3 * cls.DISPLAY_RATIO
                rect2.height *= 0.3 * cls.DISPLAY_RATIO
                game_by = pygame.transform.smoothscale(game_by, (rect2.width, rect2.height))
                rect2.centerx = w // 2 - rect.width // 2 - math.floor(200 * cls.DISPLAY_RATIO)
                rect2.centery = rect.centery

                for alpha in range(0, 256, 10):
                    cls.clock.tick(60)
                    rect2.centerx += (255 - alpha) // 50
                    pygame.draw.rect(Game.surface, (255, 255, 255), rect2)
                    game_by.set_alpha(alpha)
                    cls.surface.blit(game_by, rect2)
                    cls.window.update()

                pygame.time.delay(2000)

                for alpha in range(0, 256, 1):
                    cls.clock.tick(60)
                    pygame.draw.rect(Game.surface, (255, 255, 255), pygame.Rect(0, 0, w, h))
                    logo.set_alpha(255 - alpha)
                    game_by.set_alpha(255 - alpha)
                    cls.surface.blit(logo, rect)
                    cls.surface.blit(game_by, rect2)
                    cls.window.update()

                pygame.mixer_music.fadeout(1000)
                pygame.time.delay(1000)

            # Tests webcoms
            #  from dpt.engine.webCommunications import Communication
            #  cls.com = Communication()
            # cls.com.create()
            # cls.com.create_vote_event(0, 0)

            # Scene par défaut
            from dpt.engine.scenes import Scenes
            # Scenes.main_menu()
            # Scenes.editor("dpt.levels.levelTest")
            Scenes.main_menu()

            # MainLoop
            while cls.run:
                Game.events = pygame.event.get()
                Game.add_debug_info("PERFORMANCES INFORMATIONS")
                Game.add_debug_info("CPU load: " + str(psutil.cpu_percent()) + "%")
                Game.add_debug_info("Memory usage: " + str(psutil.virtual_memory().percent) + "%")
                Game.add_debug_info(str(math.floor(Game.clock.get_fps())) + " FPS")
                Game.add_debug_info("----------")
                cls.loop()
                Game.draw_cursor()
                Game.clock.tick(60)
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
            font = pygame.font.SysFont("arial", math.floor(15 * Game.DISPLAY_RATIO))
            y = 0
            for text in cls._debug_infos:
                debug_text = font.render(text, True, (0, 0, 0))
                rect = debug_text.get_rect()
                rect.x = 0
                rect.y = y
                y += math.floor(15 * Game.DISPLAY_RATIO)
                cls.surface.blit(debug_text, rect)
        cls._debug_infos = []

    @classmethod
    def draw_cursor(cls):
        if not cls.cursor_on_button:
            image = cls.cursor1
        else:
            image = cls.cursor2
        rect = image.get_rect()
        rect.x = pygame.mouse.get_pos()[0]
        rect.y = pygame.mouse.get_pos()[1]
        cls.surface.blit(image, rect)
        Game.cursor_on_button = False
