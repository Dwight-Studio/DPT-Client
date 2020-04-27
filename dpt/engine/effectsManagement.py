from dpt.engine.webCommunications import Communication
from dpt.engine.tileManager import TileManager

import random


class effectsManagement(Communication):

    listEffects = ["Ice",
                   "Slow",
                   "Fast",
                   "monsterimmortal",
                   "star",
                   "jumpBoost",
                   "inversion",
                   "lowGravity"]

    dicoEffects = {"Ice": "Perm",
                   "Slow": "Temp",
                   "Fast": "Temp",
                   "monsterimmortal": "Temp",
                   "star": "Temp",
                   "jumpBoost": "Temp",
                   "inversion": "Temp",
                   "lowGravity": "Perm"}

    def __init__(self):
        super().__init__()
        self.result = None

    def update(self):
        self.vote()

    def vote(self):
        mod1 = random.choice(effectsManagement.listEffects)
        mod2 = random.choice(effectsManagement.listEffects)
        while mod2 == mod1:
            mod2 = random.choice(effectsManagement.listEffects)
        self.result = self.create_vote_event(mod1, mod2)
