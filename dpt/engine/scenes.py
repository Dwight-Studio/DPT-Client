import math

import pygame

from dpt.game import Game


class Scenes:
    @classmethod
    def editor(cls, level):
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Nettoyage
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.progressbar import ProgressBar
        from dpt.engine.gui.menu.checkbox import Checkbox
        Button.buttonsGroup.empty()
        Button.text_sprite_buttonsGroup.empty()
        ProgressBar.progressbarGroup.empty()
        ProgressBar.barGroup.empty()
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
                                            127,
                                            46,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Jouer")}

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def level(cls, level):
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
        # Loops
        from dpt.engine.mainLoop import pause_loop
        Game.loop = pause_loop
        return True

    @classmethod
    def main_menu(cls):
        from dpt.engine.loader import RessourceLoader

        # Gestion des ressources
        RessourceLoader.unload()
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.ui.UI_WINDOW_*")
        RessourceLoader.add_pending("dpt.images.gui.buttons.*")
        RessourceLoader.add_pending("dpt.images.gui.symbols.*")
        RessourceLoader.add_pending("dpt.images.dpt")
        RessourceLoader.add_pending("dpt.sounds.musics.story_time")
        RessourceLoader.load()

        # Gestion de la musique
        pygame.mixer_music.load(RessourceLoader.get("dpt.sounds.musics.story_time"))
        pygame.mixer_music.play(-1)

        # Ajout du GUI
        from dpt.engine.gui.menu.button import Button
        from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
        buttons_width = math.floor(92 * Game.DISPLAY_RATIO)
        buttons_height = math.floor(95 * Game.DISPLAY_RATIO)
        buttons_gap_x = math.floor(80 * Game.DISPLAY_RATIO)
        buttons_starting_x = math.floor((Game.surface.get_size()[0] / 2) - (buttons_width + buttons_gap_x) * 2)
        buttons_y = (Game.surface.get_size()[1] // 4) * 3 + 50 * Game.DISPLAY_RATIO
        Game.gui = {"button_play": Button(buttons_starting_x, buttons_y, buttons_width, buttons_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get(
                                              "dpt.images.gui.buttons.BTN_GREEN_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                              "dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_editor": Button(buttons_starting_x + (buttons_width + buttons_gap_x), buttons_y,
                                            buttons_width,
                                            buttons_height,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_BLUE_CIRCLE_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_BLUE_CIRCLE_IN"),
                                            text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                                "dpt.images.gui.symbols.SYMB_PLAY"))),
                    "button_settings": Button(buttons_starting_x + (buttons_width + buttons_gap_x) * 2, buttons_y,
                                              buttons_width,
                                              buttons_height,
                                              RessourceLoader.get("dpt.images.gui.buttons.BTN_GRAY_CIRCLE_OUT"),
                                              pushed_image=RessourceLoader.get(
                                                  "dpt.images.gui.buttons.BTN_GRAY_CIRCLE_IN"),
                                              text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                                  "dpt.images.gui.symbols.SYMB_SETTINGS"))),
                    "button_quit": Button(buttons_starting_x + (buttons_width + buttons_gap_x) * 3, buttons_y,
                                          buttons_width,
                                          buttons_height,
                                          RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_OUT"),
                                          pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_RED_CIRCLE_IN"),
                                          text_sprite=TextSpriteButton(47, 50, RessourceLoader.get(
                                              "dpt.images.gui.symbols.SYMB_X")))}

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True
