import pygame

from dpt.game import Game
from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.engine.graphics.platforms.Block import Block


def redraw_game_window():
    game = Game.get_instance()
    game.surface.blit(bg, (0, 0))
    game.joueur.update()
    game.platforms.update()
    game.platforms.draw(game.surface)
    game.joueur.draw(game.surface)
    game.window.update()


# Mainloop
def loop():
    global bg
    game = Game.get_instance()
    screen_width, screen_height = game.surface.get_size()
    game.playerSprite = PlayerSprite(300, screen_height - 100, 64, 64)
    game.platform = Block((150, 0, 150), 500, screen_height - 140, 500, 30)
    game.platforms.add(game.platform)
    game.joueur.add(game.playerSprite)
    bg = game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        hits = pygame.sprite.spritecollide(game.playerSprite, game.platforms, False)

        if hits:
            run = False

        redraw_game_window()

    pygame.quit()
