import pygame
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class Lever(pygame.sprite.Sprite):
    texture = "dpt.images.environment.lever.Lever_Left"
    sounds = "dpt.sounds.sfx.sfx_stone"
    width = height = Game.TILESIZE
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 2)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.interactible_blocks_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.x = x
        self.y = y
        self.clicked = False
        self.right = False
        self.left = True
        self.set = False
        if not TileManager.loadlevel:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def update(self):
        mouseButtons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        from dpt.engine.tileManager import TileManager
        if self.x + TileManager.camera.last_x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.height:
            if mouseButtons[0] == 1 and not self.clicked:
                self.clicked = True
                from dpt.engine.gui.editor.tileEditor import TileEditor
                if not TileEditor.in_editor:
                    if self.left:
                        self.left = False
                        self.right = True
                        texture = "dpt.images.environment.lever.Lever_Right"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                    elif self.right:
                        self.right = False
                        self.left = True
                        texture = "dpt.images.environment.lever.Lever_Left"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                elif TileEditor.in_editor:
                    pass
            elif mouseButtons[0] != 1 and self.clicked:
                self.clicked = False
        if not self.set:
            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y + 30), (mousePos[0], mousePos[1]))
