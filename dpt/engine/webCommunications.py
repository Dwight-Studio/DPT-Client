import requests
from dpt.game import Game
import string
import random
import threading
import time

class Communication(object):
    def __init__(self, address):
        self.address = address
        self.i = 0
        self.game = Game.get_instance()
        self.log = self.game.get_logger("WebCom")
        self.sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
        self.keepAliveThread = threading.Thread(target=self.keepAlive)

    def create(self):
        request = requests.get("http://"+self.address+"/init.php?session="+self.sessionName)
        if request.json() == self.sessionName:
            self.log.info("Created session : "+self.sessionName)
            self.log.info("Starting keepAlive...")
            self.keepAliveThread.start()
        else:
            self.log.critical("Session creation failed")
            return False

    def keepAlive(self):
        keep = True
        while keep:
            time.sleep(3)
            keepLink = requests.get("http://"+self.address+"/keepAlive.php?session="+self.sessionName)
            if keepLink.json() != True:
                self.i += 1
                if self.i == 3:
                    self.log.critical("keepAlive failed")
                else:
                    continue