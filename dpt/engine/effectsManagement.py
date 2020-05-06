import random
import pygame

from dpt.engine.webCommunications import WebCommunication
from dpt.game import Game


class EffectsManagement:
    list_effects = ["Ice",
                    "Slow",
                    "Fast",
                    "monsterimmortal",
                    "star",
                    "jumpBoost",
                    "inversion",
                    "lowGravity"]

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
    mods = []

    @classmethod
    def update(cls):
        for event in Game.events:
            if event.type == Game.VOTE_RESULT_AVAILABLE_EVENT:
                for effects in cls.temp_list:
                    cls.dico_current_effects[effects] = False
                    cls.temp_list.remove(effects)
                if not WebCommunication.last_result == "Both":
                    if cls.dico_effects[WebCommunication.last_result] == "Temp":
                        cls.temp_list.append(WebCommunication.last_result)
                    cls.dico_current_effects[WebCommunication.last_result] = True
                    pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 30000, True)
                else:
                    for mods in cls.mods:
                        if cls.dico_effects[mods] == "Temp":
                            cls.temp_list.append(mods)
                        cls.dico_current_effects[mods] = True
                        pygame.time.set_timer(Game.WAIT_BETWEEN_VOTE_EVENT, 30000, True)
            elif event.type == Game.WAIT_BETWEEN_VOTE_EVENT:
                cls.vote()

    @classmethod
    def vote(cls):
        mod1 = random.choice(cls.list_effects)
        mod2 = random.choice(cls.list_effects)
        cls.mods = [mod1, mod2]
        while mod2 == mod1:
            mod2 = random.choice(cls.list_effects)
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
