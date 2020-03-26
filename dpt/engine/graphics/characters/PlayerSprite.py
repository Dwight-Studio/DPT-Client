from dpt.game import Game
import pygame
import math


class PlayerSprite(pygame.sprite.Sprite):
    game = Game.get_instance()
    char = game.ressources.get("dpt.images.characters.player.standing")
    walkRight = game.ressources.get_multiple("dpt.images.characters.player.R*")
    walkLeft = game.ressources.get_multiple("dpt.images.characters.player.L*")

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image, self.rect = PlayerSprite.walkLeft[0], -1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount
        self.left = True
        self.right = False
        self.walkCount = 0
        self.standing = True

    def update(self):
        keys = pygame.key.get_pressed()
        game = Game.get_instance()
        screen_width, screen_height = game.window.get_size()


"""
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_LEFT]:
            self.x = 0
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.x + self.width + self.vel < screen_width:
            self.x += self.vel
            self.left = False
            self.right = True
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.x = screen_width - self.width
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.standing = True
            self.walkCount = 0

        if not self.isJump:
            if keys[pygame.K_UP]:
                self.isJump = True
                self.left = False
                if self.right:
                    self.right = True
                else:
                    self.right = False
                self.walkCount = 0
        else:
            if self.jumpCount >= -self.CONSTJUMPCOUNT:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= math.floor((self.jumpCount ** 2) * 0.5) * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = self.CONSTJUMPCOUNT
"""
