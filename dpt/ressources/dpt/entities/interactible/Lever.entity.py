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
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group, TileManager.interactible_blocks_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.x = x
        self.y = y
        self.clicked = False
        self.clicked2 = False
        self.right = False
        self.left = True
        self.set = False
        self.attributing = False
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        if self.x + self.offset_x + TileManager.camera.last_x <= mousePos[0] <= self.x + self.offset_x + self.width and self.y + self.offset_y <= mousePos[1] <= self.y + self.offset_y + self.height:
            if mouse_buttons[0] == 1 and not self.clicked:
                self.clicked = True
                if not TileEditor.enabled_editor:
                    if self.left:
                        self.left = False
                        self.right = True
                        texture = "dpt.images.environment.lever.Lever_Right"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                        for keys, data in TileEditor.created_level.items():
                            if keys == str(self.x) + ", " + str(self.y):
                                for interact in TileManager.interactible_blocks_group:
                                    pos = tuple(map(int, data["assignement"].split(", ")))
                                    try:
                                        if interact.x == pos[0] and interact.y == pos[1]:
                                            interact.deactivate()
                                    except AttributeError:
                                        continue
                    elif self.right:
                        self.right = False
                        self.left = True
                        texture = "dpt.images.environment.lever.Lever_Left"
                        self.image = RessourceLoader.get(texture)
                        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x + self.offset_x
                        self.rect.y = self.y + self.offset_y
                        for keys, data in TileEditor.created_level.items():
                            if keys == str(self.x) + ", " + str(self.y):
                                for interact in TileManager.interactible_blocks_group:
                                    pos = tuple(map(int, data["assignement"].split(", ")))
                                    if interact.x == pos[0] and interact.y == pos[1]:
                                        interact.activate()
                elif TileEditor.enabled_editor:
                    self.attributing = True
            elif mouse_buttons[0] != 1 and self.clicked:
                self.clicked = False
        if TileEditor.enabled_editor and self.attributing:
            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y + 30), (mousePos[0], mousePos[1]))
            if mouse_buttons[0] == 1 and not self.clicked2:
                self.clicked2 = True
                for sprites in TileManager.interactible_blocks_group:
                    try:
                        if isinstance(sprites, RessourceLoader.get("dpt.entities.spike")):
                            if sprites.x + TileManager.camera.last_x <= mousePos[0] <= sprites.x + sprites.width and sprites.y + sprites.offset_y <= mousePos[1] <= sprites.y:
                                self.attributing = False
                                TileEditor.created_level[str(self.x) + ", " + str(self.y)]["assignement"] = str(sprites.x) + ", " + str(sprites.y)
                    except AttributeError:
                        continue
            elif mouse_buttons[0] != 1 and self.clicked2:
                self.clicked2 = False
