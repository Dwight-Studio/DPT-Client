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
                if platformes.rect.y - (game.playerSprite.rect.y + game.playerSprite.height) <= 0:
                    if game.playerSprite.isFalling:
                        game.playerSprite.onPlatform = True
                        game.playerSprite.isJump = False
                        game.playerSprite.jumpCount = game.playerSprite.CONSTJUMPCOUNT
                        game.playerSprite.isFalling = False
                elif platformes.rect.y + platformes.height - platformes.rect.y >= 0:
                    if game.playerSprite.isJump:
                        game.playerSprite.jumpCount = 0
