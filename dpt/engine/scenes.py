import math
import pygame
import time

from threading import Thread
from dpt.engine.loader import UnreachableRessourceError
from dpt.game import Game


class Scenes:
    """Gestionnaire des scènes"""
    logger = Game.get_logger(__name__)

    @classmethod
    def editor(cls, level):
        """Met en place les élèments d'éditeur

        :param level: Niveau à charger

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying EDITOR")
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Nettoyage
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.progressbar import ProgressBar
        from dpt.engine.gui.menu.checkbox import Checkbox
        Button.buttonsGroup.empty()
        Button.text_sprite_buttonsGroup.empty()
        ProgressBar.progress_bar_group.empty()
        ProgressBar.bar_group.empty()
        Checkbox.checkbox_group.empty()

        # Gestion des ressources
        RessourceLoader.add_pending("dpt.images.gui.buttons.BTN_GREEN_RECT_*")
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_out")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_in")

        # Initialisation du TileManager
        TileEditor.is_editing = TileEditor.enabled_editor = True
        if not TileManager.load_level(level):
            Scenes.return_error("Impossible de charger le niveau.", "Détails :", "Aucune information supplémentaire")

        # Ajout du bouton d'éditeur
        from dpt.engine.gui.menu import Text
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite

        win = Window(0, Game.WINDOW_HEIGHT - math.floor(64 * 5 * Game.DISPLAY_RATIO), 2, 5)
        Game.gui = {"window": win,
                    "title": Text(0,
                                  win.rect.y + math.floor(5 * Game.DISPLAY_RATIO),
                                  "Éditeur",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=win.rect.centerx),
                    "r1": Text(math.floor(15 * Game.DISPLAY_RATIO),
                               win.rect.y + math.floor(80 * Game.DISPLAY_RATIO),
                               "Ctrl + S → Sauvegarder",
                               math.floor(25 * Game.DISPLAY_RATIO),
                               (0, 0, 0),
                               "dpt.fonts.DINOT_CondBlack"),
                    "r2": Text(math.floor(15 * Game.DISPLAY_RATIO),
                               win.rect.y + math.floor(105 * Game.DISPLAY_RATIO),
                               "Ctrl + O → Ouvrir",
                               math.floor(25 * Game.DISPLAY_RATIO),
                               (0, 0, 0),
                               "dpt.fonts.DINOT_CondBlack"),
                    "r3": Text(math.floor(15 * Game.DISPLAY_RATIO),
                               win.rect.y + math.floor(130 * Game.DISPLAY_RATIO),
                               "Ctrl + N → Nouveau",
                               math.floor(25 * Game.DISPLAY_RATIO),
                               (0, 0, 0),
                               "dpt.fonts.DINOT_CondBlack"),
                    "r4": Text(math.floor(15 * Game.DISPLAY_RATIO),
                               win.rect.y + math.floor(155 * Game.DISPLAY_RATIO),
                               "Ctrl + T → Menu",
                               math.floor(25 * Game.DISPLAY_RATIO),
                               (0, 0, 0),
                               "dpt.fonts.DINOT_CondBlack"),
                    "r5": Text(math.floor(15 * Game.DISPLAY_RATIO),
                               win.rect.y + math.floor(180 * Game.DISPLAY_RATIO),
                               "Ctrl + I → Propriétés",
                               math.floor(25 * Game.DISPLAY_RATIO),
                               (0, 0, 0),
                               "dpt.fonts.DINOT_CondBlack"),
                    "editor_button": Button(math.floor(40 * Game.DISPLAY_RATIO),
                                            Game.WINDOW_HEIGHT - math.floor(80 * Game.DISPLAY_RATIO),
                                            math.floor(170 * Game.DISPLAY_RATIO),
                                            math.floor(61 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_RECT_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_BLUE_RECT_IN"),
                                            text_sprite=SimpleSprite(math.floor(143 * Game.DISPLAY_RATIO),
                                                                     math.floor(35 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.TEXT_START")))}

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def level(cls, level):
        """Met en place les élèments de niveau

        :param level: Niveau à charger

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying LEVEL")
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        from dpt.engine.effectsManagement import EffectsManagement

        # Initialisation du TileManager
        TileEditor.is_editing = TileEditor.enabled_editor = False
        if not TileManager.load_level(level):
            return False

        # Initialisation de la gestion des effets
        EffectsManagement.create_effects_image()
        EffectsManagement.reset()
        EffectsManagement.vote()

        from dpt.engine.gui.menu import Text
        Game.gui = {"wb_player_count": Text(0, 0,
                                            "Connexion au serveur...",
                                            math.floor(25 * Game.DISPLAY_RATIO),
                                            (0, 0, 0),
                                            "dpt.fonts.DINOT_CondBlack"),
                    "wb_session": Text(0, math.floor(25 * Game.DISPLAY_RATIO),
                                       "Connexion au serveur...",
                                       math.floor(25 * Game.DISPLAY_RATIO),
                                       (0, 0, 0),
                                       "dpt.fonts.DINOT_CondBlack")}

        Game.gui["wb_player_count"].rect.right = Game.WINDOW_WIDTH - math.floor(10 * Game.DISPLAY_RATIO)
        Game.gui["wb_session"].rect.right = Game.WINDOW_WIDTH - math.floor(10 * Game.DISPLAY_RATIO)

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def pause(cls):
        """Met en place les élèments du menu pause

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.gui.editor.tileEditor import TileEditor
        cls.logger.info("Displaying PAUSE")

        # Musiques et sons
        def music():
            for i in range(0, 101):
                pygame.time.wait(2)
                pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * ((100 - i) / 100))
            pygame.mixer.pause()
            pygame.mixer.music.pause()

        Thread(target=music).start()

        from dpt.engine.effectsManagement import EffectsManagement

        EffectsManagement.upsidedown = False

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
        buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)
        buttons_x = (Game.WINDOW_WIDTH // 2) - (button_width // 2)

        Game.gui.update({"p_window": Window(0, 0, 3, 9, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                         "p_title": Text(0,
                                         buttons_starting_y - math.floor(90 * Game.DISPLAY_RATIO),
                                         "Pause",
                                         math.floor(50 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack",
                                         centerx=Game.WINDOW_WIDTH // 2),
                         "p_button_resume": Button(buttons_x, buttons_starting_y, button_width, button_height,
                                                   RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                                   pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                                   text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                            math.floor(50 * Game.DISPLAY_RATIO),
                                                                            RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                         "p_button_main_menu": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 2, button_width, button_height,
                                                      RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                                      pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                                      text_sprite=SimpleSprite(math.floor(50 * Game.DISPLAY_RATIO),
                                                                               math.floor(38 * Game.DISPLAY_RATIO),
                                                                               RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                         "p_button_quit": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 3,
                                                 button_width,
                                                 button_height,
                                                 RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                                 pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                                 text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                          math.floor(50 * Game.DISPLAY_RATIO),
                                                                          RessourceLoader.get("dpt.images.gui.symbols.SYMB_X")))})

        if not TileEditor.enabled_editor:
            Game.gui["p_button_restart_save"] = Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height), button_width, button_height,
                                                       RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                                       pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                                       text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                                math.floor(40 * Game.DISPLAY_RATIO),
                                                                                RessourceLoader.get("dpt.images.gui.symbols.SYMB_REPLAY")))
        else:
            Game.gui["p_button_restart_save"] = Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height), button_width, button_height,
                                                       RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                                       pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                                       text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                                math.floor(47 * Game.DISPLAY_RATIO),
                                                                                RessourceLoader.get("dpt.images.gui.symbols.SYMB_STOP")))

        from dpt.engine.mainLoop import pause_loop
        Game.loop = pause_loop
        return True

    @classmethod
    def main_menu(cls, load=True):
        """Met en place les élèments du menu principale

        :param load: (Re)Charge les ressources
        :type load: bool

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        cls.logger.info("Displaying MAIN_MENU")
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.effectsManagement import EffectsManagement

        EffectsManagement.upsidedown = False

        # Gestion des ressources
        if load:
            RessourceLoader.init()
            Game.levels_list = None
            Game.temp = {}
            RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
            RessourceLoader.add_pending("dpt.images.gui.*")
            RessourceLoader.add_pending("dpt.images.dpt")
            RessourceLoader.add_pending("dpt.fonts.*")
            RessourceLoader.add_pending("dpt.sounds.musics.story_time")
            RessourceLoader.add_pending("dpt.sounds.sfx.switch6")
            RessourceLoader.add_pending("dpt.images.not_found")
            RessourceLoader.load()

        # Gestion de la musique
        if load:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"])
            pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
            pygame.mixer_music.play(-1)

        # Webcoms
        from dpt.engine.webCommunications import WebCommunication
        WebCommunication.close()

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)
        buttons_gap_x = math.floor(80 * Game.DISPLAY_RATIO)
        buttons_starting_x = math.floor((Game.WINDOW_WIDTH / 2) - button_width * 2 - buttons_gap_x * 1.5)
        buttons_y = (Game.WINDOW_HEIGHT // 4) * 3 + 50 * Game.DISPLAY_RATIO
        Game.gui = {"button_play": Button(buttons_starting_x, buttons_y, button_width, button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                          text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                   math.floor(50 * Game.DISPLAY_RATIO),
                                                                   RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_editor": Button(buttons_starting_x + (button_width + buttons_gap_x), buttons_y,
                                            button_width,
                                            button_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                            text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                     math.floor(50 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLUS"))),
                    "button_settings": Button(buttons_starting_x + (button_width + buttons_gap_x) * 2, buttons_y,
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_SETTINGS"))),
                    "button_quit": Button(buttons_starting_x + (button_width + buttons_gap_x) * 3, buttons_y,
                                          button_width,
                                          button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                   math.floor(50 * Game.DISPLAY_RATIO),
                                                                   RessourceLoader.get("dpt.images.gui.symbols.SYMB_X"))),
                    "window": Window((Game.WINDOW_WIDTH // 2) - math.floor(122 * 3 * Game.DISPLAY_RATIO),
                                     buttons_y + button_height // 2 - math.floor(64 * 1.5 * Game.DISPLAY_RATIO), 6, 3)}

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True

    @classmethod
    def settings_menu(cls):
        """Met en place les élèments du menu des paramètres

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """

        cls.logger.info("Displaying SETTINGS_MENU")
        from dpt.engine.loader import RessourceLoader

        # Ajout du GUI
        from dpt.engine.gui.menu.slider import Slider
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.gui.menu.radioButton import RadioButton
        from dpt.engine.gui.menu.checkbox import Checkbox

        btn_list = []

        Game.gui = {"window_sound": Window(410 * Game.DISPLAY_RATIO, 190 * Game.DISPLAY_RATIO, 9, 5),
                    "sound_title": Text(math.floor(810 * Game.DISPLAY_RATIO),
                                        math.floor(200 * Game.DISPLAY_RATIO),
                                        "Options sonores",
                                        math.floor(50 * Game.DISPLAY_RATIO),
                                        (0, 0, 0),
                                        "dpt.fonts.DINOT_CondBlack"),
                    "general_volume_slider": Slider(math.floor(480 * Game.DISPLAY_RATIO),
                                                    math.floor(330 * Game.DISPLAY_RATIO),
                                                    math.floor(960 * Game.DISPLAY_RATIO),
                                                    math.floor(50 * Game.DISPLAY_RATIO),
                                                    Game.settings["general_volume"],
                                                    image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                                    image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7"),
                                                    image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                                    image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13"),
                                                    image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_2"),
                                                    image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_8"),
                                                    image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                    image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_FULLBAR")),
                    "general_volume_title": Text(math.floor(890 * Game.DISPLAY_RATIO),
                                                 math.floor(295 * Game.DISPLAY_RATIO),
                                                 "Volume général",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "music_volume_slider": Slider(math.floor(480 * Game.DISPLAY_RATIO),
                                                  math.floor(380 * Game.DISPLAY_RATIO),
                                                  math.floor(470 * Game.DISPLAY_RATIO),
                                                  math.floor(50 * Game.DISPLAY_RATIO),
                                                  Game.settings["music_volume"],
                                                  image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_17"),
                                                  image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_5"),
                                                  image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_23"),
                                                  image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_11"),
                                                  image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_12"),
                                                  image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_6"),
                                                  image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                  image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_COLORBAR_2")),
                    "music_volume_title": Text(math.floor(620 * Game.DISPLAY_RATIO),
                                               math.floor(430 * Game.DISPLAY_RATIO),
                                               "Volume de la musique",
                                               math.floor(25 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),
                    "sound_volume_slider": Slider(math.floor(970 * Game.DISPLAY_RATIO),
                                                  math.floor(380 * Game.DISPLAY_RATIO),
                                                  math.floor(470 * Game.DISPLAY_RATIO),
                                                  math.floor(50 * Game.DISPLAY_RATIO),
                                                  Game.settings["sound_volume"],
                                                  image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_16"),
                                                  image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_4"),
                                                  image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_22"),
                                                  image_right_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_10"),
                                                  image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_11"),
                                                  image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_5"),
                                                  image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                                  image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_COLORBAR_3")),
                    "sound_volume_title": Text(math.floor(1125 * Game.DISPLAY_RATIO),
                                               math.floor(430 * Game.DISPLAY_RATIO),
                                               "Volume des effets",
                                               math.floor(25 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),

                    "window_graphics": Window(math.floor(409 * Game.DISPLAY_RATIO), math.floor(505 * Game.DISPLAY_RATIO), 5, 6),
                    "graphics_title": Text(math.floor(550 * Game.DISPLAY_RATIO),
                                           math.floor(515 * Game.DISPLAY_RATIO),
                                           "Options graphiques",
                                           math.floor(50 * Game.DISPLAY_RATIO),
                                           (0, 0, 0),
                                           "dpt.fonts.DINOT_CondBlack"),
                    "left_button": Button(math.floor(440 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          math.floor(43 * Game.DISPLAY_RATIO),
                                          math.floor(50 * Game.DISPLAY_RATIO),
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7")),
                    "right_button": Button(math.floor(840 * Game.DISPLAY_RATIO),
                                           math.floor(800 * Game.DISPLAY_RATIO),
                                           math.floor(43 * Game.DISPLAY_RATIO),
                                           math.floor(50 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13")),
                    "graphics_text": Text(math.floor(500 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          "Par défaut",
                                          math.floor(30 * Game.DISPLAY_RATIO),
                                          (0, 0, 0),
                                          "dpt.fonts.DINOT_CondBlack",
                                          centerx=math.floor(660 * Game.DISPLAY_RATIO),
                                          centery=math.floor(825 * Game.DISPLAY_RATIO)),
                    "graphics_checkbox": Checkbox(math.floor(840 * Game.DISPLAY_RATIO),
                                                  math.floor(675 * Game.DISPLAY_RATIO),
                                                  0.7),
                    "graphics_checkbox_text": Text(math.floor(890 * Game.DISPLAY_RATIO),
                                                   math.floor(675 * Game.DISPLAY_RATIO),
                                                   "60 FPS",
                                                   math.floor(30 * Game.DISPLAY_RATIO),
                                                   (0, 0, 0),
                                                   "dpt.fonts.DINOT_CondBlack"),

                    "window_server": Window(math.floor(1022 * Game.DISPLAY_RATIO), math.floor(505 * Game.DISPLAY_RATIO), 4, 6),
                    "server_title": Text(math.floor(1080 * Game.DISPLAY_RATIO),
                                         math.floor(515 * Game.DISPLAY_RATIO),
                                         "Options de connexion",
                                         math.floor(50 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack"),
                    "default_server_button": RadioButton(math.floor(1100 * Game.DISPLAY_RATIO),
                                                         math.floor(625 * Game.DISPLAY_RATIO),
                                                         0.7,
                                                         btn_list),
                    "custom_server_button": RadioButton(math.floor(1100 * Game.DISPLAY_RATIO),
                                                        math.floor(675 * Game.DISPLAY_RATIO),
                                                        0.7,
                                                        btn_list),
                    "default_server_text": Text(math.floor(1150 * Game.DISPLAY_RATIO),
                                                math.floor(620 * Game.DISPLAY_RATIO),
                                                "Serveur officiel",
                                                math.floor(30 * Game.DISPLAY_RATIO),
                                                (0, 0, 0),
                                                "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text": Text(math.floor(1150 * Game.DISPLAY_RATIO),
                                               math.floor(670 * Game.DISPLAY_RATIO),
                                               "Serveur privé",
                                               math.floor(30 * Game.DISPLAY_RATIO),
                                               (0, 0, 0),
                                               "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_button": Button(math.floor(1330 * Game.DISPLAY_RATIO),
                                                        math.floor(665 * Game.DISPLAY_RATIO),
                                                        math.floor(69 * Game.DISPLAY_RATIO),
                                                        math.floor(52 * Game.DISPLAY_RATIO),
                                                        RessourceLoader.get("dpt.images.gui.buttons.BTN_PLAIN_2"),
                                                        text_sprite=SimpleSprite(math.floor(40 * Game.DISPLAY_RATIO),
                                                                                 math.floor(30 * Game.DISPLAY_RATIO),
                                                                                 RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                    "custom_server_text_1": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(710 * Game.DISPLAY_RATIO),
                                                 "Attention, cet option permet de se",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_2": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(735 * Game.DISPLAY_RATIO),
                                                 "connecter à un serveur, pas de le créer !",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_3": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(760 * Game.DISPLAY_RATIO),
                                                 "Voir la documentation pour plus d'infor-",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),
                    "custom_server_text_4": Text(math.floor(1100 * Game.DISPLAY_RATIO),
                                                 math.floor(785 * Game.DISPLAY_RATIO),
                                                 "mations sur la création de serveurs.",
                                                 math.floor(25 * Game.DISPLAY_RATIO),
                                                 (0, 0, 0),
                                                 "dpt.fonts.DINOT_CondBlack"),

                    "window_menu": Window(50 * Game.DISPLAY_RATIO, 0, 2, 6, centery=Game.WINDOW_HEIGHT // 2),
                    "apply_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                           math.floor(390 * Game.DISPLAY_RATIO),
                                           math.floor(92 * Game.DISPLAY_RATIO),
                                           math.floor(95 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=SimpleSprite(math.floor(50 * Game.DISPLAY_RATIO),
                                                                    math.floor(47 * Game.DISPLAY_RATIO),
                                                                    RessourceLoader.get("dpt.images.gui.symbols.SYMB_CHECK"))),
                    "cancel_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(495 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                            text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                     math.floor(50 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.SYMB_BIGX"))),
                    "return_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(600 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                            text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                     math.floor(33 * Game.DISPLAY_RATIO),
                                                                     RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW")))
                    }

        if Game.settings["server_address"] == Game.DEFAULT_SERVER_ADDRESS:
            Game.gui["default_server_button"].value = True
        else:
            Game.gui["custom_server_button"].value = True

        Game.temp["display_size"] = Game.settings["display_size"]
        Game.temp["prev"] = Game.settings.copy()

        Game.gui["graphics_checkbox"].value = Game.settings["30_FPS"] == 1

        # Loops
        from dpt.engine.mainLoop import settings_menu_loop
        Game.loop = settings_menu_loop
        return True

    @classmethod
    def levels_menu(cls):
        """Met en place les élèments du menu de choix de niveau

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """

    @classmethod
    def start_level(cls):
        """Met en place les élèments du menu de début de niveau

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        cls.logger.info("Displaying START_LEVEL")

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.webCommunications import WebCommunication
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        Game.gui = {"window": Window(0, 0, 10, 10, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                    "title": Text(0,
                                  math.floor(230 * Game.DISPLAY_RATIO),
                                  "Démarrer une nouvelle session",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=Game.WINDOW_WIDTH // 2),
                    "session1": Text(0,
                                     math.floor(320 * Game.DISPLAY_RATIO),
                                     "ID de session :",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.WINDOW_WIDTH // 2),
                    "session2": Text(0,
                                     math.floor(350 * Game.DISPLAY_RATIO),
                                     WebCommunication.sessionName,
                                     math.floor(120 * Game.DISPLAY_RATIO),
                                     (84, 66, 243),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.WINDOW_WIDTH // 2),
                    "session3": Text(0,
                                     math.floor(525 * Game.DISPLAY_RATIO),
                                     "ou utilisez directement le lien",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.WINDOW_WIDTH // 2),
                    "session4": Text(0,
                                     math.floor(555 * Game.DISPLAY_RATIO),
                                     Game.settings["server_address"] + "/?session=" + WebCommunication.sessionName,
                                     math.floor(70 * Game.DISPLAY_RATIO),
                                     (84, 66, 243),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.WINDOW_WIDTH // 2),
                    "session5": Text(0,
                                     math.floor(635 * Game.DISPLAY_RATIO),
                                     "(Le lien a été copié dans votre presse-papier)",
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     (0, 0, 0),
                                     "dpt.fonts.DINOT_CondBlack",
                                     centerx=Game.WINDOW_WIDTH // 2),
                    "button_start": Button(math.floor(Game.WINDOW_WIDTH / 2 + 50 * Game.DISPLAY_RATIO),
                                           math.floor(Game.DISPLAY_RATIO * 720), button_width, button_height,
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                    math.floor(50 * Game.DISPLAY_RATIO),
                                                                    RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_previous": Button(math.floor(Game.WINDOW_WIDTH / 2 - button_width - 50 * Game.DISPLAY_RATIO),
                                              math.floor(Game.DISPLAY_RATIO * 720),
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(33 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW"))),
                    "wb_player_count": Text(0, 0,
                                            "Connexion au serveur...",
                                            math.floor(25 * Game.DISPLAY_RATIO),
                                            (0, 0, 0),
                                            "dpt.fonts.DINOT_CondBlack"),
                    "wb_session": Text(0, math.floor(25 * Game.DISPLAY_RATIO),
                                       "Session non disponnible",
                                       math.floor(25 * Game.DISPLAY_RATIO),
                                       (0, 0, 0),
                                       "dpt.fonts.DINOT_CondBlack")}

        Game.gui["wb_player_count"].rect.right = Game.WINDOW_WIDTH - math.floor(10 * Game.DISPLAY_RATIO)
        Game.gui["wb_session"].rect.right = Game.WINDOW_WIDTH - math.floor(10 * Game.DISPLAY_RATIO)

        from tkinter import Tk
        root = Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append("http://" + Game.settings["server_address"] + "/?session=" + WebCommunication.sessionName)
        root.update()
        root.destroy()

        Game.temp["next_level"] = Game.selected_level
        Game.temp["coins"] = 0

        # Loops
        from dpt.engine.mainLoop import start_level_loop
        Game.loop = start_level_loop
        return True

    @classmethod
    def end_level(cls):
        """Met en place les élèments du menu de fin de niveau

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.gui.editor.tileEditor import TileEditor
        from dpt.engine.gui.menu.timer import Timer
        from dpt.engine.tileManager import TileManager
        import time

        if TileEditor.enabled_editor:
            return

        cls.logger.info("Displaying END_LEVEL")

        from dpt.engine.effectsManagement import EffectsManagement
        EffectsManagement.reset()
        EffectsManagement.upsidedown = False

        # Score
        Game.temp["score"] = Game.temp["coins"] * 50 + Timer.time * 10
        if "respawn" in Game.temp:
            Game.temp["score"] -= Game.temp["respawn"] * 500
        Game.temp["score"] = max(Game.temp["score"], 0)
        Game.temp["score_display"] = 0
        Game.temp["score_sound"] = True
        Game.temp["1_done"] = False
        Game.temp["2_done"] = False
        Game.temp["3_done"] = False
        Game.temp["start"] = False
        Game.temp["chrono"] = 0

        if TileManager.levelName not in Game.saves:
            Game.saves[TileManager.levelName] = {}
        Game.temp["time"] = math.floor(time.time())
        Game.saves[TileManager.levelName].update({Game.temp["time"]: Game.temp["score"]})
        Game.save_profile()

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.gui.menu.fade import FadeOut
        from dpt.engine.gui.menu.score_stars import TransitionStar
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
        buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)
        buttons_x = (Game.WINDOW_WIDTH // 2) - (button_width // 2)

        Game.gui.update({"el_window": Window(0, 0, 5, 9, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                         "el_title": Text(0,
                                          buttons_starting_y - math.floor(90 * Game.DISPLAY_RATIO),
                                          "Victoire !",
                                          math.floor(50 * Game.DISPLAY_RATIO),
                                          (0, 0, 0),
                                          "dpt.fonts.DINOT_CondBlack",
                                          centerx=Game.WINDOW_WIDTH // 2),
                         "el_title_1": Text(0,
                                            buttons_starting_y - math.floor(10 * Game.DISPLAY_RATIO),
                                            "Score :",
                                            math.floor(30 * Game.DISPLAY_RATIO),
                                            (0, 0, 0),
                                            "dpt.fonts.DINOT_CondBlack",
                                            centerx=Game.WINDOW_WIDTH // 2),
                         "el_title_score": Text(0,
                                                buttons_starting_y + math.floor(20 * Game.DISPLAY_RATIO),
                                                "0",
                                                math.floor(90 * Game.DISPLAY_RATIO),
                                                (0, 0, 0),
                                                "dpt.fonts.DINOT_CondBlack",
                                                centerx=Game.WINDOW_WIDTH // 2),
                         "el_button_name": Button(math.floor(1185 * Game.DISPLAY_RATIO),
                                                  math.floor(755 * Game.DISPLAY_RATIO),
                                                  math.floor(69 * Game.DISPLAY_RATIO),
                                                  math.floor(52 * Game.DISPLAY_RATIO),
                                                  RessourceLoader.get("dpt.images.gui.buttons.BTN_PLAIN_2"),
                                                  text_sprite=SimpleSprite(math.floor(40 * Game.DISPLAY_RATIO),
                                                                           math.floor(30 * Game.DISPLAY_RATIO),
                                                                           RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                         "el_button_main_menu": Button(buttons_x - button_width - buttons_gap_y, buttons_starting_y + (buttons_gap_y + button_height) * 3, button_width, button_height,
                                                       RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                                       pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                                       text_sprite=SimpleSprite(math.floor(50 * Game.DISPLAY_RATIO),
                                                                                math.floor(38 * Game.DISPLAY_RATIO),
                                                                                RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                         "el_button_quit": Button(buttons_x + button_width + buttons_gap_y, buttons_starting_y + (buttons_gap_y + button_height) * 3,
                                                  button_width,
                                                  button_height,
                                                  RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                                  pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                                  text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                           math.floor(50 * Game.DISPLAY_RATIO),
                                                                           RessourceLoader.get("dpt.images.gui.symbols.SYMB_X"))),
                         "star_3": TransitionStar(Game.WINDOW_WIDTH // 2 + math.floor(Game.DISPLAY_RATIO * 85), buttons_starting_y + math.floor(150 * Game.DISPLAY_RATIO), Game.temp["score"] >= 1000, True, False),
                         "star_2": TransitionStar(Game.WINDOW_WIDTH // 2, buttons_starting_y + math.floor(150 * Game.DISPLAY_RATIO), Game.temp["score"] >= 2000, True, False),
                         "star_1": TransitionStar(Game.WINDOW_WIDTH // 2 - math.floor(Game.DISPLAY_RATIO * 85), buttons_starting_y + math.floor(150 * Game.DISPLAY_RATIO), Game.temp["score"] >= 3000, True, False),
                         "fade": FadeOut(4000)})

        # Sons
        pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.flakey_a_major"))
        pygame.mixer_music.play()

        # Loops
        from dpt.engine.mainLoop import end_level_loop
        Game.loop = end_level_loop
        return True

    @classmethod
    def game_over(cls):
        """Met en place les élèments du menu d'échec

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """

        from dpt.engine.loader import RessourceLoader
        from dpt.engine.gui.editor.tileEditor import TileEditor

        if TileEditor.enabled_editor:
            return

        # Musiques et sons
        def music():
            for i in range(0, 101):
                pygame.time.wait(10)
                pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * ((100 - i) / 100))
            pygame.mixer.pause()
            pygame.mixer.music.pause()

        Thread(target=music).start()

        from dpt.engine.effectsManagement import EffectsManagement
        EffectsManagement.reset()
        EffectsManagement.upsidedown = False

        cls.logger.info("Displaying GAME_OVER")

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        buttons_gap_y = math.floor(15 * Game.DISPLAY_RATIO)
        buttons_starting_y = math.floor((Game.WINDOW_HEIGHT / 2) - button_height * 2 - buttons_gap_y * 1.5) + math.floor(32 * Game.DISPLAY_RATIO)
        buttons_x = (Game.WINDOW_WIDTH // 2) - (button_width // 2)

        Game.gui.update({"go_window": Window(0, 0, 3, 9, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                         "go_title": Text(0,
                                          buttons_starting_y - math.floor(90 * Game.DISPLAY_RATIO),
                                          "Échec",
                                          math.floor(50 * Game.DISPLAY_RATIO),
                                          (0, 0, 0),
                                          "dpt.fonts.DINOT_CondBlack",
                                          centerx=Game.WINDOW_WIDTH // 2),
                         "go_button_checkpoint": Button(buttons_x, buttons_starting_y, button_width, button_height,
                                                        RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                                        pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                                        text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                                 math.floor(40 * Game.DISPLAY_RATIO),
                                                                                 RessourceLoader.get("dpt.images.gui.symbols.SYMB_REPLAY"))),
                         "go_button_main_menu": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 2, button_width, button_height,
                                                       RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                                       pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                                       text_sprite=SimpleSprite(math.floor(50 * Game.DISPLAY_RATIO),
                                                                                math.floor(38 * Game.DISPLAY_RATIO),
                                                                                RessourceLoader.get("dpt.images.gui.symbols.SYMB_MENU"))),
                         "go_button_quit": Button(buttons_x, buttons_starting_y + (buttons_gap_y + button_height) * 3,
                                                  button_width,
                                                  button_height,
                                                  RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                                  pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                                  text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                           math.floor(50 * Game.DISPLAY_RATIO),
                                                                           RessourceLoader.get("dpt.images.gui.symbols.SYMB_X")))})

        from dpt.engine.mainLoop import game_over_loop
        Game.loop = game_over_loop
        return True

    @classmethod
    def return_error(cls, *messages):
        """Met en place les élèments du menu d'erreur

        :param messages: Messages d'erreur
        :type messages: str

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        import dpt.engine.gui.menu as menu
        from dpt.engine.loader import RessourceLoader

        pygame.mixer.music.stop()
        pygame.mixer.stop()
        pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"])
        pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
        pygame.mixer_music.play(-1)

        menu.delete_items()
        Scenes.main_menu(False)

        cls.logger.info("Displaying RETURN_ERROR")

        # Ajout du GUI
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        from random import randint

        Game.gui.update({"window_error": Window(0, 0, 6, 4, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                         "title_error": Text(0,
                                             math.floor(425 * Game.DISPLAY_RATIO),
                                             "Erreur",
                                             math.floor(50 * Game.DISPLAY_RATIO),
                                             (0, 0, 0),
                                             "dpt.fonts.DINOT_CondBlack",
                                             centerx=Game.WINDOW_WIDTH // 2)})

        for i in range(len(messages)):
            Game.gui["message_" + str(randint(1000, 9999))] = Text(0, 0, messages[i],
                                                                   math.floor(25 * Game.DISPLAY_RATIO),
                                                                   (193, 39, 45),
                                                                   "dpt.fonts.DINOT_CondBlack",
                                                                   centerx=Game.WINDOW_WIDTH // 2,
                                                                   centery=(Game.WINDOW_HEIGHT // 2 + math.floor(30 * Game.DISPLAY_RATIO) - (math.floor(12.5 * Game.DISPLAY_RATIO) * len(messages)) + (math.floor((25 * i) * Game.DISPLAY_RATIO))))

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True

    @classmethod
    def loading(cls):
        """Met en place les élèments du menu des paramètres

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.gui.menu.progressbar import ProgressBar

        cls.logger.info("Displaying LOADING")

        Game.temp["text"] = ""
        Game.temp["count"] = 0

        pbar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_BARFRAME.png")
        bar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_COLORBAR_2.png")
        width = min(Game.WINDOW_WIDTH - 50, 1115)
        height = min(math.floor(52 / 1115 * width), 52)
        pb = ProgressBar(math.floor(Game.WINDOW_WIDTH / 2 - width / 2),
                         math.floor(Game.WINDOW_HEIGHT - height), width, height, pbar, bar, 1)
        pb.value = 1
        Game.temp["font"] = pygame.font.SysFont("arial", math.floor(20 * Game.DISPLAY_RATIO))

        Game.temp["text_rendered"] = Game.temp["font"].render("Chargement", True, (0, 0, 0))
        Game.temp["rect"] = Game.temp["text_rendered"].get_rect()
        Game.temp["rect"].centerx = Game.WINDOW_WIDTH // 2
        Game.temp["rect"].centery = math.floor(Game.WINDOW_HEIGHT - height / 2)
        return True

    @classmethod
    def level_selector(cls):
        """Met en place les élèments du menu de selection des niveaux

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.mainLoop import loading_loop

        # Construction de la liste des niveaux
        if Game.levels_list is None:
            Game.levels_list = []

            # Enregistrement des niveau et chargement
            Scenes.loading()
            for level in RessourceLoader.select_entries(Game.LEVELS_ENTRIES):
                Game.levels_list.append(level)
                RessourceLoader.add_pending(level)
                loading_loop()
            loading_loop(True)
            RessourceLoader.load()

            # Chargement des images

            to_del = []

            Scenes.loading()
            for level in Game.levels_list:
                try:
                    level = RessourceLoader.get(level)
                    try:
                        RessourceLoader.add_pending(level["infos"]["image"])
                    except KeyError:
                        RessourceLoader.add_pending("dpt.images.not_found")
                    loading_loop()
                except UnreachableRessourceError:
                    to_del.append(level)
                    continue
            loading_loop(True)
            RessourceLoader.load()

            for i in to_del:
                Game.levels_list.remove(i)

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.gui.menu.levelOverview import LevelOverview
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        Game.gui = {"window": Window(0, 0, 15, 15, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                    "title": Text(0,
                                  math.floor(70 * Game.DISPLAY_RATIO),
                                  "Selectionner un niveau",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=Game.WINDOW_WIDTH // 2),
                    "button_previous": Button(0,
                                              math.floor(Game.DISPLAY_RATIO * 890),
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(33 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW")),
                                              centerx=Game.WINDOW_WIDTH // 2)}

        Game.stars = 0

        x_count = 0
        y_count = 0

        for level_name in Game.levels_list:
            Game.gui[level_name + "_overview"] = LevelOverview(math.floor((90 + (x_count * 180)) * Game.DISPLAY_RATIO),
                                                               math.floor((170 + (y_count * 180)) * Game.DISPLAY_RATIO),
                                                               level_name, 1)
            x_count += 1
            if x_count > 6:
                x_count = 0
                y_count += 1

        # Loops
        from dpt.engine.mainLoop import level_selector_loop
        Game.loop = level_selector_loop
        return True

    @classmethod
    def level_selector_detail(cls):
        """Met en place les élèments du menu de details de selection des niveaux

        :return: True en cas de réussite, sinon False
        :rtype: bool
        """
        from dpt.engine.loader import RessourceLoader

        cls.logger.info("Displaying LEVEL_SELECTOR_DETAIL")

        # Déclaration des varibales
        from dpt.engine.loader import UnreachableRessourceError
        level = None
        level_name = Game.selected_level
        level_title = None
        level_image = None
        level_scores = None
        level_scores_date = None

        try:
            level = RessourceLoader.get(level_name)
        except UnreachableRessourceError:
            return False

        try:
            level_title = level["infos"]["title"]
        except KeyError:
            level_title = "Sans nom"

        try:
            RessourceLoader.get(level["infos"]["image"])
            level_image = RessourceLoader.get(level["infos"]["image"])
        except UnreachableRessourceError:
            level_image = RessourceLoader.get("dpt.images.not_found")
        except KeyError:
            level_image = RessourceLoader.get("dpt.images.not_found")

        try:
            level_scores_date = ["––/––/––––" for i in range(5)]
            level_scores = ["––––" for i in range(5)]

            temp = {k: int(v) for k, v in Game.saves[level_name].copy().items()}

            for i in range(5):
                try:
                    val = max(temp, key=lambda key: temp[key])
                    try:
                        level_scores_date[i] = time.strftime("%d/%m/%Y", time.localtime(int(val)))
                    except ValueError:
                        level_scores_date[i] = val
                    level_scores[i] = str(temp[val])
                    del temp[val]
                except ValueError:
                    continue
        except KeyError:
            pass

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.simpleSprite import SimpleSprite
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.text import Text
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)

        Game.gui = {"window": Window(0, 0, 5, 15, centerx=Game.WINDOW_WIDTH // 2, centery=Game.WINDOW_HEIGHT // 2),
                    "title": Text(0,
                                  math.floor(70 * Game.DISPLAY_RATIO),
                                  "Selectionner un niveau",
                                  math.floor(50 * Game.DISPLAY_RATIO),
                                  (0, 0, 0),
                                  "dpt.fonts.DINOT_CondBlack",
                                  centerx=Game.WINDOW_WIDTH // 2),
                    "level_image": SimpleSprite(math.floor(400 * Game.DISPLAY_RATIO),
                                                math.floor(400 * Game.DISPLAY_RATIO),
                                                level_image,
                                                centerx=Game.WINDOW_WIDTH // 2,
                                                y=math.floor(155 * Game.DISPLAY_RATIO)),
                    "level_title": Text(0,
                                        math.floor(555 * Game.DISPLAY_RATIO),
                                        level_title,
                                        math.floor(40 * Game.DISPLAY_RATIO),
                                        (0, 0, 0),
                                        "dpt.fonts.DINOT_CondBlack",
                                        centerx=Game.WINDOW_WIDTH // 2),
                    "score_title": Text(0,
                                        math.floor(650 * Game.DISPLAY_RATIO),
                                        "Meilleurs scores",
                                        math.floor(30 * Game.DISPLAY_RATIO),
                                        (0, 0, 0),
                                        "dpt.fonts.DINOT_CondBlack",
                                        centerx=Game.WINDOW_WIDTH // 2),
                    "button_start": Button(math.floor(Game.WINDOW_WIDTH / 2 + 50 * Game.DISPLAY_RATIO),
                                           math.floor(Game.DISPLAY_RATIO * 890), button_width, button_height,
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                    math.floor(50 * Game.DISPLAY_RATIO),
                                                                    RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_main_menu": Button(math.floor(Game.WINDOW_WIDTH / 2 - button_width - 50 * Game.DISPLAY_RATIO),
                                               math.floor(Game.DISPLAY_RATIO * 890),
                                               button_width,
                                               button_height,
                                               RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                               pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                               text_sprite=SimpleSprite(math.floor(47 * Game.DISPLAY_RATIO),
                                                                        math.floor(33 * Game.DISPLAY_RATIO),
                                                                        RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW")))}

        # Ajout des scores
        for i in range(5):
            date_name = level_scores_date[i]
            if len(date_name) > 10:
                date_name = date_name[:10] + "..."
            Game.gui.update({"score_" + str(i) + "_date": Text((Game.WINDOW_WIDTH // 2) - 90,
                                                               math.floor((690 + i * 25) * Game.DISPLAY_RATIO),
                                                               date_name,
                                                               math.floor(25 * Game.DISPLAY_RATIO),
                                                               (0, 0, 0),
                                                               "dpt.fonts.DINOT_CondBlack"),
                             "score_" + str(i): Text((Game.WINDOW_WIDTH // 2) + 50,
                                                     math.floor((690 + i * 25) * Game.DISPLAY_RATIO),
                                                     level_scores[i],
                                                     math.floor(25 * Game.DISPLAY_RATIO),
                                                     (0, 0, 0),
                                                     "dpt.fonts.DINOT_CondBlack")})

        # Loops
        from dpt.engine.mainLoop import level_selector_detail_loop
        Game.loop = level_selector_detail_loop
        return True
