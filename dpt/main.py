import logging
from logging.handlers import RotatingFileHandler
import argparse
import sys

VERSION = "BETA-0.0.1"
PYTHON_VERSION = "3.7"
PLATFORM = sys.platform

parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', type=bool, help='enable/disable debug log', default=False)


def setup_main_logging():
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)%s ] %(message)s")

    logger = logging.getLogger()
    main_file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    main_file_handler.setLevel(logging.DEBUG)


def main():
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info("Starting Don't Play Together.")
    logger.debug("Version: " + VERSION)
    logger.debug("Python version: " + PYTHON_VERSION)
    logger.debug("")
    logger.debug("OS: ")


if __name__ == '__main__':
    main()
