import math
from dpt.engine.gui.editor.editorPanel import EditorPanel
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.gui.menu.bar import Bar
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.progressbar import ProgressBar
from dpt.engine.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game
import pygame


def do_synch_anims():
    # Lava
    if Game.animCountLava + 1 >= 104:
        Game.animCountLava = 0
    else:
        Game.animCountLava += 1

    # Water
    if Game.animCountWater + 1 >= 52:
        Game.animCountWater = 0
    else:
        Game.animCountWater += 1


def redraw_Game_window():
    TileManager.environmentGroup.update()
    if not TileEditor.inEditor:
        TileManager.camera.update(Game.playerSprite)
    elif TileEditor.inEditor:
        TileManager.editorCamera.update(Game.playerSprite)

    TileEditor.update()

    try:
        TileManager.editorPanelGroup.update()
        TileManager.editorPanelGroup.draw(Game.surface)
    except pygame.error:
        Game.get_logger("MainLoop").critical("Error when drawing editorPanelGroup")
        Game.get_logger("MainLoop").critical("Content: ")
        for sp in TileManager.editorPanelGroup:
            try:
                Game.get_logger("MainLoop").critical("    " + str(sp.block))
            except AttributeError:
                pass
        raise

    TileEditor.ghostBlockGroup.draw(Game.surface)

    Game.playerGroup.update()

    TileManager.enemyGroup.update()
    TileManager.entityGroup.update()
    TileManager.outOfWindow()

    Button.buttonsGroup.update()
    Button.buttonsGroup.draw(Game.surface)
    for i in Button.text_buttonsList:
        Game.surface.blit(i[0], i[1])
    Game.text_buttonsGroup = []

    ProgressBar.progressbarGroup.update()
    Bar.barGroup.update()
    Bar.barGroup.draw(Game.surface)
    ProgressBar.progressbarGroup.draw(Game.surface)

    Checkbox.checkboxGroup.update()
    Checkbox.checkboxGroup.draw(Game.surface)

    Game.display_debug_info()
    Game.window.update()


# Mainloop
def loop():
    global bg
    bg = RessourceLoader.get("dpt.images.environment.background.background")
    run = True
    while run:
        Game.clock.tick(27)
        Game.surface.blit(bg, (0, 0))

        Game.events = pygame.event.get()

        for event in Game.events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            elif event.type == Game.BUTTONEVENT:
                TileEditor.inEditor = not TileEditor.inEditor
                TileEditor.panelOpen = False
                TileManager.loadLevel(TileManager.levelName)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    TileManager.scrollUp()
                elif event.button == 5:
                    TileManager.scrollDown()

        do_synch_anims()
        redraw_Game_window()

    pygame.quit()
