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
        from dpt.engine.tileManager import TileManager
        from dpt.engine.loader import RessourceLoader
        from dpt.game import Game
        pygame.sprite.Sprite.__init__(self, TileManager.environment_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image)


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
        """Créer un sprite du type Entitée

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int

        :rtype: pygame.sprite.Sprite
        """
        from dpt.engine.tileManager import TileManager
        from dpt.engine.loader import RessourceLoader
        from dpt.game import Game
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group)
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
        self.mask = pygame.mask.from_surface(self.image)

    @abstractmethod
    def update(self, *args, **kwargs):
        """Actualise les sprites

        :param args: Arguments spécifique
        :param kwargs: Arguments spécifique
        """
