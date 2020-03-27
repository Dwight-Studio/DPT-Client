import pygame

from dpt.game import Game
from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite


def redraw_game_window():
    game = Game.get_instance()
    game.sprites.update()
    game.surface.blit(bg, (0, 0))
    game.sprites.draw(game.surface)
    game.window.update()


# Mainloop
def loop():
    global bg
    game = Game.get_instance()
    screen_width, screen_height = game.surface.get_size()
    game.playerSprite = PlayerSprite(300, screen_height - 200, 64, 64)
    game.sprites.add(game.playerSprite)
    bg = game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        redraw_game_window()

    pygame.quit()
