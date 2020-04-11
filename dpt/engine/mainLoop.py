import pygame

from dpt.engine.graphics.gui.editor import EditorPanel
from dpt.engine.graphics.gui.editor.tileEditor import TileEditor
from dpt.engine.graphics.gui.menu.Button import Button
from dpt.engine.graphics.tileManager import TileManager
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


def redraw_Game_window():
    TileManager.environmentGroup.update()
    if not TileEditor.inEditor:
        TileManager.camera.update(Game.playerSprite)
    elif TileEditor.inEditor:
        TileManager.editorCamera.update(Game.playerSprite)
    TileEditor.update()
    EditorPanel.editorPanelGroup.draw(Game.surface)
    EditorPanel.editorPanelGroup.update()
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
    Game.display_debug_info()
    Game.window.update()


# Mainloop
def loop():
    global bg
    bg = RessourceLoader.get("dpt.images.environment.background")
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
                Game.playerGroup.empty()
                TileManager.entityGroup.empty()
                TileEditor.ghostBlockGroup.empty()
                TileManager.loadLevel(TileManager.levelName)

        redraw_Game_window()

    pygame.quit()
