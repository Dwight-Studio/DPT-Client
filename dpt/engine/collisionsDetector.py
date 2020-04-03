import pygame

from dpt.game import Game


class Detector:
    def __init__(self):
        hits = pygame.sprite.spritecollide(Game.playerSprite, Game.platforms, False)
        if hits:
            for platformes in hits:
                print("Point en haut à gauche :", platformes.rect.x, platformes.rect.y)
                print("Point en bas à droite :", platformes.rect.x + platformes.width, platformes.rect.y + platformes.height)
                if platformes.rect.y - (Game.playerSprite.rect.y + Game.playerSprite.height) <= 0:
                    if Game.playerSprite.isFalling:
                        Game.playerSprite.onPlatform = True
                        Game.playerSprite.isJump = False
                        Game.playerSprite.jumpCount = Game.playerSprite.CONSTJUMPCOUNT
                        Game.playerSprite.isFalling = False
                elif platformes.rect.y + platformes.height - platformes.rect.y >= 0:
                    if Game.playerSprite.isJump:
                        Game.playerSprite.jumpCount = 0
