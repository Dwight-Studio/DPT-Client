import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Start the game.')
parser.add_argument('--debug', help='enable debug logging', action="store_true")


def main():
    print("MAIN: Adding " + os.path.pardir + " to PYTHONPATH")
    sys.path.insert(0, os.path.pardir)
    from dpt.game import Game
    global game
    args = parser.parse_args()
    game = Game(args.debug)
    Game.set_instance(game)
    game.play()


if __name__ == '__main__':
    main()
