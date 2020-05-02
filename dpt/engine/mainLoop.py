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
from dpt.engine.gui.menu import Text
from threading import Thread

try:
    bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
    bg = pygame.transform.smoothscale(bg, Game.surface.get_size())
except:
    pass


def do_synch_anims():
    """Gère les annimations synchronisées"""
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
    """Boucle des niveaux"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            Scenes.pause()
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
    TileManager.clouds_group.draw(Game.surface)
    TileManager.update_clouds()
    TileManager.out_of_window()
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

    # if not TileEditor.in_editor and Game.count % 1800 == 0:
    # Game.effects_management.update()
    # Game.count += 1

    # Comptage des joueurs
    if not TileEditor.in_editor:
        def count():
            try:
                nb = Game.com.get_player_count()
                if nb is None:
                    Game.gui["players_text"].text = "Déconnecté du serveur"
                    Game.gui["players_text"].color = (254, 0, 61)
                else:
                    nb = str()
                    while len(nb) < 3:
                        nb = "0" + nb
                    Game.gui["players_text"].text = "Joueurs connectés : " + nb
            except KeyError:
                pass

        try:
            if Game.com is not None:
                if Game.temp["player_count_check"] + 1 >= 60:
                    Game.temp["player_count_check"] = 0
                    Thread(target=count).start()
                else:
                    Game.temp["player_count_check"] += 1
            else:
                Game.gui["players_text"].text = "Déconnecté des serveurs"
                Game.gui["players_text"].color = (254, 0, 61)
        except KeyError:
            pass

    Text.main_loop()
    Button.main_loop()

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def pause_loop():
    """Boucle de pause"""
    Game.surface.blit(bg, (0, 0))

    TileManager.camera.update(Game.player_sprite, True)
    TileManager.clouds_group.draw(Game.surface)

    menu.main_loop()

    for event in Game.events:
        if event.type == pygame.QUIT:
            if Game.com is not None:
                Scenes.loading()
                Game.com.close()
                Game.loading = False
            if TileEditor.in_editor:
                FileManager.save_file(TileEditor.created_level)
            Game.run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu.delete_items()
            Game.loop = Game.temp["prev_loop"]
            return
        if event.type == Game.BUTTON_EVENT:
            menu.delete_items()
            if event.button == Game.gui["button_resume"]:
                Game.loop = Game.temp["prev_loop"]
                return
            elif event.button == Game.gui["button_restart"]:
                menu.delete_items()
                Scenes.level(TileManager.levelName)
                return
            elif event.button == Game.gui["button_main_menu"]:
                if Game.com is not None:
                    Scenes.loading()
                    Game.com.close()
                    Game.loading = False
                if TileEditor.in_editor:
                    FileManager.save_file(TileEditor.created_level)
                menu.delete_items()
                Scenes.main_menu()
                return
            elif event.button == Game.gui["button_quit"]:
                if Game.com is not None:
                    Scenes.loading()
                    Game.com.close()
                    Game.loading = False
                if TileEditor.in_editor:
                    FileManager.save_file(TileEditor.created_level)
                Game.run = False

        # Comptage des joueurs
        if not TileEditor.in_editor:
            def count():
                try:
                    nb = Game.com.get_player_count()
                    if nb is None:
                        Game.gui["players_text"].text = "Déconnecté du serveur"
                        Game.gui["players_text"].color = (254, 0, 61)
                    else:
                        nb = str()
                        while len(nb) < 3:
                            nb = "0" + nb
                        Game.gui["players_text"].text = "Joueurs connectés : " + nb
                except KeyError:
                    pass

            try:
                if Game.com is not None:
                    if Game.temp["player_count_check"] + 1 >= 60:
                        Game.temp["player_count_check"] = 0
                        Thread(target=count).start()
                    else:
                        Game.temp["player_count_check"] += 1
                else:
                    Game.gui["players_text"].text = "Déconnecté des serveurs"
                    Game.gui["players_text"].color = (254, 0, 61)
            except KeyError:
                pass

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def main_menu_loop():
    """Boucle du menu principale"""
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["button_play"]:
                menu.delete_items()

                Scenes.loading()

                # Initialisation de la session (dans un thread pour ne pas bloquer)
                from dpt.engine.webCommunications import Communication
                Game.com = Communication()
                if not Game.com.create():
                    Scenes.return_error(["Impossible de se connecter au serveur de jeu.",
                                         "Verifiez votre connexion internet et réessayer",
                                         " ",
                                         "Si le problème persiste, vous pouvez nous contacter sur Discord",
                                         "Dwight Studio Hub: discord.gg/yZwuNqN",
                                         "(Lien copié dans le presse-papier)"])

                    from tkinter import Tk
                    root = Tk()
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append("https://discord.gg/yZwuNqN")
                    root.update()
                    root.destroy()
                    Game.loading = False
                    return

                Game.loading = False
                Scenes.start_level("dpt.levels.leveltest")
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

    image = RessourceLoader.get("dpt.images.dpt")
    image = pygame.transform.smoothscale(image,
                                         (math.floor(1480 * Game.DISPLAY_RATIO), math.floor(600 * Game.DISPLAY_RATIO)))
    rect = image.get_rect()
    rect.centerx = Game.surface.get_size()[0] // 2
    rect.bottom = (Game.surface.get_size()[1] // 4) * 3
    Game.surface.blit(image, rect)

    menu.main_loop()

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def settings_menu_loop():
    """Boucle du menu des paramètres"""
    Game.surface.blit(bg, (0, 0))

    ds = Game.temp["display_size"]
    Game.gui["graphics_text"].text, w, h = Game.display_list[ds]

    menu.main_loop()

    def apply_settings():
        Game.settings["general_volume"] = Game.gui["general_volume_slider"].value
        Game.settings["music_volume"] = Game.gui["music_volume_slider"].value
        Game.settings["sound_volume"] = Game.gui["sound_volume_slider"].value

        Game.settings["display_size"] = ds

        if "s" in Game.temp and Game.gui["custom_server_button"]:
            Game.settings["server_address"] = Game.temp["s"]
        elif Game.gui["default_server_button"]:
            Game.settings["server_address"] = Game.DEFAULT_SERVER_ADDRESS
        pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])

        if Game.temp["prev"]["display_size"] != Game.settings["display_size"]:
            Game.update_display()
            global bg
            bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
            bg = pygame.transform.smoothscale(bg, Game.surface.get_size())
            menu.delete_items()
            Game.save_settings()
            Game.temp = {}
            Scenes.settings_menu()

        Game.save_settings()

    for event in Game.events:
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            apply_settings()
            menu.delete_items()
            Game.temp = {}
            Scenes.main_menu(load=False)
            return
        if event.type == Game.BUTTON_EVENT:
            if event.button == Game.gui["left_button"]:
                Game.temp["display_size"] -= 1
                Game.temp["display_size"] = max(Game.temp["display_size"], 0)
                Game.temp["display_size"] = min(Game.temp["display_size"], 5)
            if event.button == Game.gui["right_button"]:
                Game.temp["display_size"] += 1
                Game.temp["display_size"] = max(Game.temp["display_size"], 0)
                Game.temp["display_size"] = min(Game.temp["display_size"], 5)
            if event.button == Game.gui["apply_button"]:
                apply_settings()
            if event.button == Game.gui["cancel_button"]:
                pygame.mixer_music.set_volume(Game.settings["general_volume"] * Game.settings["music_volume"])
                menu.delete_items()
                Game.save_settings()
                Game.temp = {}
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["return_button"]:
                apply_settings()
                menu.delete_items()
                Game.temp = {}
                Scenes.main_menu(load=False)
                return
            if event.button == Game.gui["custom_server_text_button"]:
                root = tk.Tk()
                root.withdraw()
                s = simpledialog.askstring("Adresse du serveur", "URL (sans le http(s)://)", parent=root, )
                if s is not None:
                    Game.temp["s"] = s

    rect1 = pygame.rect.Rect(0,
                             math.floor(600 * Game.DISPLAY_RATIO),
                             math.floor(175 * (Game.surface.get_size()[0] / Game.surface.get_size()[1]) * Game.DISPLAY_RATIO),
                             math.floor(175 * Game.DISPLAY_RATIO))
    rect1.centerx = Game.gui["window_graphics"].rect.centerx

    if w == 0:
        w = Game.SCREEN_WIDTH
    if h == 0:
        h = Game.SCREEN_HEIGHT

    w_rect_t = math.floor((w / Game.SCREEN_WIDTH) * rect1.width)
    h_rect_t = math.floor((h / Game.SCREEN_HEIGHT) * rect1.height)

    w_rect = min(w_rect_t, rect1.width)
    h_rect = min(h_rect_t, rect1.height)

    rect1.width = math.floor((w_rect / w_rect_t) * rect1.width)
    rect1.height = math.floor((h_rect / h_rect_t) * rect1.height)

    rect2 = pygame.rect.Rect(rect1.x,
                             math.floor(600 * Game.DISPLAY_RATIO),
                             w_rect,
                             h_rect)

    pygame.draw.rect(Game.surface, (255, 255, 255, 2), rect1)
    pygame.draw.rect(Game.surface, (0, 0, 0), rect2, width=3)

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def start_level_loop():
    """Boucle de début de niveau"""
    Game.surface.blit(bg, (0, 0))

    # Comptage des joueurs
    if not TileEditor.in_editor:
        def count():
            print("start")
            try:
                nb = Game.com.get_player_count()
                if nb is None:
                    Game.gui["players_text"].text = "Déconnecté du serveur"
                    Game.gui["players_text"].color = (254, 0, 61)
                else:
                    nb = str()
                    while len(nb) < 3:
                        nb = "0" + nb
                    Game.gui["players_text"].text = "Joueurs connectés : " + nb
            except KeyError:
                raise

        try:
            if Game.com is not None:
                if Game.temp["player_count_check"] + 1 >= 60:
                    Game.temp["player_count_check"] = 0
                    Thread(target=count).start()
                else:
                    Game.temp["player_count_check"] += 1
            else:
                Game.gui["players_text"].text = "Déconnecté des serveurs"
                Game.gui["players_text"].color = (254, 0, 61)
        except KeyError:
            raise

    menu.main_loop()

    for event in Game.events:
        if event.type == pygame.QUIT:
            Scenes.loading()
            Game.com.close()
            Game.loading = False
            Game.run = False
            return
        if event.type == Game.BUTTON_EVENT:
            menu.delete_items()
            if event.button == Game.gui["button_main_menu"]:
                Scenes.loading()
                Game.com.close()
                Game.loading = False
                Scenes.main_menu(False)
                return
            elif event.button == Game.gui["button_start"]:
                Scenes.level(Game.temp["next_level"])
                pygame.mixer_music.fadeout(1000)
                pygame.mixer_music.unload()
                return

    menu.main_loop()

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def loading_loop():
    """Boucle de chargement. Boucle spécial car non executée dans game"""
    from dpt.engine.gui.menu import ProgressBar
    pbar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_BARFRAME.png")
    bar = pygame.image.load(Game.ROOT_DIRECTORY + "/ressources/dpt/images/gui/ui/UI_COLORBAR_2.png")
    width = min(Game.surface.get_size()[0] - 50, 1115)
    height = min(math.floor(52 / 1115 * width), 52)
    pb = ProgressBar(math.floor(Game.surface.get_size()[0] / 2 - width / 2),
                     math.floor(Game.surface.get_size()[1] - height), width, height, pbar, bar, 1)
    pb.value = 1
    font = pygame.font.SysFont("arial", math.floor(20 * Game.DISPLAY_RATIO))

    text = font.render("Chargement", True, (0, 0, 0))
    rect = text.get_rect()
    rect.centerx = Game.surface.get_size()[0] // 2
    rect.centery = math.floor(Game.surface.get_size()[1] - height / 2)

    t = ""
    c = 0

    while Game.loading:

        Game.events = pygame.event.get()

        Game.surface.blit(bg, (0, 0))

        if c >= 20:
            t += "."
            if t == "....":
                t = ""
            c = 0
        c += 1

        # Afficahe de la progressbar
        ProgressBar.progress_bar_group.update()
        ProgressBar.bar_group.update()
        ProgressBar.bar_group.draw(Game.surface)
        ProgressBar.progress_bar_group.draw(Game.surface)

        # Affichage du text
        text = font.render("Chargement" + t, True, (0, 0, 0))
        Game.surface.blit(text, rect)

        Game.display_debug_info()
        Game.draw_cursor()
        Game.window.update()
        Game.clock.tick(60)

    ProgressBar.bar_group.empty()
    ProgressBar.progress_bar_group.empty()
