import math
import pygame

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
    mouse_pushed_l = False
    mouse_pushed_r = False
    panel_open = False
    enabled_editor = False
    can_edit = False
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

    @classmethod
    def update(cls):
        """S'occupe de toutes la parties placement/suppression de blocs de l'éditeur de niveau"""
        from dpt.engine.tileManager import TileManager
        if cls.enabled_editor:
            cls.can_edit = True
            Game.freeze_game = True
            TileManager.camera.enable_grid()
            # Gestion des fichiers (raccourcis)
            mouse_buttons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            keysmods = pygame.key.get_mods()
            for key in keys:
                # Ouvrir un fichier
                if keysmods == 4160 or keysmods == 4224:
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
                    if keys[pygame.K_n] and not cls.npushed:
                        cls.npushed = True
                        TileManager.environment_group.empty()
                        TileManager.entity_group.empty()
                        TileManager.background_blocks_group.empty()
                        TileManager.deadly_object_group.empty()
                        TileManager.interactible_blocks_group.empty()
                        cls.created_level.clear()
                    elif not keys[pygame.K_n] and cls.npushed:
                        cls.npushed = False
                    if keys[pygame.K_t] and not cls.tpushed and not cls.panel_open:
                        cls.tpushed = True
                        cls.panel_open = True
                        TileManager.open_tile_panel()
                    elif keys[pygame.K_t] and not cls.tpushed and cls.panel_open:
                        cls.tpushed = True
                        TileManager.editor_panel_group.empty()
                        Checkbox.checkbox_group.empty()
                        cls.panel_open = False
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
                    if cls.custom_tile_placement and mouse[0] != cls.last_mouse_pos_x_c or mouse[
                        1] != cls.last_mouse_pos_y_c:
                        cls.last_mouse_pos_x_c = 0
                        cls.last_mouse_pos_y_c = 0
                        TileEditor.ghost_block_group.empty()
                        TileManager.ghost_block(mouse[0], mouse[1], TileEditor.selected_item)
            except:
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
            if mouse_buttons[0] == 1:
                for interact in TileManager.interactible_blocks_group:
                    if isinstance(interact, RessourceLoader.get(
                            "dpt.entities.interactible.lever")) and interact.x + interact.offset_x + TileManager.camera.last_x <= \
                            mouse[
                                0] <= interact.x + interact.offset_x + interact.width and interact.y + interact.offset_y <= \
                            mouse[1] <= interact.y + interact.offset_y + interact.height:
                        return
                    if isinstance(interact, RessourceLoader.get(
                            "dpt.entities.interactible.spike")) and interact.x + TileManager.camera.last_x <= mouse[
                        0] <= interact.x + interact.width and interact.y + interact.offset_y <= mouse[1] <= interact.y:
                        return

            if mouse_buttons[0] == 1 and not cls.mouse_pushed_l:
                cls.mouse_pushed_l = True
                if not cls.panel_open or cls.mouse_pos_x <= math.floor(((Game.surface.get_size()[
                                                                             0] / 4 * 3 - Game.TILESIZE) - TileManager.camera.last_x) / Game.TILESIZE):
                    cls.last_mouse_pos_x = cls.mouse_pos_x
                    cls.last_mouse_pos_y = cls.mouse_pos_y
                    cls.last_mouse_pos_x_c = mouse[0]
                    cls.last_mouse_pos_y_c = mouse[1]
                    if not cls.custom_tile_placement:
                        if not TileManager.check_back:
                            if str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y) in cls.created_level:
                                cls.created_level[str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)][
                                    "class"] = TileEditor.selected_item
                                for blocks in TileManager.environment_group:
                                    if math.floor(
                                            blocks.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                            blocks.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                        blocks.kill()
                                        del blocks
                                for blocks in TileManager.interactible_blocks_group:
                                    if math.floor(
                                            blocks.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                            blocks.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                        blocks.kill()
                                        del blocks
                                for entity in TileManager.entity_group:
                                    if math.floor(
                                            entity.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                            entity.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                        entity.kill()
                                        del entity
                            else:
                                cls.created_level[str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)] = {
                                    "class": TileEditor.selected_item}

                            TileManager.place_block(cls.mouse_pos_x, cls.mouse_pos_y, TileEditor.selected_item)
                        elif TileManager.check_back:
                            if str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y) in cls.created_level:
                                cls.created_level[str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)][
                                    "backgroundClass"] = TileEditor.selected_item
                                for blocks in TileManager.background_blocks_group:
                                    if math.floor(
                                            blocks.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                            blocks.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                        blocks.kill()
                                        del blocks
                            else:
                                cls.created_level[str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)] = {
                                    "backgroundClass": TileEditor.selected_item}
                            TileManager.place_back_block(cls.mouse_pos_x, cls.mouse_pos_y, TileEditor.selected_item)
                    elif cls.custom_tile_placement:
                        if not TileManager.check_back:
                            if str(mouse[0]) + ", " + str(mouse[1]) in cls.created_level:
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])][
                                    "class"] = TileEditor.selected_item
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])]["customPlace"] = True
                            else:
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])] = {
                                    "class": TileEditor.selected_item, "customPlace": True}
                            TileManager.place_block(mouse[0] - TileManager.camera.last_x, mouse[1],
                                                    TileEditor.selected_item)
                        elif TileManager.check_back:
                            if str(mouse[0]) + ", " + str(mouse[1]) in cls.created_level:
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])][
                                    "backgroundClass"] = TileEditor.selected_item
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])]["customPlace"] = True
                            else:
                                cls.created_level[str(mouse[0]) + ", " + str(mouse[1])] = {
                                    "backgroundClass": TileEditor.selected_item, "customPlace": True}
                            TileManager.place_back_block(mouse[0] - TileManager.camera.last_x, mouse[1],
                                                         TileEditor.selected_item)
            elif mouse_buttons[0] != 1 and cls.mouse_pushed_l:
                cls.mouse_pushed_l = False
            elif mouse_buttons[
                0] == 1 and cls.mouse_pos_x != cls.last_mouse_pos_x or cls.mouse_pos_y != cls.last_mouse_pos_y and cls.mouse_pushed_l:
                cls.mouse_pushed_l = False
            if mouse_buttons[2] == 1 and not cls.mouse_pushed_r:
                cls.mouse_pushed_r = True
                if not cls.panel_open or cls.mouse_pos_x <= math.floor(((Game.surface.get_size()[
                                                                             0] / 4 * 3 - Game.TILESIZE) - TileManager.camera.last_x) / Game.TILESIZE):
                    cls.last_mouse_pos_x = cls.mouse_pos_x
                    cls.last_mouse_pos_y = cls.mouse_pos_y
                    try:
                        for cls.backnd in TileManager.background_blocks_group:
                            try:
                                if cls.backnd.customPlacement:
                                    if cls.backnd.rect.left <= mouse[0] <= cls.backnd.rect.right and cls.backnd.rect.top <= mouse[1] <= cls.backnd.rect.bottom:
                                        cls.mouse_pos_y = cls.backnd.rect.y - cls.backnd.offset_y
                                        cls.mouse_pos_x = cls.backnd.rect.x - cls.backnd.offset_x
                                        cls.backnd.kill()
                                        del cls.backnd
                            except AttributeError:
                                if math.floor(cls.backnd.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(cls.backnd.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                    cls.backnd.kill()
                                    del cls.backnd
                        for cls.env in TileManager.environment_group:
                            try:
                                if cls.env.customPlacement:
                                    if cls.env.rect.left <= mouse[0] <= cls.env.rect.right and cls.env.rect.top <= mouse[1] <= cls.entity.rect.bottom:
                                        cls.mouse_pos_y = cls.env.rect.y - cls.env.offset_y
                                        cls.mouse_pos_x = cls.env.rect.x - cls.env.offset_x
                                        cls.env.kill()
                                        del cls.env
                            except AttributeError:
                                if math.floor(
                                        cls.env.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(cls.env.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                    cls.env.kill()
                                    del cls.env
                        for cls.intera in TileManager.interactible_blocks_group:
                            try:
                                if cls.intera.customPlacement:
                                    if cls.intera.rect.left <= mouse[0] <= cls.intera.rect.right and cls.intera.rect.top <= mouse[1] <= cls.intera.rect.bottom:
                                        cls.mouse_pos_y = cls.intera.rect.y - cls.intera.offset_y
                                        cls.mouse_pos_x = cls.intera.rect.x - cls.intera.offset_x
                                        cls.intera.kill()
                                        del cls.intera
                            except AttributeError:
                                if math.floor(cls.intera.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                        cls.intera.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                    cls.intera.kill()
                                    del cls.intera
                        for cls.entitys in TileManager.entity_group:
                            try:
                                if cls.entitys.customPlacement:
                                    if cls.entitys.rect.left <= mouse[0] <= cls.entitys.rect.right and cls.entitys.rect.top <= mouse[1] <= cls.entitys.rect.bottom:
                                        cls.mouse_pos_y = cls.entitys.rect.y - cls.entitys.offset_y
                                        cls.mouse_pos_x = cls.entitys.rect.x - cls.entitys.offset_x
                                        cls.entitys.kill()
                                        del cls.entitys
                            except AttributeError:
                                if math.floor(
                                        cls.entitys.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                        cls.entitys.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                    cls.entitys.kill()
                                    del cls.entitys
                        for cls.dead in TileManager.entity_group:
                            try:
                                if cls.dead.customPlacement:
                                    if cls.dead.rect.left <= mouse[0] <= cls.entitys.rect.right and cls.entitys.rect.top <= mouse[1] <= cls.entitys.rect.bottom:
                                        cls.mouse_pos_y = cls.dead.rect.y - cls.dead.offset_y
                                        cls.mouse_pos_x = cls.dead.rect.x - cls.dead.offset_x
                                        cls.dead.kill()
                                        del cls.dead
                            except AttributeError:
                                if math.floor(
                                        cls.dead.rect.centerx / Game.TILESIZE) == cls.mouse_pos_x and math.floor(
                                        cls.dead.rect.centery / Game.TILESIZE) == cls.mouse_pos_y:
                                    cls.dead.kill()
                                    del cls.dead
                        del cls.created_level[str(cls.mouse_pos_x) + ", " + str(cls.mouse_pos_y)]
                    except KeyError:
                        pass
            elif mouse_buttons[1] != 1 and cls.mouse_pushed_r:
                cls.mouse_pushed_r = False
            elif mouse_buttons[
                1] == 1 and cls.mouse_pos_x != cls.last_mouse_pos_x or cls.mouse_pos_y != cls.last_mouse_pos_y and cls.mouse_pushed_r:
                cls.mouse_pushed_r = False
