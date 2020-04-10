import pygame
from dpt.game import Game


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image1, image2, image3, eventargs):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.eventargs = eventargs
        self.image = image1
        self.normal_image = image1
        self.pushed_image = image2
        self.locked_image = image3
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.pushed = False
        self.locked = False
        self.previous_state = False

    def __bool__(self):
        return self.pushed

    def update(self):
        self.pushed = False
        if self.locked:
            self.image = self.locked_image
            return

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.pushed = True

        if self.pushed:
            self.image = self.pushed_image
            if not self.previous_state:
                event = pygame.event.Event(type=Game.BUTTONEVENT, **dict(button=self, **self.eventargs))
                pygame.event.post(event)
        else:
            self.image = self.normal_image

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
