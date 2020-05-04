import pygame
import math

from dpt.engine.gui.menu.textSpriteButton import TextSpriteButton
from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Timer:
    timer_list = []
    texture_semi_colon = "dpt.images.gui.symbols.SYMB_SEMICOLON"
    textures = ["dpt.images.gui.symbols.SYMB_0",
                "dpt.images.gui.symbols.SYMB_1",
                "dpt.images.gui.symbols.SYMB_2",
                "dpt.images.gui.symbols.SYMB_3",
                "dpt.images.gui.symbols.SYMB_4",
                "dpt.images.gui.symbols.SYMB_5",
                "dpt.images.gui.symbols.SYMB_6",
                "dpt.images.gui.symbols.SYMB_7",
                "dpt.images.gui.symbols.SYMB_8",
                "dpt.images.gui.symbols.SYMB_9"]

    def __init__(self, time):
        """Crée un chronomètre

        :param time: Temps en secondes
        :type time: int

        :rtype: Timer
        """
        self.height_digits = math.floor(60 * Game.DISPLAY_RATIO)
        self.width_digits = math.floor(48 * Game.DISPLAY_RATIO)
        self.width_semicolon = math.floor(24 * Game.DISPLAY_RATIO)
        self.time = time + 1

        self.digits_images = [pygame.transform.smoothscale(RessourceLoader.get(i), (self.width_digits, self.height_digits)) for i in Timer.textures]
        self.semicolon_image = pygame.transform.smoothscale(RessourceLoader.get(Timer.texture_semi_colon), (self.width_semicolon, self.height_digits))

        self.rect = pygame.rect.Rect(0, math.floor(20 * Game.DISPLAY_RATIO), 4 * self.width_digits + self.width_semicolon, self.height_digits)
        self.rect.centerx = Game.surface.get_size()[0] // 2

        self.digit1 = TextSpriteButton(self.width_digits, self.height_digits, self.digits_images[0])
        self.digit2 = TextSpriteButton(self.width_digits, self.height_digits, self.digits_images[0])
        self.semicolon = TextSpriteButton(self.width_semicolon, self.height_digits, self.semicolon_image)
        self.digit3 = TextSpriteButton(self.width_digits, self.height_digits, self.digits_images[0])
        self.digit4 = TextSpriteButton(self.width_digits, self.height_digits, self.digits_images[0])

        self.digit1.rect.left = self.rect.left
        self.digit2.rect.left = self.digit1.rect.right
        self.semicolon.rect.centerx = Game.surface.get_size()[0] // 2
        self.digit4.rect.right = self.rect.right
        self.digit3.rect.right = self.digit4.rect.left

        for sprite in [self.digit1, self.digit2, self.semicolon, self.digit3, self.digit4]:
            sprite.rect.centery = self.rect.centery

        pygame.time.set_timer(Game.TIMER_EVENT, 1000)
        pygame.event.post(pygame.event.Event(Game.TIMER_EVENT))

        Timer.timer_list.append(self)
        Game.get_logger(Timer.__name__).info("Timer created")

    def update(self):
        """Actualise le timer"""
        for event in Game.events:
            if event.type == Game.TIMER_EVENT:
                self.time -= 1

                if self.time == -1:
                    pygame.time.set_timer(Game.TIMER_EVENT, 0)
                    pygame.event.post(pygame.event.Event(Game.TIMER_FINISHED_EVENT))
                    return

                self.digit1.image = self.digits_images[self.time // 600]
                self.digit2.image = self.digits_images[(self.time % 600) // 60]
                self.digit3.image = self.digits_images[(self.time % 60) // 10]
                self.digit4.image = self.digits_images[(self.time % 60) % 10]

        Game.add_debug_info("TIMER INFORMATIONS")
        Game.add_debug_info("Time: " + str(self.time))
        Game.add_debug_info("----------")

    def kill(self):
        """Supprime le timer"""
        Timer.timer_list.remove(self)
        self.digit1.kill()
        self.digit2.kill()
        self.semicolon.kill()
        self.digit3.kill()
        self.digit4.kill()

    @classmethod
    def main_loop(cls):
        """Actualise tous les timers"""
        for timer in Timer.timer_list:
            timer.update()
