import logging
import argparse
import sys
import pygame
from pygame.locals import *

VERSION = "BETA-0.0.1"
PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
PYGAME_VERSION = pygame.version.ver
PLATFORM = sys.platform

# Loggers
LOGGING_FORMAT = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%H:%M:%S")
main_logger = None

parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', type=bool, help='enable/disable debug log', default=False)


def get_main_logging(debug):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("../latest.log")
    file_handler.setFormatter(LOGGING_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(LOGGING_FORMAT)

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

    main_logger = get_main_logging(True)

    main_logger.info("--- Starting Don't Play Together. ---")
    main_logger.debug("Version: " + VERSION)
    main_logger.debug("Python version: " + PYTHON_VERSION)
    main_logger.debug("Pygame version: " + PYGAME_VERSION)
    main_logger.debug("OS: " + PLATFORM)

if __name__ == '__main__':
    main()