import math
import pygame

from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Button(pygame.sprite.Sprite):
    buttonsGroup = pygame.sprite.Group()
    text_sprite_buttonsGroup = pygame.sprite.Group()
    text_buttonsList = []

    def __init__(self, x, y, width, height, normal_image, **kwargs):
        """Crée un bouton

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type x: int
        :param width: Largeur
        :type width: int
        :param height: Hauteur
        :type height: int
        :param normal_image: Image
        :type normal_image: pygame.Surface

        :keyword pushed_image: Image utilisé lorsque le bouton est pressé
        :keyword locked_image: Image utilisé lorque le bouton est verrouillé
        :keyword hover_image: Image utilisé lorsque le bouton est survolé
        :keyword font: Police d'écriture
        :keyword font_color: Couleur du texte
        :keyword text: Texte du bouton
        :keyword text_sprite: Image à afficher sur le bouton (Utilise l'objet 'TextSpriteButton')

        :rtype: Button
        """

        pygame.sprite.Sprite.__init__(self, Button.buttonsGroup)  # Sprite's constructor called
        self.normal_image = normal_image
        if "pushed_image" in kwargs:
            self.pushed_image = kwargs["pushed_image"]
            del kwargs["pushed_image"]
        else:
            self.pushed_image = self.normal_image
        if "locked_image" in kwargs:
            self.locked_image = kwargs["locked_image"]
            del kwargs["locked_image"]
        else:
            self.locked_image = self.normal_image
        if "hover_image" in kwargs:
            self.hover_image = kwargs["hover_image"] or self.normal_image
            del kwargs["hover_image"]
        else:
            self.hover_image = self.normal_image
        if "font" in kwargs:
            self.font = kwargs["font"]
            del kwargs["font"]
        else:
            self.font = pygame.font.SysFont("arial", math.floor(15 * Game.DISPLAY_RATIO))
        if "font_color" in kwargs:
            self.font_color = kwargs["font_color"]
            del kwargs["font_color"]
        else:
            self.font_color = (0, 0, 0)
        if "text" in kwargs:
            self.text = kwargs["text"]
            del kwargs["text"]
        else:
            self.text = None
        if "text_sprite" in kwargs:
            self.text_sprite = kwargs["text_sprite"]
            del kwargs["text_sprite"]
        else:
            self.text_sprite = None

        self.eventargs = kwargs
        self.image = self.normal_image
        self.width = width
        self.height = height
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pushed = False
        self.previous = 0
        self.locked = False
        Game.get_logger("Button").debug("Button created")

    def __bool__(self):
        return self.pushed

    def update(self):
        """Actualise le bouton"""
        if self.text_sprite is not None:
            self.text_sprite.rect.centerx = self.rect.centerx
            self.text_sprite.rect.centery = self.rect.centery

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
                    sound = RessourceLoader.get("dpt.sounds.sfx.switch6")
                    sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
                    sound.play()
                    self.pushed = True
                    self.previous = 5

        if self.pushed or self.previous > 0:
            self.image = self.pushed_image
            if self.text_sprite is not None:
                self.text_sprite.rect.centery = self.rect.centery + math.floor(self.rect.height * 0.1)
            if self.pushed:
                event = pygame.event.Event(Game.BUTTON_EVENT, **dict(button=self, **self.eventargs))
                pygame.event.post(event)
            else:
                self.previous -= 1
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
                Game.cursor_on_button = True
            else:
                self.image = self.normal_image

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

    def lock(self):
        """Verrouille le bouton"""
        self.locked = True

    def unlock(self):
        """Déverrouille """
        self.locked = False

    @classmethod
    def main_loop(cls):
        """Actualise tous les boutons"""
        Button.text_buttonsList = []
        Button.buttonsGroup.update()
        Button.text_sprite_buttonsGroup.update()
        Button.buttonsGroup.draw(Game.surface)
        Button.text_sprite_buttonsGroup.draw(Game.surface)
        for i in Button.text_buttonsList:
            Game.surface.blit(i[0], i[1])
