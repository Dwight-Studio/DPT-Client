import math
import random
import pygame

from dpt.engine.loader import RessourceLoader
from dpt.engine.webCommunications import WebCommunication
from dpt.game import Game
from threading import Thread
from dpt.engine.gui.ui.effects.Fast import Fast
from dpt.engine.gui.ui.effects.Ice import Ice
from dpt.engine.gui.ui.effects.inversion import Inversion
from dpt.engine.gui.ui.effects.jumpBoost import JumpBoost
from dpt.engine.gui.ui.effects.lowGravity import LowGravity
from dpt.engine.gui.ui.effects.monsterimmortal import Monsterimmortal
from dpt.engine.gui.ui.effects.Slow import Slow
from dpt.engine.gui.ui.effects.star import Star
from dpt.engine.gui.ui.effects.reverse import Reverse


class EffectsManagement:
    """Gestion des effets (les activer/désactiver, lancer des votes, les afficher, communiquer avec le PlayerSprite...)"""
    list_effects = ["Ice",
                    "Slow",
                    "Fast",
                    "monsterimmortal",
                    "star",
                    "jumpBoost",
                    "inversion",
                    "lowGravity",
                    "reverse"]

    list_current_effects = []

    dico_effects = {"Ice": "Perm",
                    "Slow": "Temp",
                    "Fast": "Temp",
                    "monsterimmortal": "Temp",
                    "star": "Temp",
                    "jumpBoost": "Temp",
                    "inversion": "Temp",
                    "lowGravity": "Perm",
                    "reverse": "Temp"}

    dico_current_effects = {"Ice": False,
                            "Slow": False,
                            "Fast": False,
                            "monsterimmortal": False,
                            "star": False,
                            "jumpBoost": False,
                            "inversion": False,
                            "lowGravity": False,
                            "reverse": True}

    temp_list = []
    perm_list = []
    mods = []

    image_fast = None
    image_ice = None
    image_inversion = None
    image_jumpBoost = None
    image_lowGravity = None
    image_monsterimmortal = None
    image_slow = None
    image_star = None
    image_reverse = None

    upsidedown = False

    @classmethod
    def create_effects_image(cls):
        """Crée les images des effets possibles"""
        cls.image_fast = Fast()
        cls.image_ice = Ice()
        cls.image_inversion = Inversion()
        cls.image_jumpBoost = JumpBoost()
        cls.image_lowGravity = LowGravity()
        cls.image_monsterimmortal = Monsterimmortal()
        cls.image_slow = Slow()
        cls.image_star = Star()
        cls.image_reverse = Reverse()

    @classmethod
    def update(cls):
        """Décide de lancer des nouveaux votes, supprime ou active les effets et gére le fonctionnement de certains effets"""
        cls.display_update()
        if cls.dico_current_effects["reverse"]:
            EffectsManagement.upsidedown = True
        else:
            EffectsManagement.upsidedown = False
        for event in Game.events:
            if event.type == Game.VOTE_RESULT_AVAILABLE_EVENT:
                for effects in cls.temp_list:
                    cls.dico_current_effects[effects] = False
                    cls.temp_list = []
                if not WebCommunication.last_result == "Both":
                    if cls.dico_effects[WebCommunication.last_result] == "Temp":
                        cls.temp_list.append(WebCommunication.last_result)
                    else:
                        cls.perm_list.append(WebCommunication.last_result)
                    cls.dico_current_effects[WebCommunication.last_result] = True
                    pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 30000, True)
                else:
                    for mods in cls.mods:
                        if cls.dico_effects[mods] == "Temp":
                            cls.temp_list.append(mods)
                        else:
                            cls.perm_list.append(mods)
                        cls.dico_current_effects[mods] = True
                cls.list_current_effects = []
                for mods in cls.perm_list:
                    cls.list_current_effects.append(mods)
                for mods in cls.temp_list:
                    cls.list_current_effects.append(mods)
                pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 30000, True)

                if cls.dico_current_effects["Slow"]:
                    def sound_effect():
                        for i in range(1, 81):
                            pygame.time.wait(2)
                            pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * ((100 - i) / 100))
                        sound = RessourceLoader.get("dpt.sounds.sfx.time_stop")
                        sound.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"])
                        sound.play()
                        pygame.time.wait(3000)
                        sound.fadeout(2000)
                        for i in range(20, 101):
                            pygame.time.wait(2)
                            pygame.mixer.music.set_volume(Game.settings["music_volume"] * Game.settings["general_volume"] * (i / 100))

                    Thread(target=sound_effect).start()

            elif event.type == Game.WAIT_BETWEEN_VOTE_EVENT:
                cls.vote()

    @classmethod
    def vote(cls):
        """Choisi les modificateurs et lance un vote"""
        mod1 = random.choice(cls.list_effects)
        while mod1 in cls.list_current_effects:
            mod1 = random.choice(cls.list_current_effects)
        mod2 = random.choice(cls.list_effects)
        while mod2 == mod1 or mod2 in cls.list_current_effects:
            mod2 = random.choice(cls.list_effects)
        cls.mods = [mod1, mod2]
        WebCommunication.create_vote_event(mod1, mod2)

    @classmethod
    def reset(cls):
        """Réinitialise tous les effets"""
        cls.dico_current_effects = {"Ice": False,
                                    "Slow": False,
                                    "Fast": False,
                                    "monsterimmortal": False,
                                    "star": False,
                                    "jumpBoost": False,
                                    "inversion": False,
                                    "lowGravity": False,
                                    "reverse": False}

        # Suppression des évènements en attente
        pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 0)
        pygame.time.set_timer(Game.VOTE_RESULT_AVAILABLE_EVENT, 0)

        EffectsManagement.upsidedown = False

        cls.temp_list = []
        cls.perm_list = []
        cls.list_current_effects = []
        cls.mods = []

    @classmethod
    def display_update(cls):
        """Affiche les effets actifs"""
        i = 0
        list_current_images_effects = []
        dico_images_effects = {"Ice": cls.image_ice,
                               "Slow": cls.image_slow,
                               "Fast": cls.image_fast,
                               "monsterimmortal": cls.image_monsterimmortal,
                               "star": cls.image_star,
                               "jumpBoost": cls.image_jumpBoost,
                               "inversion": cls.image_inversion,
                               "lowGravity": cls.image_lowGravity,
                               "reverse": cls.image_reverse}
        for images in cls.list_current_effects:
            list_current_images_effects.append(dico_images_effects[images])
        for images in list_current_images_effects:
            images.rect[0] = math.floor(i * 110 * Game.DISPLAY_RATIO + 10)
            images.update()
            i += 1
