from abc import ABC, abstractmethod
import pygame


class Block(ABC, pygame.sprite.Sprite):
    texture = ""
    textures = "" or None
    sounds = ""
    width = height = 0
    offset_x = 0
    offset_y = 0

    @abstractmethod
    def __init__(self, x, y):
        """Créer un sprite du type Block
        
        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int

        :rtype: pygame.sprite.Sprite
        """
        pass


class Entity(ABC, pygame.sprite.Sprite):
    texture = ""
    textures = "" or None
    sounds = ""
    width = height = 0
    offset_x = 0
    offset_y = 0
    customPlacement = False

    @abstractmethod
    def __init__(self, x, y):
        """Créer un sprite du type Block

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int

        :rtype: pygame.sprite.Sprite
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """Actualise les sprites

        :param args: Arguments spécifique
        :param kwargs: Arguments spécifique
        """
