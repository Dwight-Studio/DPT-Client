import pygame
import math

from dpt.engine.gui.menu.simpleSprite import SimpleSprite
from dpt.game import Game
from dpt.engine.loader import RessourceLoader


class Timer:
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

    digit1 = None
    digit2 = None
    semicolon = None
    digit3 = None
    digit4 = None

    digits_images = None
    semicolon_image = None

    height_digits = math.floor(60 * Game.DISPLAY_RATIO)
    width_digits = math.floor(48 * Game.DISPLAY_RATIO)
    width_semicolon = math.floor(24 * Game.DISPLAY_RATIO)

    time = 0

    @classmethod
    def start(cls, time):
        """Crée un chronomètre

        :param time: Temps en secondes
        :type time: int

        :rtype: Timer
        """
        cls.height_digits = math.floor(60 * Game.DISPLAY_RATIO)
        cls.width_digits = math.floor(48 * Game.DISPLAY_RATIO)
        cls.width_semicolon = math.floor(24 * Game.DISPLAY_RATIO)
        cls.time = time + 1

        cls.digits_images = [pygame.transform.smoothscale(RessourceLoader.get(i), (cls.width_digits, cls.height_digits)) for i in Timer.textures]
        cls.semicolon_image = pygame.transform.smoothscale(RessourceLoader.get(Timer.texture_semi_colon), (cls.width_semicolon, cls.height_digits))

        cls.rect = pygame.rect.Rect(0, math.floor(20 * Game.DISPLAY_RATIO), 4 * cls.width_digits + cls.width_semicolon, cls.height_digits)
        cls.rect.centerx = Game.WINDOW_WIDTH // 2

        cls.digit1 = SimpleSprite(cls.width_digits, cls.height_digits, cls.digits_images[0])
        cls.digit2 = SimpleSprite(cls.width_digits, cls.height_digits, cls.digits_images[0])
        cls.semicolon = SimpleSprite(cls.width_semicolon, cls.height_digits, cls.semicolon_image)
        cls.digit3 = SimpleSprite(cls.width_digits, cls.height_digits, cls.digits_images[0])
        cls.digit4 = SimpleSprite(cls.width_digits, cls.height_digits, cls.digits_images[0])

        cls.digit1.rect.left = cls.rect.left
        cls.digit2.rect.left = cls.digit1.rect.right
        cls.semicolon.rect.centerx = Game.WINDOW_WIDTH // 2
        cls.digit4.rect.right = cls.rect.right
        cls.digit3.rect.right = cls.digit4.rect.left

        for sprite in [cls.digit1, cls.digit2, cls.semicolon, cls.digit3, cls.digit4]:
            sprite.rect.centery = cls.rect.centery

        pygame.time.set_timer(Game.TIMER_EVENT, 1000)
        pygame.event.post(pygame.event.Event(Game.TIMER_EVENT))

        Game.get_logger(Timer.__name__).info("Timer created")

    @classmethod
    def update(cls):
        """Actualise le timer"""
        for event in Game.events:
            if event.type == Game.TIMER_EVENT:
                cls.time -= 1

                if cls.time == -1:
                    pygame.time.set_timer(Game.TIMER_EVENT, 0)
                    pygame.event.post(pygame.event.Event(Game.TIMER_FINISHED_EVENT))
                    return

                cls.digit1.image = cls.digits_images[cls.time // 600]
                cls.digit2.image = cls.digits_images[(cls.time % 600) // 60]
                cls.digit3.image = cls.digits_images[(cls.time % 60) // 10]
                cls.digit4.image = cls.digits_images[(cls.time % 60) % 10]

        Game.add_debug_info("TIMER INFORMATIONS")
        Game.add_debug_info("Time: " + str(cls.time))
        Game.add_debug_info("----------")

    @classmethod
    def kill(cls):
        """Supprime le timer"""
        for sprite in [cls.digit1, cls.digit2, cls.semicolon, cls.digit3, cls.digit4]:
            if sprite is not None:
                sprite.kill()
                sprite = None
        pygame.time.set_timer(Game.TIMER_EVENT, 0)
        pygame.time.set_timer(Game.TIMER_FINISHED_EVENT, 0)

    @classmethod
    def main_loop(cls):
        """Actualise le timer"""
        cls.update()
