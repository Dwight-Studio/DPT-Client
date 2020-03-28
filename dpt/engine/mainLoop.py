import pygame
import math

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
            print("Point en haut à gauche :", hits[0].rect.x, hits[0].rect.y)
            print("Point en bas à droite :", hits[0].rect.x + hits[0].width, hits[0].rect.y + hits[0].height)
            if game.playerSprite.jumpCount > 0:
                if game.playerSprite.rect.y + math.floor(((game.playerSprite.jumpCount + 1) ** 2) * 0.5) > hits[0].rect.y + hits[0].height:  # Pour détecter si le joueur vient d'en bas
                    game.playerSprite.jumpCount = 0
                elif game.playerSprite.rect.x + game.playerSprite.width - game.playerSprite.vel < hits[0].rect.x:  # Pour détecter si le joueur vient de la gauche
                    game.playerSprite.rect.x = hits[0].rect.x - (game.playerSprite.width // 2)
                elif game.playerSprite.rect.x + game.playerSprite.vel > hits[0].rect.x + hits[0].width:  # Pour détecter si le joueur vient de la droite
                    game.playerSprite.rect.x = hits[0].rect.x + hits[0].width
                    print("C'est pas moi c'est le jeu qui est con!")
            elif game.playerSprite.jumpCount < 0:
                if game.playerSprite.rect.y + game.playerSprite.height - math.floor(((game.playerSprite.jumpCount + 1) ** 2) * 0.5) < hits[0].rect.y:  # Pour détecter si le joueur vient d'en haut
                    game.playerSprite.rect.y = hits[0].rect.y - (game.playerSprite.height // 2)

        redraw_game_window()

    pygame.quit()
