import pygame

from dpt.game import Game


class Detector:
    def __init__(self):
        game = Game.get_instance()
        hits = pygame.sprite.spritecollide(game.playerSprite, game.platforms, False)
        if hits:
            for platformes in hits:
                print("Point en haut à gauche :", platformes.rect.x, platformes.rect.y)
                print("Point en bas à droite :", platformes.rect.x + platformes.width, platformes.rect.y + platformes.height)
                if platformes.rect.x - game.playerSprite.rect.x <= 0:
                    if game.playerSprite.isFalling:
                        game.playerSprite.onPlatform = True
                        game.playerSprite.isJump = False
                        game.playerSprite.jumpCount = game.playerSprite.CONSTJUMPCOUNT
                        game.playerSprite.isFalling = False
