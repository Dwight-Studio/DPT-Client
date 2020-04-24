import math
import dpt.engine.gui.menu as menu
import pygame
import tkinter as tk
from tkinter import simpledialog

from dpt.engine.fileManager import FileManager
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.scenes import Scenes
from dpt.engine.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game

bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
bg = pygame.transform.smoothscale(bg, Game.surface.get_size())


def do_synch_anims():
    # Lava
    if Game.anim_count_lava + 1 >= 208:
        Game.anim_count_lava = 0
    else:
        Game.anim_count_lava += 1

    # Water
    if Game.anim_count_water + 1 >= 104:
        Game.anim_count_water = 0
    else:
        Game.anim_count_water += 1

    # Coins
    if Game.anim_count_coins + 1 >= 144:
        Game.anim_count_coins = 0
    else:
        Game.anim_count_coins += 1


# Mainloops
def level_loop():
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            if TileEditor.in_editor:
                FileManager.save_file(TileEditor.created_level)
            #   Game.com.close()
            Game.run = False
        elif event.type == Game.BUTTON_EVENT and event.button == Game.gui["editor_button"]:
            TileEditor.in_editor = not TileEditor.in_editor
            if TileEditor.in_editor:
                Game.gui["editor_button"].text = "Jouer"
                for clouds in TileManager.clouds_group:
                    clouds.kill()
            else:
                Game.gui["editor_button"].text = "Retour"
            TileEditor.panel_open = False
            Checkbox.checkbox_group.empty()
            TileManager.clouds_group.empty()
            TileManager.load_level(TileManager.levelName)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and TileEditor.in_editor:
                TileManager.scroll_up()
            elif event.button == 5 and TileEditor.in_editor:
                TileManager.scroll_down()

    do_synch_anims()
    TileManager.clouds_group.update()
    TileManager.update_clouds()
    TileManager.out_of_window()
    TileManager.interactible_blocks_group.update()
    TileManager.camera.update(Game.player_sprite)
    TileEditor.update()

    try:
        TileManager.editor_panel_group.update()
        TileManager.editor_panel_group.draw(Game.surface)
    except pygame.error:
        Game.get_logger("MainLoop").critical("Error when drawing editorPanelGroup")
        Game.get_logger("MainLoop").critical("Content: ")
        for sp in TileManager.editor_panel_group:
            try:
                Game.get_logger("MainLoop").critical("    " + str(sp.block))
            except AttributeError:
                pass
        raise

    TileEditor.ghost_block_group.draw(Game.surface)

    Button.main_loop()

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def pause_loop():
    pass


def main_menu_loop():
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["button_play"]:
                menu.delete_items()
                Scenes.level("dpt.levels.leveltest")
                pygame.mixer_music.fadeout(1000)
                pygame.mixer_music.unload()
                return
            elif event.button == Game.gui["button_editor"]:
                menu.delete_items()
                Scenes.editor("dpt.levels.leveltest")
                pygame.mixer_music.fadeout(1000)
                pygame.mixer_music.unload()
                return
            elif event.button == Game.gui["button_settings"]:
                menu.delete_items()
                Scenes.settings_menu()
                return
            elif event.button == Game.gui["button_quit"]:
                menu.delete_items()
                pygame.mixer_music.fadeout(1000)
                pygame.mixer_music.unload()
                Game.run = False
                return

    menu.main_loop()

    image = RessourceLoader.get("dpt.images.dpt")
    image = pygame.transform.smoothscale(image,
                                         (math.floor(1480 * Game.DISPLAY_RATIO), math.floor(600 * Game.DISPLAY_RATIO)))
    rect = image.get_rect()
    rect.centerx = Game.surface.get_size()[0] // 2
    rect.bottom = (Game.surface.get_size()[1] // 4) * 3
    Game.surface.blit(image, rect)

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def settings_menu_loop():
    Game.surface.blit(bg, (0, 0))

    menu.main_loop()

    def apply_settings():
        Game.settings["general_volume"] = Game.gui["general_volume_slider"].value
        Game.settings["music_volume"] = Game.gui["music_volume_slider"].value
        Game.settings["sound_volume"] = Game.gui["sound_volume_slider"].value
        if Game.temp is not None and Game.gui["custom_server_button"]:
            Game.settings["server_address"] = Game.temp
        elif Game.gui["default_server_button"]:
            Game.settings["server_address"] = Game.DEFAULT_SERVER_ADDRESS
        pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])
        Game.surface = Game.window.set_mode((Game.settings["window_width"], Game.settings["window_height"]), pygame.NOFRAME)
        Game.save_settings()

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["apply_button"]:
                apply_settings()
            if event.button == Game.gui["cancel_button"]:
                pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])
                Game.surface = Game.window.set_mode((Game.settings["window_width"], Game.settings["window_height"]), pygame.NOFRAME)
                menu.delete_items()
                Game.save_settings()
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["return_button"]:
                apply_settings()
                menu.delete_items()
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["custom_server_text_button"]:
                root = tk.Tk()
                root.withdraw()
                s = simpledialog.askstring("Adresse du serveur", "URL (sans le http(s)://)", parent=root, )
                if s is not None:
                    Game.temp = s

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()
