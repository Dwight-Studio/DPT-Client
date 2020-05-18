import datetime
import logging
import math
import os
import sys
import tarfile
import traceback
import psutil
import pygame
import json


def void():
    pass


def get_root():
    cwd = os.path.abspath(os.getcwd())
    if os.path.exists(cwd + "/dpt"):
        return cwd + "/dpt"
    else:
        return cwd


class Game(object):
    """Classe principale du jeu"""
    # Constantes
    DEBUG = False
    VERSION = "ALPHA-0.3.0"
    PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(
        sys.version_info[2]) + "-" + str(sys.version_info[3])
    PYGAME_VERSION = pygame.version.ver
    PLATFORM = sys.platform
    ROOT_DIRECTORY = get_root()
    VOTE_TIMEOUT = 20
    DEFAULT_SERVER_ADDRESS = "join.dont-play-together.fr"
    TILESIZE = 90
    DISPLAY_RATIO = 1
    TIMER_LENGTH = 300
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    WINDOW_WIDTH = None
    WINDOW_HEIGHT = None
    LEVELS_ENTRIES = ["dpt.levels.*", "user.levels.*"]

    # Variable à définir
    temp = {}  # Variable temporaire pour stocker différentes données temporaires
    main_logger = None  # Logger principal
    run = True  # Varibale indiquant si la main loop doit continuer
    display_rect = None  # Rectange de l'écran (pour savoir si un objet est dans l'écran)
    freeze_game = False  # Indique si le jeu est sur pause
    window = None  # Variable contenant l'écran
    clock = None  # Variable contenant l'horloge
    player_group = None  # Groupe du joueur
    available_tiles = None  # Liste de tous les tiles disponible
    surface = None  # Surface principale
    player_sprite = None  # Variable contenant le sprite du joueur
    gui = {}  # Dict contenant le GUI
    events = []  # Liste des évènements (actualisés à chaque frame)
    loop = void  # Loop actuelle
    cursor_on_button = False  # Variable indiquant si le curseur est sur un bouton (changement de curseur)
    cursor1 = None  # Image 1 du curseur
    cursor2 = None  # Image 2 du curseur
    life = 1  # Variable indiquant la vie du joueur vis à vis de son affichage
    selected_level = 0  # Niveau selectionné
    levels_list = None  # Liste des niveaux
    stars = 0  # Nombre d'étoiles débloquées

    # Paramètres utilisateur
    settings = {
        "general_volume": 1,
        "music_volume": 1,
        "sound_volume": 1,
        "display_size": 0,
        "server_address": DEFAULT_SERVER_ADDRESS,
        "30_FPS": 1
    }

    # Sauvegarde utilisateur
    saves = {}

    display_list = [("Automatique", 0, 0),
                    ("720p (1280 x 720)", 1280, 720),
                    ("900p (1440 x 900)", 1440, 900),
                    ("900p (1600 x 900)", 1600, 900),
                    ("1080p (1920 x 1080)", 1920, 1080),
                    ("1440p (2560 x 1440)", 2560, 1440),
                    ("4K (3840 x 2160)", 3840, 2160),
                    ("8K (7680 x 4320)", 7680, 4320)]

    anim_count_lava = 0
    anim_count_water = 0
    anim_count_coins = 0

    # Evenements
    BUTTON_EVENT = pygame.event.custom_type()
    VOTE_FINISHED_EVENT = pygame.event.custom_type()
    VOTE_RESULT_AVAILABLE_EVENT = pygame.event.custom_type()
    KEEP_ALIVE_EVENT = pygame.event.custom_type()
    TIMER_EVENT = pygame.event.custom_type()
    TIMER_FINISHED_EVENT = pygame.event.custom_type()
    WAIT_BETWEEN_VOTE_EVENT = pygame.event.custom_type()
    WAIT_BETWEEN_RECONNECT_EVENT = pygame.event.custom_type()
    DISCONNECTED_EVENT = pygame.event.custom_type()
    PLAYER_DEATH_EVENT = pygame.event.custom_type()

    # Variable privée pour l'affichage des infos de debug
    _debug_infos = None

    # Logs
    # Gère les fichiers de logs
    try:
        if os.path.isfile(ROOT_DIRECTORY + "/logs/latest.log"):
            file = tarfile.open(
                ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz",
                mode="x:gz", )
            file.add(ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
            file.close()
            os.remove(ROOT_DIRECTORY + "/logs/latest.log")
    except PermissionError:
        exit()

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
        """Lance le jeu

        :param debug: Activation du déboggage
        :type debug: bool
        :param skip_intro: Ignorer l'introduction
        :type skip_intro: bool
        """
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
            cls.main_logger = main_logger
            main_logger.info("--- Starting Don't Play Together. ---")
            main_logger.debug("Version: " + cls.VERSION)
            main_logger.debug("Python version: " + cls.PYTHON_VERSION)
            main_logger.debug("Pygame version: " + cls.PYGAME_VERSION)
            main_logger.debug("OS: " + cls.PLATFORM)
            main_logger.debug("CWD: " + cls.ROOT_DIRECTORY)

            # Chargement des réglages
            cls.load_profile()

            pygame.init()
            cls.SCREEN_WIDTH = pygame.display.Info().current_w
            cls.SCREEN_HEIGHT = pygame.display.Info().current_h
            main_logger.debug("Screen size: " + str(cls.SCREEN_WIDTH) + "x" + str(cls.SCREEN_HEIGHT))

            cls._debug_infos = []

            # Chargement de l'affichage
            cls.update_display()
            w, h = cls.surface.get_size()
            main_logger.debug("Tile size: " + str(cls.TILESIZE))
            pygame.display.set_caption("Don't play together")
            cls.clock = pygame.time.Clock()

            pygame.mixer.init()

            # Groupes Pygame
            cls.player_group = pygame.sprite.Group()

            # Séquence d'intro
            pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])
            pygame.mouse.set_visible(False)
            cls.cursor1 = pygame.transform.smoothscale(
                pygame.image.load(
                    cls.ROOT_DIRECTORY + "/ressources/dpt/images/gui/Cursors/CRS_ARROW.png").convert_alpha(),
                (32, 39))
            cls.cursor2 = pygame.transform.smoothscale(
                pygame.image.load(
                    cls.ROOT_DIRECTORY + "/ressources/dpt/images/gui/Cursors/CRS_HAND.png").convert_alpha(),
                (32, 44))
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

                for alpha in range(0, 256, 8):
                    Game.events = pygame.event.get()
                    cls.clock.tick(30)
                    pygame.draw.rect(Game.surface, (0, 0, 0), rect)
                    pygame_logo.set_alpha(alpha)
                    cls.surface.blit(pygame_logo, rect)
                    cls.window.update()

                pygame.time.delay(1000)

                for alpha in range(0, 256, 8):
                    Game.events = pygame.event.get()
                    cls.clock.tick(30)
                    pygame.draw.rect(Game.surface, (0, 0, 0), pygame.Rect(0, 0, w, h))
                    pygame_logo.set_alpha(248 - alpha)
                    cls.surface.blit(pygame_logo, rect)
                    cls.window.update()

                pygame.time.delay(1000)

                pygame.mixer_music.load(cls.ROOT_DIRECTORY + "/ressources/dpt/sounds/musics/intro_sequence.music.ogg")
                pygame.mixer_music.play()

                rect = logo.get_rect()
                rect.width *= 0.8 * cls.DISPLAY_RATIO
                rect.height *= 0.8 * cls.DISPLAY_RATIO
                logo = pygame.transform.smoothscale(logo, (rect.width, rect.height))
                rect.centerx = w // 2
                rect.centery = h // 2

                for alpha in range(0, 256, 2):
                    Game.events = pygame.event.get()
                    log = logo.copy()
                    cls.clock.tick(30)
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
                rect2.x = rect.left + math.floor(500 * Game.DISPLAY_RATIO)
                rect2.y = rect.bottom - math.floor(80 * Game.DISPLAY_RATIO)

                for alpha in range(0, 256, 13):
                    Game.events = pygame.event.get()
                    cls.clock.tick(30)
                    pygame.draw.rect(Game.surface, (255, 255, 255), rect2)
                    rect2.centerx += (255 - alpha) // 50
                    game_by.set_alpha(alpha)
                    cls.surface.blit(game_by, rect2)
                    cls.window.update()

                pygame.time.delay(2000)

                for alpha in range(0, 256, 2):
                    Game.events = pygame.event.get()
                    cls.clock.tick(30)
                    pygame.draw.rect(Game.surface, (255, 255, 255), pygame.Rect(0, 0, w, h))
                    logo.set_alpha(255 - alpha)
                    game_by.set_alpha(255 - alpha)
                    cls.surface.blit(logo, rect)
                    cls.surface.blit(game_by, rect2)
                    cls.window.update()

                pygame.mixer_music.fadeout(1000)
                pygame.time.delay(1000)

            # Scene par défaut
            from dpt.engine.scenes import Scenes
            Scenes.main_menu()

            from dpt.engine.effectsManagement import EffectsManagement

            # MainLoop
            while cls.run:
                Game.events = pygame.event.get()
                Game.add_debug_info("PERFORMANCES INFORMATIONS")
                Game.add_debug_info("CPU load: " + str(psutil.cpu_percent()) + "%")
                Game.add_debug_info("Memory usage: " + str(psutil.virtual_memory().percent) + "%")
                Game.add_debug_info(str(math.floor(Game.clock.get_fps())) + " FPS")
                Game.add_debug_info("----------")
                Game.add_debug_info("MOUSE INFORMATIONS")
                Game.add_debug_info("Mouse X: " + str(pygame.mouse.get_pos()[0]))
                Game.add_debug_info("Mouse Y: " + str(pygame.mouse.get_pos()[1]))
                Game.add_debug_info("----------")

                cls.loop()

                if EffectsManagement.upsidedown:
                    sc = pygame.transform.flip(Game.surface, False, True)
                    Game.surface.blit(sc, (0, 0))

                Game.display_debug_info()
                Game.window.update()

                Game.clock.tick(60 // Game.settings["30_FPS"])

            cls.save_profile()
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
        """Retourne un logger

        :param name: Nom du module
        :type name str

        :return: Logger specifique au module
        """

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            logger.addHandler(cls.stream_handler)
            logger.addHandler(cls.file_handler)

        return logger

    @classmethod
    def add_debug_info(cls, str):
        """Ajoute une information de déboggage à afficher (pendant une frame)

        :param str: Message
        :type str: str
        """
        cls._debug_infos.append(str)

    @classmethod
    def display_debug_info(cls):
        """Affiche les informations de déboggage"""
        if cls.DEBUG:
            font = pygame.font.SysFont("arial", math.floor(15 * Game.DISPLAY_RATIO))
            y = 0
            for text in cls._debug_infos:
                debug_text = font.render(text, True, (255, 255, 255))
                rect = debug_text.get_rect()
                rect.x = 0
                rect.y = y
                y += math.floor(15 * Game.DISPLAY_RATIO)
                cls.surface.blit(debug_text, rect)
        cls._debug_infos = []

    @classmethod
    def draw_cursor(cls):
        """Affiche le curseur"""
        if not cls.cursor_on_button:
            image = cls.cursor1
        else:
            image = cls.cursor2
        rect = image.get_rect()
        rect.x = pygame.mouse.get_pos()[0]
        rect.y = pygame.mouse.get_pos()[1]
        cls.surface.blit(image, rect)
        Game.cursor_on_button = False

    @classmethod
    def load_profile(cls):
        """Charge les paramètres"""
        try:
            from dpt.engine.loader import RESSOURCES_DIRECTORY
            file = open(RESSOURCES_DIRECTORY + "user/profile.json", "r")
            profile = json.loads(file.read())
            Game.settings.update(profile["settings"])
            Game.saves.update(profile["saves"])
            file.close()
            cls.get_logger("ProfileManager").info("Profile loaded")

        except FileNotFoundError:
            cls.save_profile()
            cls.get_logger("ProfileManager").warning("Can't find profile file, creating one")

        except Exception:
            cls.get_logger("ProfileManager").critical("Can't load profile")
            exc_type, exc_value, exc_tb = sys.exc_info()
            trace = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            for ms in trace.split("\n"):
                cls.main_logger.warning(ms)

    @classmethod
    def save_profile(cls):
        """Sauvegarde les paramètres"""
        from dpt.engine.loader import RESSOURCES_DIRECTORY
        file = open(RESSOURCES_DIRECTORY + "user/profile.json", "w")
        file.write(json.dumps({"settings": Game.settings, "saves": Game.saves}))
        file.close()
        cls.get_logger("ProfileManager").info("Profile saved")

    @classmethod
    def update_display(cls):
        """Actualise l'affichage (paramètres)"""
        if cls.PLATFORM == "win32":
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        cls.window = pygame.display

        try:
            text, cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT = cls.display_list[Game.settings["display_size"]]
        except KeyError:
            cls.WINDOW_WIDTH = 0
            cls.WINDOW_HEIGHT = 0

        cls.surface = cls.window.set_mode((cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT), pygame.NOFRAME)

        if cls.WINDOW_WIDTH == 0:
            cls.WINDOW_WIDTH = cls.surface.get_size()[0]

        if cls.WINDOW_HEIGHT == 0:
            cls.WINDOW_HEIGHT = cls.surface.get_size()[1]

        w, h = cls.surface.get_size()
        cls.main_logger.debug("Window size: " + str(w) + "x" + str(h))
        cls.DISPLAY_RATIO = h / 1080
        cls.TILESIZE = math.floor(cls.DISPLAY_RATIO * 90)
