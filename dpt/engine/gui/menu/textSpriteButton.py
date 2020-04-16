import pygame

from dpt.engine.gui.menu.button import Button


class TextSpriteButton(pygame.sprite.Sprite):

    def __init__(self, width, height, image):
        pygame.sprite.Sprite.__init__(self, Button.text_sprite_buttonsGroup)  # Sprite's constructor called
        self.image = image
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
