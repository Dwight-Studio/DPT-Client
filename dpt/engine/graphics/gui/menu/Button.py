import pygame

from dpt.game import Game


class Button(pygame.sprite.Sprite):
    buttonsGroup = pygame.sprite.Group()
    text_buttonsList = []

    def __init__(self, x, y, width, height, image, **kwargs):
        pygame.sprite.Sprite.__init__(self, Button.buttonsGroup)  # Sprite's constructor called
        self.normal_image = image
        try:
            self.pushed_image = kwargs["pushed_image"]
            del kwargs["pushed_image"]
        except KeyError:
            self.pushed_image = self.normal_image
        try:
            self.locked_image = kwargs["locked_image"]
            del kwargs["locked_image"]
        except KeyError:
            self.locked_image = self.normal_image
        try:
            self.hover_image = kwargs["hover_image"] or self.normal_image
            del kwargs["hover_image"]
        except KeyError:
            self.hover_image = self.normal_image
        try:
            self.font = kwargs["font"]
            del kwargs["font"]
        except KeyError:
            self.font = pygame.font.SysFont("arial", 15)
        try:
            self.font_color = kwargs["font_color"]
            del kwargs["font_color"]
        except KeyError:
            self.font_color = (0, 0, 0)
        try:
            self.text = kwargs["text"]
            del kwargs["text"]
        except KeyError:
            self.text = None
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

    def __bool__(self):
        return self.pushed

    def update(self):
        if self.text is not None:
            text = self.font.render(self.text, True, self.font_color)
            rect = text.get_rect()
            rect.centerx = self.rect.centerx
            rect.centery = self.rect.centery
            Button.text_buttonsList.append((text, rect))

        self.pushed = False
        if self.locked:
            self.image = self.locked_image
            return

        for event in Game.events:
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
