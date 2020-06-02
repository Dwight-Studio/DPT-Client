#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pygame
import math

from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class ButtonYellow(pygame.sprite.Sprite):
    texture = "dpt.images.environment.buttons.Button_Yellow_Up"
    textures = "dpt.images.environment.buttons.Button_Yellow_*"
    sounds = ["dpt.sounds.sfx.sfx_stone", "dpt.sounds.sfx.metal_button_press"]
    width = Game.TILESIZE
    height = Game.TILESIZE // 6
    offset_x = -(Game.TILESIZE // 2)
    offset_y = -(Game.TILESIZE // 5)
    customPlacement = True

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
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
        self.down = False
        self.up = True
        self.set = False
        if TileManager.is_loading_level:
            self.attributing = False
            TileEditor.attributing = False
        else:
            self.attributing = True
            TileEditor.attributing = True
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds[0])
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor
        if round(self.x / Game.DISPLAY_RATIO, 4) + self.offset_x <= mousePos[0] - TileManager.camera.last_x <= round(self.x / Game.DISPLAY_RATIO, 4) + self.offset_x + self.width and round(self.y / Game.DISPLAY_RATIO, 4) + self.offset_y <= mousePos[1] <= round(self.y * Game.DISPLAY_RATIO, 4) + self.offset_y + self.height:
            if mouse_buttons[0] == 1 and not self.clicked and TileEditor.is_editing:
                self.clicked = True
                self.attributing = True
                TileEditor.attributing = True
            elif mouse_buttons[0] != 1 and self.clicked and TileEditor.is_editing:
                self.clicked = False
        if TileEditor.is_editing and self.attributing:
            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y), (mousePos[0], mousePos[1]), 1)
            if mouse_buttons[0] == 1 and not self.clicked:
                self.clicked = True
                for sprites in TileManager.interactible_blocks_group:
                    if hasattr(sprites, "customPlacement"):
                        if hasattr(sprites, "x") and hasattr(sprites, "y"):
                            if sprites.x + sprites.offset_x <= mousePos[0] - TileManager.camera.last_x <= sprites.x + sprites.offset_x + sprites.width and sprites.y + sprites.offset_y <= mousePos[1] <= sprites.y + sprites.offset_y + sprites.height:
                                if "assignement" not in TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]:
                                    TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"] = []
                                TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"].append(str(sprites.x / Game.DISPLAY_RATIO) + ", " + str(sprites.y / Game.DISPLAY_RATIO))
                                sound = RessourceLoader.get_multiple(self.sounds[1])[0]
                                sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                                sound.play()
                        else:
                            if sprites.rect.x <= mousePos[0] <= sprites.rect.x + sprites.width and sprites.rect.y <= mousePos[1] <= sprites.rect.y + sprites.height:
                                if "assignement" not in TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]:
                                    TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"] = []
                                TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"].append(str(sprites.rect.x - sprites.offset_x) + ", " + str(sprites.rect.y - sprites.offset_y))
                                sound = RessourceLoader.get_multiple(self.sounds[1])[0]
                                sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                                sound.play()
                    else:
                        if sprites.rect.x <= mousePos[0] - TileManager.camera.last_x <= sprites.rect.x + sprites.width and sprites.rect.y <= mousePos[1] <= sprites.rect.y + sprites.height:
                            if "assignement" not in TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]:
                                TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"] = []
                            TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]["assignement"].append(str((sprites.rect.x - sprites.offset_x) // Game.TILESIZE) + ", " + str((sprites.rect.y - sprites.offset_y) // Game.TILESIZE))
                            sound = RessourceLoader.get_multiple(self.sounds[1])[0]
                            sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                            sound.play()
            elif mouse_buttons[2] == 1:
                self.attributing = False
                TileEditor.attributing = False
            elif mouse_buttons[0] != 1 and self.clicked:
                self.clicked = False

        if TileEditor.is_editing:
            if "assignement" in TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]:
                for sprite in TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO,4))]["assignement"]:
                    try:
                        if sprite == str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4)):
                            continue
                        if "customPlace" in TileEditor.created_level["tiles"][sprite]:
                            x = round(float(sprite.split(", ")[0]), 4) + Game.TILESIZE // 2
                            y = round(float(sprite.split(", ")[1]), 4)

                            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y), (x + TileManager.camera.last_x, y))
                        else:
                            x = (int(sprite.split(", ")[0]) * Game.TILESIZE) + (Game.TILESIZE // 2)
                            y = (int(sprite.split(", ")[1]) * Game.TILESIZE) + (Game.TILESIZE // 2)

                            pygame.draw.line(Game.surface, (0, 0, 0), (self.x + TileManager.camera.last_x, self.y), (x + TileManager.camera.last_x, y))
                    except KeyError:
                        raise
        else:
            if pygame.sprite.collide_mask(self, Game.player_sprite):
                self.colliding = True
            else:
                self.colliding = False
            for enemy in TileManager.enemy_group:
                if pygame.sprite.collide_mask(self, enemy):
                    self.colliding = True
            if not self.clicked and self.colliding:
                self.clicked = True
                if self.up:
                    self.up = False
                    self.down = True
                    texture = "dpt.images.environment.buttons.Button_Yellow_Down"
                    self.image = RessourceLoader.get(texture)
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height // 2))
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x + self.offset_x
                    self.rect.y = self.y + self.offset_y // 2
                    data = TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]
                    if "assignement" in data:
                        for interact in TileManager.interactible_blocks_group:
                            positions = [tuple(map(float, i.split(", "))) for i in data["assignement"]]
                            for pos in positions:
                                if hasattr(interact, "x") and hasattr(interact, "y"):
                                    if interact.x == pos[0] and interact.y == pos[1]:
                                        if hasattr(interact, "activate"):
                                            interact.activate()
                                if interact.rect.x == pos[0] and interact.rect.y == pos[1]:
                                    if hasattr(interact, "activate"):
                                        interact.activate()
                                if interact.rect.x // Game.TILESIZE == pos[
                                    0] and interact.rect.y // Game.TILESIZE == pos[1]:
                                    if hasattr(interact, "activate"):
                                        interact.activate()
                    sound = RessourceLoader.get_multiple(self.sounds[1])[0]
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()
            else:
                if self.down and self.clicked and not self.colliding:
                    self.clicked = False
                    self.down = False
                    self.up = True
                    texture = "dpt.images.environment.buttons.Button_Yellow_Up"
                    self.image = RessourceLoader.get(texture)
                    self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x + self.offset_x
                    self.rect.y = self.y + self.offset_y
                    data = TileEditor.created_level["tiles"][str(round(self.x / Game.DISPLAY_RATIO, 4)) + ", " + str(round(self.y / Game.DISPLAY_RATIO, 4))]
                    if "assignement" in data:
                        for interact in TileManager.interactible_blocks_group:
                            positions = [tuple(map(float, i.split(", "))) for i in data["assignement"]]
                            for pos in positions:
                                if hasattr(interact, "x") and hasattr(interact, "y"):
                                    if interact.x == pos[0] and interact.y == pos[1]:
                                        if hasattr(interact, "deactivate"):
                                            interact.deactivate()
                                if interact.rect.x == pos[0] and interact.rect.y == pos[1]:
                                    if hasattr(interact, "deactivate"):
                                        interact.deactivate()
                                if interact.rect.x // Game.TILESIZE == pos[
                                    0] and interact.rect.y // Game.TILESIZE == \
                                        pos[1]:
                                    if hasattr(interact, "deactivate"):
                                        interact.deactivate()
                    sound = RessourceLoader.get_multiple(self.sounds[1])[1]
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()
