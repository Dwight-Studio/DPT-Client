from dpt.engine.graphics.enemies.EnemySprite import EnemySprite
from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.game import Game
import pygame


def redraw_Game_window():
    Game.platforms.update()
    Game.camera.update(Game.playerSprite)
    Game.editor.update()
    Game.ghostBlock.draw(Game.surface)
    Game.joueur.update()
    Game.enemyGroup.update()
    Game.display_debug_info()
    Game.window.update()


# Mainloop
def loop():
    global bg

    screen_width, screen_height = Game.surface.get_size()
    Game.playerSprite = PlayerSprite(300, screen_height - 500, 64, 64)
    Game.enemySprite = EnemySprite(500, screen_height - 500, 64, 64)
    Game.joueur.add(Game.playerSprite)
    Game.enemyGroup.add(Game.enemySprite)
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
