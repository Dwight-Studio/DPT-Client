import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        from dpt.engine.gui.menu.progressbar import ProgressBar
        pygame.sprite.Sprite.__init__(self, ProgressBar.bar_group)  # Sprite's constructor called
        self.image = image
        self.normal_image = image
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(self.normal_image, (self.width, self.height))
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.progress = width

    def update(self):
        self.rect.width = self.progress
        self.image = self.normal_image.subsurface(pygame.Rect(0, 0, self.rect.width, self.rect.height)).copy()
