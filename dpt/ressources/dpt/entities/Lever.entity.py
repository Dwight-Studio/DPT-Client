import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Lever(pygame.sprite.Sprite):
    texture = "dpt.images.environment.lever.Lever_Left"
    width = height = Game.TILESIZE
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.interactible_blocks)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.x = x
        self.y = y
        self.clicked = False
        self.right = False
        self.left = True

    def update(self):
        mouseButtons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if mouseButtons[0] == 1 and not self.clicked:
            self.clicked = True
            from dpt.engine.tileManager import TileManager
            if mousePos[0] >= self.x + TileManager.camera.last_x and mousePos[0] <= self.x + self.width and mousePos[1] >= self.y and mousePos[1] <= self.y + self.height:
                from dpt.engine.gui.editor.tileEditor import TileEditor
                if not TileEditor.in_editor:
                    if self.left:
                        self.left = False
                        self.right = True
                        texture = "dpt.images.environment.lever.Lever_Right"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.scale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                    elif self.right:
                        self.right = False
                        self.left = True
                        texture = "dpt.images.environment.lever.Lever_Left"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.scale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                elif TileEditor.in_editor:
                    pass
        elif mouseButtons[0] != 1 and self.clicked:
            self.clicked = False
