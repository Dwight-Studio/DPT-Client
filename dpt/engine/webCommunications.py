import requests
from dpt.game import Game
import string
import random
import threading
import time
import json

class Communication(object):
    def __init__(self):
        self.i = 0
        self.game = Game.get_instance()
        self.log = self.game.get_logger("WebCom")
        self.sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
        self.keepAliveThread = threading.Thread(target=self.keepAlive)
        self.keep = False
        self.currentTime = int(round(time.time() * 1000))

    def create(self):
        request = requests.get("http://" + Game.SERVER_ADDRESS + "/init.php?session=" + self.sessionName)
        if request.json() == self.sessionName:
            self.log.info("Created session : " + self.sessionName)
            self.log.info("http://" + Game.SERVER_ADDRESS + "/?session=" + self.sessionName)
            self.log.info("Starting keepAlive...")
            self.keep = True
            self.keepAliveThread.start()
        else:
            self.log.critical("Session creation failed")
            return False

    def keepAlive(self):
        while self.keep:
            time.sleep(3)
            keepLink = requests.get("http://" + Game.SERVER_ADDRESS + "/keepAlive.php?session=" + self.sessionName)
            if not keepLink.json():
                self.i += 1
                if self.i == 3:
                    self.log.critical("keepAlive failed")
                    self.keep = False
                else:
                    continue

    def createVoteEvent(self, mod1, mod2):
        self.currentTime = int(round(time.time() * 1000))
        data = {"endDate": self.currentTime+(Game.VOTE_TIMEOUT*1000)+2000,
                "mod1": mod1,
                "mod2": mod2}
        requests.get("http://" + Game.SERVER_ADDRESS + "/registerVote.php?session=" + self.sessionName + "&data=" + json.dumps(data))

    def close(self):
        requestClose = requests.get("http://" + Game.SERVER_ADDRESS + "/close.php?session=" + self.sessionName)
        self.keep = False
        if not requestClose.json():
            self.log.warning("Close session failed")
        self.log.info("Session closed")