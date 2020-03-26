import pygame
import math

from dpt.engine.graphics.characters.PlayerSprite import PlayerSprite
from dpt.game import Game
from dpt.engine.graphics.characters.Player import Player


def redraw_game_window():
    game = Game.get_instance()
    game.window.blit(bg, (0, 0))
    game.player.draw(game.window)
    """allsprites = pygame.sprite.RenderPlain(game.playerSprite)
    allsprites.update()
    allsprites.draw(game.window)"""
    pygame.display.update()


# Mainloop
def loop():
    global bg
    game = Game.get_instance()
    screen_width, screen_height = game.window.get_size()
    """game.playerSprite = PlayerSprite(300, screen_height - 100, 64, 64)"""
    game.player = Player(300, screen_height - 100, 64, 64)
    bg = game.ressources.get("dpt.images.environment.background")
    run = True
    while run:
        game.clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and game.player.x > game.player.vel:
            game.player.x -= game.player.vel
            game.player.left = True
            game.player.right = False
            game.player.standing = False
        elif keys[pygame.K_LEFT]:
            game.player.x = 0
            game.player.left = True
            game.player.right = False
            game.player.standing = False
        elif keys[pygame.K_RIGHT] and game.player.x + game.player.width + game.player.vel < screen_width:
            game.player.x += game.player.vel
            game.player.left = False
            game.player.right = True
            game.player.standing = False
        elif keys[pygame.K_RIGHT]:
            game.player.x = screen_width - game.player.width
            game.player.left = False
            game.player.right = True
            game.player.standing = False
        else:
            game.player.standing = True
            game.player.walkCount = 0

        if not game.player.isJump:
            if keys[pygame.K_UP]:
                game.player.isJump = True
                game.player.left = False
                if game.player.right:
                    game.player.right = True
                else:
                    game.player.right = False
                game.player.walkCount = 0
        else:
            if game.player.jumpCount >= -game.player.CONSTJUMPCOUNT:
                neg = 1
                if game.player.jumpCount < 0:
                    neg = -1
                game.player.y -= math.floor((game.player.jumpCount ** 2) * 0.5) * neg
                game.player.jumpCount -= 1
            else:
                game.player.isJump = False
                game.player.jumpCount = game.player.CONSTJUMPCOUNT

        redraw_game_window()

    pygame.quit()
