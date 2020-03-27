import pygame
import math

from dpt.game import Game


class PlayerSprite(pygame.sprite.Sprite):
    game = Game.get_instance()
    screen_width, screen_height = game.surface.get_size()
    char = game.ressources.get("dpt.images.characters.player.standing")
    walkRight = game.ressources.get_multiple("dpt.images.characters.player.R*")
    walkLeft = game.ressources.get_multiple("dpt.images.characters.player.L*")

    def __init__(self, color, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
        self.left = True
        self.right = False
        self.standing = False
        self.width = width
        self.height = height
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > self.vel:
            self.rect.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_LEFT]:
            self.rect.x = 0
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.rect.x + self.width + self.vel < PlayerSprite.screen_width:
            self.rect.x += self.vel
            self.left = False
            self.right = True
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.rect.x = PlayerSprite.screen_width - self.width
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
                self.rect.y -= math.floor((self.jumpCount ** 2) * 0.5) * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = self.CONSTJUMPCOUNT