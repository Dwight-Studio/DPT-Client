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

    log = Game.get_logger("WebCom")
    sessionName = None
    sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))
    connected = False
    player_number = 0

    @classmethod
    def make_request(cls, url):
        logger_request = Game.get_logger("WebComs.Request")
        logger_json = Game.get_logger("WebComs.JSONDecoder")

        request = None
        message = None

        try:
            request = requests.get(url)

            message = request.json()

            return message
        except ConnectionAbortedError as ex:
            logger_request.critical("Connection aborted: " + str(ex))
            cls.connected = False
            return None
        except ConnectionRefusedError as ex:
            logger_request.critical("Connection refused: " + str(ex))
            cls.connected = False
            return None
        except ConnectionResetError as ex:
            logger_request.critical("Connection reset: " + str(ex))
            cls.connected = False
            return None
        except ConnectionError as ex:
            logger_request.critical("Connection error: " + str(ex))
            cls.connected = False
            return None
        except ValueError as ex:
            logger_json.critical("Can't decode request: " + str(ex))
            logger_json.critical("  " + str(request.content))

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

        for event in Game.events:
            if event.type == Game.KEEP_ALIVE_EVENT:
                if cls.sessionName is not None:
                    cls.make_request("http://" + Game.settings["server_address"] + "/keepAlive.php?session=" + cls.sessionName)
                else:
                    Game.get_logger("WebComs")
