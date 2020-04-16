import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', help='enable debug logging', action="store_true")
parser.add_argument('--skipintro', help='skip intros', action="store_true")


def main():
    print("MAIN: Adding " + os.path.abspath(".") + " to PYTHONPATH")
    sys.path.insert(0, os.path.abspath("."))
    from dpt.game import Game
    args = parser.parse_args()
    Game.play(args.debug, args.skipintro)


if __name__ == '__main__':
    main()
