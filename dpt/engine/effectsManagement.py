import math
import random
import pygame

from dpt.engine.webCommunications import WebCommunication
from dpt.game import Game

from dpt.engine.gui.ui.effects.Fast import Fast
from dpt.engine.gui.ui.effects.Ice import Ice
from dpt.engine.gui.ui.effects.inversion import Inversion
from dpt.engine.gui.ui.effects.jumpBoost import JumpBoost
from dpt.engine.gui.ui.effects.lowGravity import LowGravity
from dpt.engine.gui.ui.effects.monsterimmortal import Monsterimmortal
from dpt.engine.gui.ui.effects.Slow import Slow
from dpt.engine.gui.ui.effects.star import Star


class EffectsManagement:
    list_effects = ["Ice",
                    "Slow",
                    "Fast",
                    "monsterimmortal",
                    "star",
                    "jumpBoost",
                    "inversion",
                    "lowGravity"]

    list_current_effects = []

    dico_effects = {"Ice": "Perm",
                    "Slow": "Temp",
                    "Fast": "Temp",
                    "monsterimmortal": "Temp",
                    "star": "Temp",
                    "jumpBoost": "Temp",
                    "inversion": "Temp",
                    "lowGravity": "Perm"}

    dico_current_effects = {"Ice": False,
                            "Slow": False,
                            "Fast": False,
                            "monsterimmortal": False,
                            "star": False,
                            "jumpBoost": False,
                            "inversion": False,
                            "lowGravity": False}

    temp_list = []
    perm_list = []
    mods = []
    image_fast = Fast()
    image_ice = Ice()
    image_inversion = Inversion()
    image_jumpBoost = JumpBoost()
    image_lowGravity = LowGravity()
    image_monsterimmortal = Monsterimmortal()
    image_slow = Slow()
    image_star = Star()

    @classmethod
    def update(cls):
        cls.display_update()
        for event in Game.events:
            if event.type == Game.VOTE_RESULT_AVAILABLE_EVENT:
                cls.list_current_effects = []
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
                for mods in cls.perm_list:
                    cls.list_current_effects.append(mods)
                for mods in cls.temp_list:
                    cls.list_current_effects.append(mods)
                pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 30000, True)
            elif event.type == Game.WAIT_BETWEEN_VOTE_EVENT:
                cls.vote()

    @classmethod
    def vote(cls):
        mod1 = "Slow"
        mod2 = random.choice(cls.list_effects)
        while mod2 == mod1:
            mod2 = random.choice(cls.list_effects)
        cls.mods = [mod1, mod2]
        WebCommunication.create_vote_event(mod1, mod2)

    @classmethod
    def reset(cls):
        cls.dico_current_effects = {"Ice": False,
                                    "Slow": False,
                                    "Fast": False,
                                    "monsterimmortal": False,
                                    "star": False,
                                    "jumpBoost": False,
                                    "inversion": False,
                                    "lowGravity": False}
        cls.temp_list = []
        cls.perm_list = []

    @classmethod
    def display_update(cls):
        i = 0
        list_current_images_effects = []
        dico_images_effects = {"Ice": cls.image_ice,
                               "Slow": cls.image_slow,
                               "Fast": cls.image_fast,
                               "monsterimmortal": cls.image_monsterimmortal,
                               "star": cls.image_star,
                               "jumpBoost": cls.image_jumpBoost,
                               "inversion": cls.image_inversion,
                               "lowGravity": cls.image_lowGravity}
        for images in cls.list_current_effects:
            list_current_images_effects.append(dico_images_effects[images])
        for images in list_current_images_effects:
            images.rect[0] = math.floor(i * 110 * Game.DISPLAY_RATIO)
            images.update()
            i += 1
