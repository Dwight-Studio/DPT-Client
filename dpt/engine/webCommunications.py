import json
import random
import math
import string
import requests
import pygame
import time

from dpt.game import Game
from dpt.engine.gui.menu.text import Text
from threading import Thread

_return = None


class CommunicationError(object):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WebCommunication(object):
    """Gestionnaire des communication webs"""

    log = Game.get_logger(__name__)
    sessionName = None
    connected = False
    connected_players_count = 0
    last_result = None
    last_vote = None

    @classmethod
    def make_request(cls, url, silent=False):
        """Crée une requète vers un serveur

        :param url: URL à atteindre
        :type url: str
        :param silent: Parallèlisation
        :return: Erreur ou page parsé en JSON
        :rtype: dict, CommunicationError
        """
        global _return
        from dpt.engine.scenes import Scenes
        from dpt.engine.mainLoop import loading_loop

        def request(url):
            global _return
            logger_request = Game.get_logger("WebComs.Request")
            logger_json = Game.get_logger("WebComs.JSONDecoder")

            request = None

            try:
                request = requests.get(url)

                message = request.json()

                _return = message

            except requests.exceptions.RequestException as ex:
                logger_request.error(ex.__class__.__name__ + ": " + str(ex))
                pygame.event.post(pygame.event.Event(Game.DISCONNECTED_EVENT, {}))
                _return = CommunicationError("CommunicationError: " + ex.__class__.__name__)
            except json.decoder.JSONDecodeError as ex:
                logger_json.error(ex.__class__.__name__ + ": " + str(ex))
                pygame.event.post(pygame.event.Event(Game.DISCONNECTED_EVENT, {}))
                _return = CommunicationError("CommunicationError: " + ex.__class__.__name__)

        if not silent:
            Scenes.loading()
        thread = Thread(target=request, args=[url])
        thread.start()
        if silent:
            thread.join()
        else:
            while thread.is_alive():
                loading_loop()
            loading_loop(True)
        return _return

    @classmethod
    def init_connection(cls):
        """Crée la session sur le serveur"""

        cls.sessionName = "".join(random.choice(string.ascii_uppercase) for i in range(5))

        reply = cls.make_request("http://" + Game.settings["server_address"] + "/init.php?session=" + cls.sessionName)

        if not isinstance(reply, CommunicationError):
            cls.log.info("Session " + cls.sessionName + " created")
            cls.log.info("URL: http://" + Game.settings["server_address"] + "/?session=" + cls.sessionName)
            pygame.time.set_timer(Game.KEEP_ALIVE_EVENT, 5000)
            pygame.event.post(pygame.event.Event(Game.KEEP_ALIVE_EVENT))
            cls.connected = True
            return True
        else:
            cls.log.critical("Session creation failed")
            return reply

    @classmethod
    def reconnect(cls):
        """Recrée la session sur le serveur, avec la même ID"""
        reply = cls.make_request("http://" + Game.settings["server_address"] + "/init.php?session=" + cls.sessionName)

        if not isinstance(reply, CommunicationError):
            cls.log.info("Session " + cls.sessionName + " created")
            cls.log.info("URL: http://" + Game.settings["server_address"] + "/?session=" + cls.sessionName)
            pygame.time.set_timer(Game.KEEP_ALIVE_EVENT, 0)
            pygame.time.set_timer(Game.VOTE_TIMEOUT, 0)
            pygame.time.set_timer(Game.KEEP_ALIVE_EVENT, 5000)
            pygame.event.post(pygame.event.Event(Game.KEEP_ALIVE_EVENT))
            cls.connected = True
            return True
        else:
            cls.log.critical("Session reconnection failed")
            pygame.time.set_timer(Game.WAIT_BETWEEN_RECONNECT_EVENT, 2000, True)
            return reply

    @classmethod
    def update(cls):
        """Actualise les communications"""
        if cls.sessionName is not None:
            for event in Game.events:
                if event.type == Game.KEEP_ALIVE_EVENT:
                    def ka():
                        if cls.connected:
                            reply = cls.make_request("http://" + Game.settings["server_address"] + "/keepAlive.php?session=" + cls.sessionName, True)

                            if isinstance(reply, CommunicationError):
                                return

                            reply = cls.make_request("http://" + Game.settings["server_address"] + "/sessions.json", True)

                            if "wb_player_count" not in Game.gui:
                                Game.gui["wb_player_count"]: Text(Game.surface.get_size()[0] - math.floor(Game.DISPLAY_RATIO * 220),
                                                                  0,
                                                                  "Connexion au serveur...",
                                                                  math.floor(25 * Game.DISPLAY_RATIO),
                                                                  (0, 0, 0),
                                                                  "dpt.fonts.DINOT_CondBlack")

                            if isinstance(reply, CommunicationError) or cls.sessionName not in reply:
                                cls.log.warning("Can't get connected players count")
                                Game.gui["wb_player_count"].text = "Déconnecté du serveur"
                                Game.gui["wb_player_count"].color = (255, 0, 0)
                                return

                            nb = str(len(reply[cls.sessionName]))

                            while len(nb) < 3:
                                nb = "0" + nb

                            Game.gui["wb_player_count"].text = "Joueurs connectés : " + nb
                            Game.gui["wb_player_count"].color = (0, 0, 0)

                        else:
                            Game.gui["wb_player_count"]: Text(Game.surface.get_size()[0] - math.floor(Game.DISPLAY_RATIO * 220),
                                                              0,
                                                              "Déconnecté du serveur",
                                                              math.floor(25 * Game.DISPLAY_RATIO),
                                                              (255, 0, 0),
                                                              "dpt.fonts.DINOT_CondBlack")

                            Game.gui["wb_player_count"].text = "Déconnecté du serveur"
                            Game.gui["wb_player_count"].color = (255, 0, 0)

                    Thread(target=ka).start()
                    continue

                elif event.type == Game.VOTE_FINISHED_EVENT:
                    if cls.connected:
                        vote_one = 0
                        vote_two = 0
                        cls.log.info("Requesting vote output...")

                        reply = cls.make_request("http://" + Game.settings["server_address"] + "/sessions.json")

                        if not isinstance(reply, CommunicationError):
                            if cls.sessionName not in reply:
                                pygame.event.post(pygame.event.Event(Game.DISCONNECTED_EVENT, {}))
                                return

                            if isinstance(reply[cls.sessionName], list):
                                cls.log.info("Draw")
                                cls.last_result = "Both"
                            else:
                                for data in reply[cls.sessionName].values():
                                    cls.log.debug("Vote " + data)
                                    if data == "1":
                                        vote_one += 1
                                    elif data == "2":
                                        vote_two += 1
                                if vote_one > vote_two:
                                    cls.log.info("Effect 1 won")
                                    cls.last_result = cls.last_vote[0]
                                elif vote_two > vote_one:
                                    cls.log.info("Effect 2 won")
                                    cls.last_result = cls.last_vote[1]
                                else:
                                    cls.log.info("Draw")
                                    cls.last_result = "Both"

                            event = pygame.event.Event(Game.VOTE_RESULT_AVAILABLE_EVENT, {"results": cls.last_result})
                            pygame.event.post(event)

                        else:
                            cls.log.error("Results request failed")
                            continue
                    else:
                        cls.log.warning("Handling VOTE_FINISHED_EVENT while disconnected")
                        continue

                elif event.type == Game.WAIT_BETWEEN_RECONNECT_EVENT:
                    cls.reconnect()
                elif event.type == Game.DISCONNECTED_EVENT:
                    cls.connected = False
                    cls.reconnect()

        Text.main_loop()

    @classmethod
    def close(cls):
        """Ferme la session actuelle"""
        if cls.connected:
            reply = cls.make_request("http://" + Game.settings["server_address"] + "/close.php?session=" + cls.sessionName)
            pygame.time.set_timer(Game.KEEP_ALIVE_EVENT, 0)

            cls.last_vote = None

            if not isinstance(reply, CommunicationError):
                cls.log.info("Session closed")
            else:
                cls.log.warning("Failed to close session, ignoring (session will be marked as timedOut in few seconds)")

    @classmethod
    def create_vote_event(cls, mod1, mod2):
        """Crée un évènement de vote

        :param mod1: Modificateur 1
        :type mod1: str
        :param mod2: Modificateur 2
        :type mod2: str
        :rtype: bool
        :return: Retourne True si le vote est correctement créé sinon False
        """

        cls.log.info("Creating a new vote...")
        current_time = int(round(time.time() * 1000))

        data = {"endDate": current_time + (Game.VOTE_TIMEOUT * 1000) + 2000,
                "mod1": mod1,
                "mod2": mod2}

        reply = cls.make_request("http://" + Game.settings["server_address"] + "/registerVote.php?session=" + cls.sessionName + "&data=" + json.dumps(data), True)

        if isinstance(reply, CommunicationError):
            cls.log.error("Can't create vote event")
            return reply

        cls.log.info("Vote created, results will be available in " + str(Game.VOTE_TIMEOUT + 2) + " seconds")

        cls.last_vote = (mod1, mod2)
        pygame.time.set_timer(Game.VOTE_FINISHED_EVENT, (Game.VOTE_TIMEOUT + 2) * 1000, True)
        return True
