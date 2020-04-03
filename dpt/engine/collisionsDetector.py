import pygame

from dpt.game import Game


class Detector(object):
    def __init__(self):
        game = Game.get_instance()
        hits = pygame.sprite.spritecollide(game.playerSprite, game.platforms, False)
        if hits:
            for platformes in hits:
                print("Point en haut à gauche :", platformes.rect.x, platformes.rect.y)
                print("Point en bas à droite :", platformes.rect.x + platformes.width, platformes.rect.y + platformes.height)
