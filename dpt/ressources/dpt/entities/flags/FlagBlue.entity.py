import pygame

from dpt.engine.effectsManagement import EffectsManagement
from dpt.engine.loader import RessourceLoader
from dpt.game import Game


class FlagBlue(pygame.sprite.Sprite):
    checkpoint_list = []

    texture = "dpt.images.environment.flag.Flag_Blue"
    sounds = "dpt.sounds.sfx.sfx_stone"
    screen_width, screen_height = (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
    width = Game.TILESIZE
    height = Game.TILESIZE * 2
    offset_x = 0
    offset_y = -Game.TILESIZE

    def __init__(self, x, y):
        from dpt.engine.tileManager import TileManager
        pygame.sprite.Sprite.__init__(self, TileManager.entity_group, TileManager.interactible_blocks_group, TileManager.foreground_blocks_group)  # Sprite's constructor called
        self.image = RessourceLoader.get(self.texture)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.offset_x
        self.rect.y = y + self.offset_y
        self.id = None
        self.already_activated = False
        if not TileManager.is_loading_level:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()

        FlagBlue.checkpoint_list.append(self)

    def update(self):
        from dpt.engine.gui.menu.timer import Timer
        for i in Game.player_group:
            if pygame.sprite.collide_mask(self, i) and not self.already_activated:
                self.already_activated = True
                if "last_checkpoint" in Game.temp:
                    last = Game.temp["last_checkpoint"]
                    Game.temp["last_checkpoint"] = max(self.id, Game.temp["last_checkpoint"])
                    if Game.temp["last_checkpoint"] == self.id and Game.temp["last_checkpoint"] != last:
                        Game.temp["last_checkpoint_time"] = Timer.time
                        Game.temp["last_checkpoint_life"] = Game.life
                        Game.temp["last_checkpoint_effects"] = {}
                        Game.temp["last_checkpoint_coins"] = RessourceLoader.get("dpt.entities.Coin").coin_checkpoint_list
                        for key, value in EffectsManagement.__dict__.items():
                            Game.temp["last_checkpoint_effects"].update({key: value})
                    else:
                        Game.get_logger(FlagBlue.__name__).warning("This checkpoint is not the last checkpoint")

                else:
                    Game.temp["last_checkpoint"] = self.id
                    Game.temp["last_checkpoint_time"] = Timer.time
                    Game.temp["last_checkpoint_life"] = Game.life
                    Game.temp["last_checkpoint_effects"] = {}
                    for key, value in EffectsManagement.__dict__.items():
                        Game.temp["last_checkpoint_effects"].update({key: value})

    @classmethod
    def compute_ids(cls):
        def x(el):
            return el.rect.x

        cls.checkpoint_list.sort(key=x)

        for id in range(len(cls.checkpoint_list)):
            cls.checkpoint_list[id].id = id