import pygame
from dpt.game import Game


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, **kwargs):
        pygame.sprite.Sprite.__init__(self)  # Sprite's constructor called
        self.normal_image = kwargs["normal_image"]
        del kwargs["normal_image"]
        self.pushed_image = kwargs["pushed_image"] or self.normal_image
        del kwargs["pushed_image"]
        self.locked_image = kwargs["locked_image"] or self.normal_image
        del kwargs["locked_image"]
        self.hover_image = kwargs["hover_image"] or self.normal_image
        del kwargs["hover_image"]
        self.eventargs = kwargs
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.pushed = False
        self.locked = False
        self.previous_state = False
        Game.get_logger("Button").debug("Button created")
        Game.buttonsGroup.add(self)

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
                event = pygame.event.Event(Game.BUTTONEVENT, **dict(button=self, **self.eventargs))
                pygame.event.post(event)
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
            else:
                self.image = self.normal_image

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
