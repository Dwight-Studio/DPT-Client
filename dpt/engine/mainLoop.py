from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.engine.graphics.gui.editor.tileEditor import TileEditor
from dpt.game import Game
import pygame


def redraw_Game_window():
    Game.environment.update()
    Game.camera.update(Game.playerSprite)
    TileEditor.update()
    Game.editorPanelGroup.draw(Game.surface)
    Game.editorPanelGroup.update()
    Game.ghostBlock.draw(Game.surface)
    Game.player.update()
    Game.enemyGroup.update()
    Game.buttonsGroup.update()
    Game.buttonsGroup.draw(Game.surface)
    for i in Game.text_buttonsGroup:
        Game.surface.blit(i[0], i[1])
    Game.text_buttonsGroup = []
    Game.display_debug_info()
    Game.window.update()


# Mainloop
def loop():
    global bg

    screen_width, screen_height = Game.surface.get_size()
    bg = Game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        Game.clock.tick(27)
        Game.surface.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        redraw_Game_window()

    pygame.quit()
