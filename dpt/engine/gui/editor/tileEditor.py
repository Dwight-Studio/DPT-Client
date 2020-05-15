import math
import pygame
import tkinter as tk
import shutil
import os

from random import randint
from tkinter import simpledialog
from tkinter import filedialog
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class TileEditor:
    selected_item = "dpt.blocks.grass.Grass"  # Item selectionné par le joueur (Éditeur)
    opushed = False
    spushed = False
    npushed = False
    tpushed = False
    ipushed = False
    mouse_pushed_l = False
    mouse_pushed_r = False
    panel_open = False
    is_editing = False
    enabled_editor = False
    mouse_pos_x = None
    mouse_pos_y = None
    last_mouse_pos_x = None
    last_mouse_pos_y = None
    last_mouse_pos_x_c = 0
    last_mouse_pos_y_c = 0
    ghost_block_group = pygame.sprite.Group()
    created_level = {}
    custom_tile_placement = False
    intera = None
    entitys = None
    env = None
    backnd = None
    dead = None
    attributing = False

    @classmethod
    def update(cls):
        """S'occupe de toutes la parties placement/suppression de blocs de l'éditeur de niveau"""
        from dpt.engine.tileManager import TileManager
        if cls.is_editing:
            cls.enabled_editor = True
            Game.freeze_game = True
            TileManager.camera.enable_grid()
            # Gestion des fichiers (raccourcis)
            mouse_buttons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            keysmods = pygame.key.get_mods()
            for key in keys:
                if keysmods == 4160 or keysmods == 4224:
                    # Ouvrir un fichier
                    if keys[pygame.K_o] and not cls.opushed:
                        cls.opushed = True
                        from dpt.engine.fileManager import FileManager
                        FileManager.import_file()
                    elif not keys[pygame.K_o] and cls.opushed:
                        cls.opushed = False
                    # Sauvegarder un fichier
                    if keys[pygame.K_s] and not cls.spushed:
                        cls.spushed = True
                        from dpt.engine.fileManager import FileManager
                        FileManager.save_file(cls.created_level)
                    elif not keys[pygame.K_s] and cls.spushed:
                        cls.spushed = False
                    # Générer un niveau vide
                    if keys[pygame.K_n] and not cls.npushed:
                        cls.npushed = True
                        list = []
                        list.extend(TileManager.environment_group)
                        list.extend(TileManager.entity_group)
                        list.extend(TileManager.background_blocks_group)
                        for sprite in list:
                            sprite.kill()
                        cls.created_level.clear()
                        cls.created_level["tiles"] = {}
                        cls.created_level["infos"] = {}
                    elif not keys[pygame.K_n] and cls.npushed:
                        cls.npushed = False
                    # Ouvrir le panneau des blocs
                    if keys[pygame.K_t] and not cls.tpushed and not cls.panel_open:
                        cls.tpushed = True
                        cls.panel_open = True
                        TileManager.open_tile_panel()
                    elif keys[pygame.K_t] and not cls.tpushed and cls.panel_open:
                        cls.tpushed = True
                        TileManager.editor_panel_group.empty()
                        Checkbox.checkbox_group.empty()
                        cls.panel_open = False
                    elif keys[pygame.K_i] and not cls.ipushed:
                        cls.level_infos_creation()
                        cls.ipushed = True
                    elif not keys[pygame.K_i] and cls.ipushed:
                        cls.ipushed = False
                    elif not keys[pygame.K_t] and cls.tpushed:
                        cls.tpushed = False
            # Gestion de la position de la souris et du placement de blocks
            mouse = pygame.mouse.get_pos()
            cls.mouse_pos_x = math.floor((mouse[0] - TileManager.camera.last_x) / Game.TILESIZE)
            cls.mouse_pos_y = math.floor(mouse[1] / Game.TILESIZE)
            Game.add_debug_info("TILESET INFORMATIONS")
            Game.add_debug_info("Mouse AbsX: " + str(cls.mouse_pos_x))
            Game.add_debug_info("Mouse AbsY: " + str(cls.mouse_pos_y))
            Game.add_debug_info("----------")
            try:
                if RessourceLoader.get(TileEditor.selected_item).customPlacement:
                    cls.custom_tile_placement = True
                    if cls.custom_tile_placement and mouse[0] != cls.last_mouse_pos_x_c or mouse[1] != cls.last_mouse_pos_y_c:
                        cls.last_mouse_pos_x_c = 0
                        cls.last_mouse_pos_y_c = 0
                        TileEditor.ghost_block_group.empty()
                        TileManager.ghost_block(mouse[0], mouse[1], TileEditor.selected_item)
            except AttributeError:
                cls.custom_tile_placement = False

            if not cls.custom_tile_placement:
                if not cls.custom_tile_placement and cls.mouse_pos_x != cls.last_mouse_pos_x or cls.mouse_pos_y != cls.last_mouse_pos_y:
                    cls.last_mouse_pos_x = None
                    cls.last_mouse_pos_y = None
                    TileEditor.ghost_block_group.empty()
                    TileManager.ghost_block((cls.mouse_pos_x * Game.TILESIZE) + TileManager.camera.last_x,
                                            cls.mouse_pos_y * Game.TILESIZE, TileEditor.selected_item)

            if mouse_buttons[0] == 1 or mouse_buttons[1] == 1 or mouse_buttons[2] == 1:
                for btn in Button.buttonsGroup:
                    if btn.rect.collidepoint(mouse[0], mouse[1]):
                        return

            if mouse_buttons[0] == 1 and not cls.mouse_pushed_l:
                cls.mouse_pushed_l = True
                if not cls.panel_open or cls.mouse_pos_x <= math.floor((((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)[
                                                                             0] / 4 * 3 - Game.TILESIZE) - TileManager.camera.last_x) / Game.TILESIZE):
                    cls.last_mouse_pos_x = cls.mouse_pos_x
                    cls.last_mouse_pos_y = cls.mouse_pos_y
                    cls.last_mouse_pos_x_c = mouse[0]
                    cls.last_mouse_pos_y_c = mouse[1]

                    for sprites in TileManager.interactible_blocks_group:
                        if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                            return

                    if not cls.custom_tile_placement:
                        if not TileManager.check_back:
                            if str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y) in cls.created_level["tiles"]:
                                cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)][
                                    "class"] = TileEditor.selected_item
                                for sprites in TileManager.environment_group:
                                    if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                        sprites.kill()
                                        del sprites
                                for sprites in TileManager.entity_group:
                                    if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                        sprites.kill()
                                        del sprites
                            else:
                                cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)] = {
                                    "class": TileEditor.selected_item}

                            TileManager.place_block(cls.mouse_pos_x, cls.mouse_pos_y, TileEditor.selected_item)
                        elif TileManager.check_back:
                            if str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y) in cls.created_level["tiles"]:
                                cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)][
                                    "backgroundClass"] = TileEditor.selected_item
                                for sprites in TileManager.background_blocks_group:
                                    if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                        sprites.kill()
                                        del sprites
                            else:
                                cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)] = {
                                    "backgroundClass": TileEditor.selected_item}
                            TileManager.place_back_block(cls.mouse_pos_x, cls.mouse_pos_y, TileEditor.selected_item)
                    elif cls.custom_tile_placement:
                        if not TileManager.check_back:
                            if str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO) in cls.created_level["tiles"]:
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)][
                                    "class"] = TileEditor.selected_item
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)]["customPlace"] = True
                            else:
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)] = {
                                    "class": TileEditor.selected_item, "customPlace": True}
                            TileManager.place_block(mouse[0] - TileManager.camera.last_x, mouse[1],
                                                    TileEditor.selected_item)
                        elif TileManager.check_back:
                            if str(mouse[0] - TileManager.camera.last_x) + ", " + str(mouse[1]) in cls.created_level["tiles"]:
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)][
                                    "backgroundClass"] = TileEditor.selected_item
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)]["customPlace"] = True
                            else:
                                cls.created_level["tiles"][str((mouse[0] / Game.DISPLAY_RATIO) - TileManager.camera.last_x) + ", " + str(mouse[1] / Game.DISPLAY_RATIO)] = {
                                    "backgroundClass": TileEditor.selected_item, "customPlace": True}
                            TileManager.place_back_block(mouse[0] - TileManager.camera.last_x, mouse[1],
                                                         TileEditor.selected_item)
            elif mouse_buttons[0] != 1 and cls.mouse_pushed_l:
                cls.mouse_pushed_l = False
            elif mouse_buttons[0] == 1 and cls.mouse_pos_x != cls.last_mouse_pos_x or cls.mouse_pos_y != cls.last_mouse_pos_y and cls.mouse_pushed_l:
                cls.mouse_pushed_l = False
            if mouse_buttons[2] == 1 and not cls.mouse_pushed_r:
                cls.mouse_pushed_r = True
                if not cls.panel_open or cls.mouse_pos_x <= math.floor((((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)[
                                                                             0] / 4 * 3 - Game.TILESIZE) - TileManager.camera.last_x) / Game.TILESIZE):
                    cls.last_mouse_pos_x = cls.mouse_pos_x
                    cls.last_mouse_pos_y = cls.mouse_pos_y
                    if TileManager.check_back:
                        for sprites in TileManager.background_blocks_group:
                            if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                if hasattr(sprites, "customPlacement"):
                                    if hasattr(sprites, "x") and hasattr(sprites, "y"):
                                        cls.mouse_pos_y = sprites.y / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = sprites.x / Game.DISPLAY_RATIO
                                    else:
                                        cls.mouse_pos_y = (sprites.rect.y - sprites.offset_y) / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = (sprites.rect.x - sprites.offset_x) / Game.DISPLAY_RATIO
                                    sprites.kill()
                                    del sprites
                                else:
                                    sprites.kill()
                                    del sprites
                                try:
                                    del cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)]["backgroundClass"]
                                except KeyError:
                                    pass
                    else:
                        for sprites in TileManager.environment_group:
                            if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                if hasattr(sprites, "customPlacement"):
                                    if hasattr(sprites, "x") and hasattr(sprites, "y"):
                                        cls.mouse_pos_y = sprites.y / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = sprites.x / Game.DISPLAY_RATIO
                                    else:
                                        cls.mouse_pos_y = (sprites.rect.y - sprites.offset_y) / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = (sprites.rect.x - sprites.offset_x) / Game.DISPLAY_RATIO
                                    sprites.kill()
                                    del sprites
                                else:
                                    sprites.kill()
                                    del sprites
                                try:
                                    del cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)]["class"]
                                except KeyError:
                                    pass
                        for sprites in TileManager.entity_group:
                            if sprites.rect.collidepoint(mouse[0] - TileManager.camera.last_x, mouse[1]):
                                if hasattr(sprites, "customPlacement"):
                                    if hasattr(sprites, "x") and hasattr(sprites, "y"):
                                        cls.mouse_pos_y = sprites.y / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = sprites.x / Game.DISPLAY_RATIO
                                    else:
                                        cls.mouse_pos_y = (sprites.rect.y - sprites.offset_y) / Game.DISPLAY_RATIO
                                        cls.mouse_pos_x = (sprites.rect.x - sprites.offset_x) / Game.DISPLAY_RATIO
                                    sprites.kill()
                                    del sprites
                                else:
                                    sprites.kill()
                                    del sprites
                                try:
                                    del cls.created_level["tiles"][str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)]["class"]
                                except KeyError:
                                    pass
            elif mouse_buttons[1] != 1 and cls.mouse_pushed_r:
                cls.mouse_pushed_r = False
            elif mouse_buttons[1] == 1 and cls.mouse_pos_x != cls.last_mouse_pos_x or cls.mouse_pos_y != cls.last_mouse_pos_y and cls.mouse_pushed_r:
                cls.mouse_pushed_r = False

    @classmethod
    def level_infos_creation(cls):
        root = tk.Tk()
        root.withdraw()

        if "infos" in cls.created_level:
            if "title" in cls.created_level["infos"]:
                level_title = cls.created_level["infos"]["title"]
            else:
                level_title = "Sans nom"

            if "image" in cls.created_level["infos"]:
                image = cls.created_level["infos"]["image"]
            else:
                image = "dpt.images.environment.terrain.Goop_Tile_Flat_Edge_a"

            if "music" in cls.created_level["infos"]:
                music = cls.created_level["infos"]["music"]
            else:
                music = "dpt.sounds.musics.Grasslands_Theme"

            if "required_stars" in cls.created_level["infos"]:
                required_stars = cls.created_level["infos"]["required_stars"]
            else:
                required_stars = 0

            if "background" in cls.created_level["infos"]:
                background = cls.created_level["infos"]["background"]
            else:
                background = "Plains"
        else:
            level_title = "Sans nom"
            image = "dpt.images.environment.terrain.Goop_Tile_Flat_Edge_a"
            required_stars = 0
            background = "Plains"
            music = "dpt.sounds.musics.Grasslands_Theme"

        s = simpledialog.askstring("Titre", f"Titre du niveau (Annuler pour garder '{level_title}')", parent=root, )

        if s is not None:
            level_title = s
        cls.created_level["infos"]["title"] = level_title

        s = filedialog.askopenfilename(parent=root, title="Sélectionner une image (carrées de préférence) pour le niveau (Annuler pour garder l'ancienne image)", filetypes=[("Images", "*.png")])

        if s is not None and not s == "":
            Game.get_logger(cls.__name__).info("Copying image for level creation")
            filename = str(randint(11111, 99999))
            shutil.copy(os.path.realpath(s), Game.ROOT_DIRECTORY + "/ressources/user/images/" + filename + ".png")
            Game.get_logger(cls.__name__).info(os.path.realpath(s) + " --> " + Game.ROOT_DIRECTORY + "/ressources/user/images/" + filename + ".png")
            Game.get_logger(cls.__name__).info("Created entry: " + "user.images." + filename)
            cls.created_level["infos"]["image"] = "user.images." + filename
        else:
            cls.created_level["infos"]["image"] = image

        s = filedialog.askopenfilename(parent=root, title="Sélectionner une musique (boucle) pour le niveau (Annuler pour garder l'ancienne musique)", filetypes=[("Musique", "*.ogg")])

        if s is not None and not s == "":
            Game.get_logger(cls.__name__).info("Copying music for level creation")
            filename = str(randint(11111, 99999))
            shutil.copy(os.path.realpath(s), Game.ROOT_DIRECTORY + "/ressources/user/musics/" + filename + ".music.ogg")
            Game.get_logger(cls.__name__).info(os.path.realpath(s) + " --> " + Game.ROOT_DIRECTORY + "/ressources/user/musics/" + filename + ".music.ogg")
            Game.get_logger(cls.__name__).info("Created entry: " + "user.musics." + filename)
            cls.created_level["infos"]["music"] = "user.musics." + filename
        else:
            cls.created_level["infos"]["music"] = music

        s = simpledialog.askinteger("Nombre d'étoiles", f"Nombre d'étoiles requises pour jouer au niveau (Annuler pour garder '{required_stars}')", parent=root, )

        if s is not None:
            required_stars = s
        cls.created_level["infos"]["required_stars"] = required_stars

        s = simpledialog.askstring("Fond", f"Fond à utiliser ('Plains', 'Desert', 'Ice', 'Goop' uniquement) (Annuler pour garder '{background}')", parent=root, )

        if s is not None and (s == "Plains" or s == "Desert" or s == "Ice" or s == "Goop"):
            background = s
        cls.created_level["infos"]["background"] = background
