from dpt.engine.graphics.platforms.Block import Block
from dpt.game import Game


class Level1(object):
    def __init__(self):
        game = Game.get_instance()
        platformList = []
        x = y = 0
        level = ["      P   ",
                 "  P       ",
                 "       P  ",
                 "          ",
                 "PPP     PP"]

        for row in level:
            for col in row:
                if col == "P":
                    P = Block((128, 128, 0), x, y, 30, 30)
                    game.platforms.add(P)
                    platformList.append(P)
                x += 30
            y += 30
            x = 0

        totalLevelWidth = len(level[0]) * 30
        totalLevelHeight = len(level) * 30
