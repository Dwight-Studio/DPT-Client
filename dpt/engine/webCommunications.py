import json
import random
import string
import threading
import time

import requests

from dpt.game import Game


class Communication(object):
    """Gestionnaire des communication webs"""
    def __init__(self):
        """Initialize la communication avec le serveur

        :rtype: Communication
        """
        self.i = 0
        self.log = Game.get_logger("WebCom")
        self.sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
        self.keepAliveThread = threading.Thread(target=self.keep_alive)
        self.keep = False
        self.currentTime = int(round(time.time() * 1000))
        self.waitThread = threading.Thread(target=self.start_wait)
        self.time_to_wait = 0

    def create(self):
        """Crée la session sur le serveur """
        try:
            request = requests.get("http://" + Game.settings["server_address"] + "/init.php?session=" + self.sessionName)
            if request.json() == self.sessionName:
                self.log.info("Created session : " + self.sessionName)
                self.log.info("http://" + Game.settings["server_address"] + "/?session=" + self.sessionName)
                self.log.info("Starting keepAlive...")
                self.keep = True
                self.keepAliveThread.start()
                return True
            else:
                self.log.critical("Session creation failed")
                return False
        except:
            self.log.warning("Hostname not found. Is the server running ? Check the server address !")

    def keep_alive(self):
        """Envoie de paquets toutes les 3 secondes pour garder la session active"""
        while self.keep:
            time.sleep(3)
            keep_link = requests.get("http://" + Game.settings["server_address"] + "/keepAlive.php?session=" + self.sessionName)
            if not keep_link.json():
                self.i += 1
                if self.i == 3:
                    self.log.critical("keepAlive failed")
                    self.keep = False
                else:
                    continue

    def create_vote_event(self, mod1, mod2):
        """Crée un évènement de vote

        :param mod1: Modificateur 1
        :type mod1: str
        :param mod2: Modificateur 2
        :type mod2: str
        :rtype: bool
        :return: Retourne True si le vote est correctement créé sinon False
        """
        try:
            self.log.info("Creating a new vote...")
            self.currentTime = int(round(time.time() * 1000))
            data = {"endDate": self.currentTime + (Game.VOTE_TIMEOUT * 1000) + 2000, "mod1": mod1, "mod2": mod2}
            requests.get("http://" + Game.settings["server_address"] + "/registerVote.php?session=" + self.sessionName + "&data=" + json.dumps(data))
            self.log.info("Vote created")
            self.wait_for(Game.VOTE_TIMEOUT + 2)
            return True
        except:
            self.log.warning("Cannot create vote event ! Is the hostname exist or the server running ?")
            return False

    def vote_result(self):
        """Donne le résultat des votes

        :return str: Résultat du vote
        :rtype str: str, None
        """
        vote_one = 0
        vote_two = 0
        self.log.info("Requesting vote output...")
        request_vote = requests.get("http://" + Game.settings["server_address"] + "/sessions.json").json()
        if request_vote is not None:
            for data in request_vote[self.sessionName].values():
                self.log.debug("Vote " + data)
                if data == "1":
                    vote_one += 1
                elif data == "2":
                    vote_two += 1
            if vote_one > vote_two:
                self.log.info("Majority of vote 1")
                return "1"
            elif vote_two > vote_one:
                self.log.info("Majority of vote 2")
                return "2"
            else:
                self.log.info("Vote equality")
                return "0"
        else:
            self.log.critical("Connection error (" + Game.settings["server_address"] + ")")
            self.log.critical("Vote request failed")
            return None

    def wait_for(self, time):
        """Spécifie le temps du timer en secondes

        :param time: Temps en seconde
        :type time: int
        """
        self.time_to_wait = time
        self.waitThread.start()

    def start_wait(self):
        """Lance le timer"""
        time.sleep(self.time_to_wait)
        self.vote_result()

    def get_player_count(self):
        """Évalue le nombre de joueurs connectés à la session

        :return nb: Nombre de joueurs connectés à la session
        :rtype nb: int, None
        """
        request = requests.get("http://" + Game.settings["server_address"] + "/sessions.json").json()
        if request is not None and self.sessionName in request:
            return len(request[self.sessionName])
        else:
            self.log.critical("Connection error (" + Game.settings["server_address"] + ")")
            return None

    def close(self):
        """Ferme la session actuelle"""
        request_close = requests.get("http://" + Game.settings["server_address"] + "/close.php?session=" + self.sessionName)
        self.keep = False
        try:
            success = request_close.json()
            if not success:
                self.log.critical("Connection error (" + Game.settings["server_address"] + ")")
                self.log.warning("Close session failed")
            self.log.info("Session closed")
        except Exception:
            self.log.critical("Unable to json: " + str(request_close.content))
            raise
