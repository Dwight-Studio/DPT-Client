from dpt.game import Game


class Player(object):
    game = Game.get_instance()
    char = game.ressources.get("dpt.images.characters.player.standing")
    walkRight = game.ressources.get_multiple("dpt.images.characters.player.R*")
    walkLeft = game.ressources.get_multiple("dpt.images.characters.player.L*")

    def __init__(self, x, y, width, height):
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

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(self.walkRight[0], (self.x, self.y))
            else:
                window.blit(self.walkLeft[0], (self.x, self.y))
