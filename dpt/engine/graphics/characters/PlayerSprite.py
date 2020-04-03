import pygame
import math

from dpt.game import Game


class PlayerSprite(pygame.sprite.Sprite):
    game = Game.get_instance()
    screen_width, screen_height = game.surface.get_size()
    char = game.ressources.get("dpt.images.characters.player.standing")
    walkRight = game.ressources.get_multiple("dpt.images.characters.player.R*")
    walkLeft = game.ressources.get_multiple("dpt.images.characters.player.L*")

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.image = PlayerSprite.char
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 8
        self.left = True
        self.right = False
        self.standing = False
        self.width = width
        self.height = height
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 8
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.isFalling = True

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.vel
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
                self.onPlatform = False
        else:
            if not self.onPlatform:
                if self.jumpCount > 0:
                    self.isFalling = False
                    neg = 1
                else:
                    self.isFalling = True
                    neg = -1
                self.rect.y -= math.floor((self.jumpCount ** 2) * 0.5) * neg
                self.jumpCount -= 1
            elif self.onPlatform:
                self.jumpCount = self.CONSTJUMPCOUNT
                self.isJump = False

        self.animation()

    def animation(self):
        game = Game.get_instance()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                self.image = PlayerSprite.walkLeft[self.walkCount // 3]
                self.walkCount += 1
            elif self.right:
                self.image = PlayerSprite.walkRight[self.walkCount // 3]
                self.walkCount += 1
        else:
            if self.right:
                self.image = PlayerSprite.walkRight[0]
            else:
                self.image = PlayerSprite.walkLeft[0]
        pygame.draw.rect(game.surface, (255, 0, 0), self.rect, 2)
