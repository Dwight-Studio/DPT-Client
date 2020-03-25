import pygame

DIRECTORY = "engine/graphics/characters/pictures/"
char = pygame.image.load(DIRECTORY + 'standing.png')
walkRight = [pygame.image.load(DIRECTORY + 'R1.png'), pygame.image.load(DIRECTORY + 'R2.png'), pygame.image.load(DIRECTORY + 'R3.png'), pygame.image.load(DIRECTORY + 'R4.png'), pygame.image.load(DIRECTORY + 'R5.png'), pygame.image.load(DIRECTORY + 'R6.png'), pygame.image.load(DIRECTORY + 'R7.png'), pygame.image.load(DIRECTORY + 'R8.png'), pygame.image.load(DIRECTORY + 'R9.png')]
walkLeft = [pygame.image.load(DIRECTORY + 'L1.png'), pygame.image.load(DIRECTORY + 'L2.png'), pygame.image.load(DIRECTORY + 'L3.png'), pygame.image.load(DIRECTORY + 'L4.png'), pygame.image.load(DIRECTORY + 'L5.png'), pygame.image.load(DIRECTORY + 'L6.png'), pygame.image.load(DIRECTORY + 'L7.png'), pygame.image.load(DIRECTORY + 'L8.png'), pygame.image.load(DIRECTORY + 'L9.png')]


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
        self.walkCount = 0
        self.standing = True

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
