import pygame
import math

pygame.init()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
pygame.display.set_caption("Don't play together")
clock = pygame.time.Clock()


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 8
        self.staticJumpCount = self.jumpCount
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True

    def draw(self, window):
        if self.walkcount + 1 >= """IL FAUT METTRE LE NOMBRE D'IMAGE DE L'ANIMATION""":
            self.walkcount = 0
        if not self.standing:
            if self.left:
                window.blit("""IL FAUT LES FICHIERS DE L'ANIMATION QUI VA VERS LA GAUCHE""")
                self.walkcount += 1
            elif self.right:
                window.blit("""IL FAUT LES FICHIERS DE L'ANIMATION QUI VA VERS LA DROITE""")
                self.walkcount += 1
        else:
            if self.right:
                window.blit("""IL FAUT LA PREMIÈRE IMAGE DE L'ANIMATION QUI VA VERS LA DROITE""")
            else:
                window.blit("""IL FAUT LA PREMIÈRE IMAGE DE L'ANIMATION QUI VA VERS LA GAUCHE""")


def redraw_game_window():
    window.blit("""IL FAUT LE FICHIER DU BACKGROUND""")
    player.draw(window)
    pygame.display.update()

# Mainloop
player = Player()
