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
        Checkbox.checkboxGroup.empty()

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
    def main_menu(cls):
        cls.logger.info("Displaying MAIN_MENU")
        from dpt.engine.loader import RessourceLoader

        # Gestion des ressources
        RessourceLoader.unload()
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.*")
        RessourceLoader.add_pending("dpt.images.dpt")
        RessourceLoader.add_pending("dpt.sounds.musics.story_time")
        RessourceLoader.load()

        # Gestion de la musique
        pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
        pygame.mixer_music.play(-1)

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        button_width = math.floor(92 * Game.DISPLAY_RATIO)
        button_height = math.floor(95 * Game.DISPLAY_RATIO)
        buttons_gap_x = math.floor(80 * Game.DISPLAY_RATIO)
        buttons_starting_x = math.floor((Game.surface.get_size()[0] / 2) - (button_width + buttons_gap_x) * 2)
        buttons_y = (Game.surface.get_size()[1] // 4) * 3 + 50 * Game.DISPLAY_RATIO
        Game.gui = {"button_play": Button(buttons_starting_x, buttons_y, button_width, button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get(
                                              "dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                              "dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_editor": Button(buttons_starting_x + (button_width + buttons_gap_x), buttons_y,
                                            button_width,
                                            button_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                                "dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_settings": Button(buttons_starting_x + (button_width + buttons_gap_x) * 2, buttons_y,
                                              button_width,
                                              button_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get(
                                                  "dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                                  "dpt.images.gui.symbols.SYMB_SETTINGS"))),
                    "button_quit": Button(buttons_starting_x + (button_width + buttons_gap_x) * 3, buttons_y,
                                          button_width,
                                          button_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                              "dpt.images.gui.symbols.SYMB_X")))}

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
        from dpt.engine.gui.menu import ProgressBar
        Game.gui = {"slider": Slider(math.floor(50 * Game.DISPLAY_RATIO),
                                     math.floor(50 * Game.DISPLAY_RATIO),
                                     math.floor(400 * Game.DISPLAY_RATIO),
                                     math.floor(40 * Game.DISPLAY_RATIO),
                                     pygame.mixer_music.get_volume(),
                                     image_left=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_19"),
                                     image_left_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_7"),
                                     image_right=RessourceLoader.get("dpt.images.gui.buttons.BTN_HORIZ_SINGLE_1"),
                                     image_right_pushed=RessourceLoader.get(
                                         "dpt.images.gui.buttons.BTN_HORIZ_SINGLE_13"),
                                     image_slide=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_2"),
                                     image_slide_pushed=RessourceLoader.get("dpt.images.gui.buttons.BTN_SLIDER_SM_8"),
                                     image_progress_bar_frame=RessourceLoader.get("dpt.images.gui.ui.UI_BARFRAME"),
                                     image_progress_bar_bar=RessourceLoader.get("dpt.images.gui.ui.UI_COLORBAR_4"))}

        # Loops
        from dpt.engine.mainLoop import settings_menu_loop
        Game.loop = settings_menu_loop
        return True
