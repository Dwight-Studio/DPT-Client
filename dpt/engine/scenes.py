import math
import pygame

from dpt.game import Game


class Scenes:
    logger = Game.get_logger("Scenes")

    @classmethod
    def editor(cls, level):
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
        RessourceLoader.unload()
        RessourceLoader.add_pending("dpt.images.gui.buttons.BTN_GREEN_RECT_*")
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_out")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_in")

        # Initialisation du TileManager
        TileEditor.in_editor = True
        if not TileManager.load_level(level):
            return False

        # Ajout du bouton d'éditeur
        Game.gui = {"editor_button": Button(0, Game.surface.get_size()[1] - math.floor(50 * Game.DISPLAY_RATIO),
                                            math.floor(127 * Game.DISPLAY_RATIO),
                                            math.floor(46 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Jouer")}

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def level(cls, level):
        cls.logger.info("Displaying LEVEL")
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Gestion des ressources
        RessourceLoader.unload()

        # Initialisation du TileManager
        TileEditor.in_editor = False
        if not TileManager.load_level(level):
            return False

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def pause(cls):
        cls.logger.info("Displaying PAUSE")
        # Loops
        from dpt.engine.mainLoop import pause_loop
        Game.loop = pause_loop
        return True

    @classmethod
    def main_menu(cls, load=True):
        cls.logger.info("Displaying MAIN_MENU")
        from dpt.engine.loader import RessourceLoader

        # Gestion des ressources
        if load:
            RessourceLoader.unload()
            RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
            RessourceLoader.add_pending("dpt.images.gui.*")
            RessourceLoader.add_pending("dpt.images.dpt")
            RessourceLoader.add_pending("dpt.fonts.*")
            RessourceLoader.add_pending("dpt.sounds.musics.story_time")
            RessourceLoader.add_pending("dpt.sounds.sfx.switch6")
            RessourceLoader.load()

        # Gestion de la musique
        if load:
            pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
            pygame.mixer_music.play(-1)

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu import Window
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)
        buttons_gap_x = math.floor(80 * Game.DISPLAY_RATIO)
        buttons_starting_x = math.floor((Game.surface.get_size()[0] / 2) - button_width * 2 - buttons_gap_x * 1.5)
        buttons_y = (Game.surface.get_size()[1] // 4) * 3 + 50 * Game.DISPLAY_RATIO
        Game.gui = {"button_play": Button(buttons_starting_x, buttons_y, button_width, button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_editor": Button(buttons_starting_x + (button_width + buttons_gap_x), buttons_y,
                                            button_width,
                                            button_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(50 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_PLUS"))),
                    "button_settings": Button(buttons_starting_x + (button_width + buttons_gap_x) * 2, buttons_y,
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                           math.floor(50 * Game.DISPLAY_RATIO),
                                                                           RessourceLoader.get("dpt.images.gui.symbols.SYMB_SETTINGS"))),
                    "button_quit": Button(buttons_starting_x + (button_width + buttons_gap_x) * 3, buttons_y,
                                          button_width,
                                          button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                       math.floor(50 * Game.DISPLAY_RATIO),
                                                                       RessourceLoader.get("dpt.images.gui.symbols.SYMB_X"))),
                    "window": Window((Game.surface.get_size()[0] // 2) - math.floor(122 * 3 * Game.DISPLAY_RATIO),
                                     buttons_y + button_height // 2 - math.floor(64 * 1.5 * Game.DISPLAY_RATIO), 6, 3)}

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True

    @classmethod
    def settings_menu(cls):
        cls.logger.info("Displaying SETTINGS_MENU")
        from dpt.engine.loader import RessourceLoader

        # Ajout du GUI
        from dpt.engine.gui.menu.slider import Slider
        from dpt.engine.gui.menu import Window
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        from dpt.engine.gui.menu.text import Text
        from dpt.engine.gui.menu.ratioButton import RatioButton

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
                    "left_button": Button(math.floor(490 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          math.floor(43 * Game.DISPLAY_RATIO),
                                          math.floor(50 * Game.DISPLAY_RATIO),
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7")),
                    "right_button": Button(math.floor(890 * Game.DISPLAY_RATIO),
                                           math.floor(800 * Game.DISPLAY_RATIO),
                                           math.floor(43 * Game.DISPLAY_RATIO),
                                           math.floor(50 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13")),
                    "graphics_text": Text(math.floor(550 * Game.DISPLAY_RATIO),
                                          math.floor(800 * Game.DISPLAY_RATIO),
                                          "Par défaut",
                                          math.floor(30 * Game.DISPLAY_RATIO),
                                          (0, 0, 0),
                                          "dpt.fonts.DINOT_CondBlack",
                                          centerx=math.floor(711 * Game.DISPLAY_RATIO),
                                          centery=math.floor(825 * Game.DISPLAY_RATIO)),

                    "window_server": Window(math.floor(1022 * Game.DISPLAY_RATIO), math.floor(505 * Game.DISPLAY_RATIO), 4, 6),
                    "server_title": Text(math.floor(1080 * Game.DISPLAY_RATIO),
                                         math.floor(515 * Game.DISPLAY_RATIO),
                                         "Options de connexion",
                                         math.floor(50 * Game.DISPLAY_RATIO),
                                         (0, 0, 0),
                                         "dpt.fonts.DINOT_CondBlack"),
                    "default_server_button": RatioButton(math.floor(1100 * Game.DISPLAY_RATIO),
                                                         math.floor(625 * Game.DISPLAY_RATIO),
                                                         0.7,
                                                         btn_list),
                    "custom_server_button": RatioButton(math.floor(1100 * Game.DISPLAY_RATIO),
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
                                                        text_sprite=TextSpriteButton(math.floor(40 * Game.DISPLAY_RATIO),
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

                    "window_menu": Window(50 * Game.DISPLAY_RATIO, 0, 2, 6, centery=Game.surface.get_size()[1] // 2),
                    "apply_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                           math.floor(390 * Game.DISPLAY_RATIO),
                                           math.floor(92 * Game.DISPLAY_RATIO),
                                           math.floor(95 * Game.DISPLAY_RATIO),
                                           RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                           pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                           text_sprite=TextSpriteButton(math.floor(50 * Game.DISPLAY_RATIO),
                                                                        math.floor(47 * Game.DISPLAY_RATIO),
                                                                        RessourceLoader.get("dpt.images.gui.symbols.SYMB_CHECK"))),
                    "cancel_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(495 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(50 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_BIGX"))),
                    "return_button": Button(math.floor(125 * Game.DISPLAY_RATIO),
                                            math.floor(600 * Game.DISPLAY_RATIO),
                                            math.floor(92 * Game.DISPLAY_RATIO),
                                            math.floor(95 * Game.DISPLAY_RATIO),
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(math.floor(47 * Game.DISPLAY_RATIO),
                                                                         math.floor(33 * Game.DISPLAY_RATIO),
                                                                         RessourceLoader.get("dpt.images.gui.symbols.SYMB_LEFTARROW")))
                    }

        if Game.settings["server_address"] == Game.DEFAULT_SERVER_ADDRESS:
            Game.gui["default_server_button"].value = True
        else:
            Game.gui["custom_server_button"].value = True

        Game.temp["display_size"] = Game.settings["display_size"]
        Game.temp["prev"] = Game.settings.copy()

        # Loops
        from dpt.engine.mainLoop import settings_menu_loop
        Game.loop = settings_menu_loop
        return True
