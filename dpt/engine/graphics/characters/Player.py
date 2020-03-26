import pygame

from dpt.game import Game

DIRECTORY = "engine/graphics/characters/player/"


class Player(object):
    game = Game.get_instance()
    char = game.ressources.get("dpt.images.characters.player.standing")
    walkRight = [game.ressources.get("dpt.images.characters.player.R1"), game.ressources.get("dpt.images.characters.player.R2"), game.ressources.get("dpt.images.characters.player.R3"), game.ressources.get("dpt.images.characters.player.R4"), game.ressources.get("dpt.images.characters.player.R5"), game.ressources.get("dpt.images.characters.player.R6"), game.ressources.get("dpt.images.characters.player.R7"), game.ressources.get("dpt.images.characters.player.R8"), game.ressources.get("dpt.images.characters.player.R9")]
    walkLeft = [game.ressources.get("dpt.images.characters.player.L1"), game.ressources.get("dpt.images.characters.player.L2"), game.ressources.get("dpt.images.characters.player.L3"), game.ressources.get("dpt.images.characters.player.L4"), game.ressources.get("dpt.images.characters.player.L5"), game.ressources.get("dpt.images.characters.player.L6"), game.ressources.get("dpt.images.characters.player.L7"), game.ressources.get("dpt.images.characters.player.L8"), game.ressources.get("dpt.images.characters.player.L9")]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 8
        self.staticJumpCount = self.jumpCount
        self.left = True
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(self.walkRight[0], (self.x, self.y))
            else:
                window.blit(self.walkLeft[0], (self.x, self.y))
