import datetime
import logging
import argparse
import sys
import tarfile

import pygame
import os.path
from pygame.locals import *

VERSION = "ALPHA-0.0.1"
PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
PYGAME_VERSION = pygame.version.ver
PLATFORM = sys.platform
ROOT_DIRECTORY = os.path.abspath("../")

# Logs
## Loggers
main_logger = None

## Formatter
LOGGING_FORMAT = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")

## File handler
if not os.path.isdir(ROOT_DIRECTORY + "/logs/"):
    os.mkdir(ROOT_DIRECTORY + "/logs/")

if os.path.isfile(ROOT_DIRECTORY + "/logs/latest.log"):
    file = tarfile.open(ROOT_DIRECTORY + "/logs/" + datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S") + ".tar.gz", mode="x:gz", )
    file.add(ROOT_DIRECTORY + "/logs/latest.log", arcname="latest.log")
    file.close()
    os.remove(ROOT_DIRECTORY + "/logs/latest.log")

file_handler = logging.FileHandler(ROOT_DIRECTORY + "/logs/latest.log")
file_handler.setFormatter(LOGGING_FORMAT)

## Stream handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(LOGGING_FORMAT)

# Args
parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', help='enable debug logging', action="store_true")


def get_loggers(debug):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if debug:
        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
        stream_handler.setLevel(logging.INFO)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.debug("Logger initied.")
    return logger


def main():
    global main_logger
    pygame.init()
    args = parser.parse_args()

    main_logger = get_loggers(args.debug)

    main_logger.info("--- Starting Don't Play Together. ---")
    main_logger.debug("Version: " + VERSION)
    main_logger.debug("Python version: " + PYTHON_VERSION)
    main_logger.debug("Pygame version: " + PYGAME_VERSION)
    main_logger.debug("OS: " + PLATFORM)

if __name__ == '__main__':
    main()
