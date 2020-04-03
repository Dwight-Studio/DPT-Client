from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.game import Game
import pygame

def redraw_Game_window():
    Game.surface.blit(bg, (0, 0))
    Game.tile.update()
    Game.camera.update(Game.playerSprite)
    Game.joueur.update()
    Game.platforms.update()
    Game.window.update()


# Mainloop
def loop():
    global bg

    screen_width, screen_height = Game.surface.get_size()
    Game.playerSprite = PlayerSprite(300, screen_height - 500, 64, 64)
    Game.joueur.add(Game.playerSprite)
    bg = Game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        Game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        redraw_Game_window()

    pygame.quit()