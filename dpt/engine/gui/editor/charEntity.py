import pygame

from dpt.game import Game


class CharEntity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Game.player_group)  # Sprite's constructor called
        self.image = pygame.Surface((Game.TILESIZE, Game.TILESIZE))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = Game.WINDOW_WIDTH / 2
        self.rect.y = Game.WINDOW_HEIGHT / 2
        self.xvel = 0
        self.yvel = 0
        self.width = Game.TILESIZE
        self.height = Game.TILESIZE

    def update(self):
        keys = pygame.key.get_pressed()
        keysmods = pygame.key.get_mods()

        left = pygame.K_LEFT
        right = pygame.K_RIGHT
        left_letter = pygame.K_q
        right_letter = pygame.K_d

        if keysmods == 4097 or keysmods == 4098:
            pass
        else:
            if keys[left] or keys[left_letter]:
                if self.xvel > 0:
                    self.xvel = 0
                if self.xvel > -16:
                    self.xvel -= 16
                if self.rect.x < Game.WINDOW_WIDTH / 2:
                    self.xvel = 0
            elif keys[right] or keys[right_letter]:
                if self.xvel < 0:
                    self.xvel = 0
                if self.xvel < 16:
                    self.xvel += 16
            else:
                self.xvel = 0
            self.rect.left += self.xvel
