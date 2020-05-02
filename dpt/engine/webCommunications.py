import json
import random
import string
import threading
import time
import requests
import pygame

from dpt.game import Game

class Communication(object):
    """Gestionnaire des communication webs"""

    log = Game.get_logger("root.WebCom")
    sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
    connected = False
    player_number = 0

    @classmethod
    def make_request(cls, url):
        logger_request = Game.get_logger("root.WebComs.Request")
        logger_json = Game.get_logger("root.WebComs.JSONDecoder")
        try:
            request = requests.get(url)

        except ConnectionAbortedError:
            Game.get_logger("root.WebComs").critical("Connection error: Connection aborted")
            return False
        except ConnectionRefusedError:
            Game.get_logger("root.WebComs").critical("Connection error: Connection refused")
            return False
        except ConnectionResetError:
            Game.get_logger("root.WebComs").critical("Connection error: Connection reset")
            return False
        except ConnectionError:
            logger = Game.get_logger("root.WebComs").critical("Connection error: Can't connect to server")
            return False

    @classmethod
    def create(cls):
        """Crée la session sur le serveur """
        try:
            request = requests.get("http://" + Game.settings["server_address"] + "/init.php?session=" + cls.sessionName)
            if request.json() == cls.sessionName:
                cls.log.info("Created session : " + cls.sessionName)
                cls.log.info("http://" + Game.settings["server_address"] + "/?session=" + cls.sessionName)
                cls.log.info("KeepAlive event sent")
                pygame.time.set_timer(Game.KEEP_ALIVE_EVENT, 5000)
                return True
            else:
                cls.log.critical("Session creation failed")
                return False
        except:
            cls.log.warning("Hostname not found. Is the server running ? Check the server address !")

    @classmethod
    def update(cls):
