import math

from dpt.engine.fileManager import FileManager
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.progressbar import ProgressBar
from dpt.engine.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game
import pygame

bg = RessourceLoader.get("dpt.images.environment.background.default_sky")
bg = pygame.transform.scale(bg, Game.surface.get_size())


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
    Game.clock.tick(60)
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            if TileEditor.in_editor:
                FileManager.save_file(TileEditor.created_level)
            # Game.com.close()
            Game.run = False
        elif event.type == Game.BUTTON_EVENT and event.button == Game.gui["editor_button"]:
            TileEditor.in_editor = not TileEditor.in_editor
            if TileEditor.in_editor:
                Game.gui["editor_button"].text = "Jouer"
            else:
                Game.gui["editor_button"].text = "Retour"
            TileEditor.panel_open = False
            Checkbox.checkboxGroup.empty()
            TileManager.load_level(TileManager.levelName)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and TileEditor.in_editor:
                TileManager.scroll_up()
            elif event.button == 5 and TileEditor.in_editor:
                TileManager.scroll_down()

    do_synch_anims()
    TileManager.out_of_window()
    TileManager.interactible_blocks.update()
    TileManager.interactible_blocks.draw(Game.surface)
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
    ProgressBar.main_loop()
    Checkbox.main_loop()

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()


def pause_loop():
    pass


def main_menu_loop():
    Game.clock.tick(60)
    Game.surface.blit(bg, (0, 0))

    for event in Game.events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            Game.run = False

    Button.main_loop()
    ProgressBar.main_loop()
    Checkbox.main_loop()

    image = RessourceLoader.get("dpt.images.dpt")
    image = pygame.transform.scale(image, (math.floor(1480 * Game.DISPLAY_RATIO), math.floor(600 * Game.DISPLAY_RATIO)))
    rect = image.get_rect()
    rect.centerx = Game.surface.get_size()[0] // 2
    rect.bottom = (Game.surface.get_size()[1] // 4) * 3
    Game.surface.blit(image, rect)

    Game.display_debug_info()
    Game.draw_cursor()
    Game.window.update()
