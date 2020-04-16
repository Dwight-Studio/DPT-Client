import json
import random
import string
import threading
import time

import requests

from dpt.game import Game


class Communication(object):
    def __init__(self):
        self.i = 0
        self.log = Game.get_logger("WebCom")
        self.sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
        self.keepAliveThread = threading.Thread(target=self.keep_alive)
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

    def keep_alive(self):
        while self.keep:
            time.sleep(3)
            keep_link = requests.get("http://" + Game.SERVER_ADDRESS + "/keepAlive.php?session=" + self.sessionName)
            if not keep_link.json():
                self.i += 1
                if self.i == 3:
                    self.log.critical("keepAlive failed")
                    self.keep = False
                else:
                    continue

    def create_vote_event(self, mod1, mod2):
        self.log.info("Creating a new vote...")
        self.currentTime = int(round(time.time() * 1000))
        data = {"endDate": self.currentTime + (Game.VOTE_TIMEOUT * 1000) + 2000, "mod1": mod1, "mod2": mod2}
        requests.get("http://" + Game.SERVER_ADDRESS + "/registerVote.php?session=" + self.sessionName + "&data=" + json.dumps(data))
        self.log.info("Vote created")

    def vote_result(self):
        vote_one = 0
        vote_two = 0
        self.log.info("Requesting vote output...")
        request_vote = requests.get("http://" + Game.SERVER_ADDRESS + "/sessions.json").json()
        if request_vote is not None:
            for data in request_vote[self.sessionName].values():
                self.log.debug("Vote " + data)
                if data == "1":
                    vote_one += 1
                elif data == "2":
                    vote_two += 1
            if vote_one > vote_two:
                self.log.info("Majority of vote 1")
            elif vote_two > vote_one:
                self.log.info("Majority of vote 2")
            else:
                self.log.info("Vote equality")
        else:
            self.log.critical("Vote request failed")

    def close(self):
        request_close = requests.get("http://" + Game.SERVER_ADDRESS + "/close.php?session=" + self.sessionName)
        self.keep = False
        if not request_close.json():
            self.log.warning("Close session failed")
        self.log.info("Session closed")
