from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.engine.graphics.tileManager import *
from dpt.engine.collisionsDetector import Detector

tile = TileManager()
camera = Camera(tile.maxWidthSize, tile.maxWidthSize)


def redraw_Game_window():
    Game.surface.blit(bg, (0, 0))
    tile.enableGrid()
    Game.joueur.update()
    Game.platforms.update()
    Game.surface.blit(Game.playerSprite.image, camera.apply(Game.playerSprite))
    for sprite in Game.platforms:
        Game.surface.blit(sprite.image, camera.apply(sprite))
    Game.window.update()


# Mainloop
def loop():
    global bg

    screen_width, screen_height = Game.surface.get_size()
    Game.playerSprite = PlayerSprite(300, screen_height - 100, 64, 64)
    Game.joueur.add(Game.playerSprite)
    bg = Game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        Game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        collisions = Detector()
        camera.update(Game.playerSprite)

        redraw_Game_window()

    pygame.quit()
