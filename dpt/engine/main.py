import pygame
import math
from dpt.engine.graphics.characters.Player import Player

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
pygame.display.set_caption("Don't play together")
clock = pygame.time.Clock()
screenWidth, screenHeight = window.get_size()
bg = pygame.image.load("graphics/backgrounds/backgrounds/background.png")


def redraw_game_window():
    window.blit(bg, (0, 0))
    player.draw(window)
    pygame.display.update()


# Mainloop
player = Player(300, screenHeight - 100, 64, 64)
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_LEFT]:
        player.x = 0
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_RIGHT] and player.x + player.width + player.vel < screenWidth:
        player.x += player.vel
        player.left = False
        player.right = True
        player.standing = False
    elif keys[pygame.K_RIGHT]:
        player.x = screenWidth - player.width
        player.left = False
        player.right = True
        player.standing = False
    else:
        player.standing = True
        player.walkCount = 0

    if not player.isJump:
        if keys[pygame.K_UP]:
            player.isJump = True
            player.left = False
            player.right = False
            player.walkCount = 0
    else:
        if player.jumpCount >= -player.staticJumpCount:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= math.floor((player.jumpCount ** 2) * 0.5) * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = player.staticJumpCount

    redraw_game_window()

pygame.quit()