from dpt.game import Game
from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.engine.graphics.tileManager import *
from dpt.engine.collisionsDetector import Detector

game = Game.get_instance()
tile = TileManager()
camera = Camera(tile.maxWidthSize, tile.maxWidthSize)


def redraw_game_window():
    game.surface.blit(bg, (0, 0))
    tile.enableGrid()
    game.joueur.update()
    game.platforms.update()
    for sprites in  game.joueur:
        game.surface.blit(sprites.image, camera.apply(sprites))
    for sprite in game.platforms:
        game.surface.blit(sprite.image, camera.apply(sprite))
    game.joueur.draw(game.surface)
    game.window.update()


# Mainloop
def loop():
    global bg

    game = Game.get_instance()
    screen_width, screen_height = game.surface.get_size()
    game.playerSprite = PlayerSprite(300, screen_height - 100, 64, 64)
    game.joueur.add(game.playerSprite)
    bg = game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        collisions = Detector()
        camera.update(game.playerSprite)

        redraw_game_window()

    pygame.quit()
