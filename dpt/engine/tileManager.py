import math
import pygame
from dpt.engine.gui.editor.editorPanel import EditorPanel
from dpt.engine.gui.editor.panelFakeEntities import PanelFakeEntity
from dpt.engine.gui.editor.tileEditor import TileEditor
from dpt.engine.backgroundFakeBlocks import BackgroundFakeBlocks
from dpt.engine.gui.menu.bar import Bar
from dpt.engine.gui.menu.button import Button
from dpt.engine.gui.menu.checkbox import Checkbox
from dpt.engine.gui.menu.progressbar import ProgressBar
from dpt.engine.loader import RessourceLoader, UnreachableRessourceError
from dpt.game import Game
from random import randint


#          {"x, y": {"blockClass": Classe}}
class TileManager:
    deadly_object_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    environment_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()
    editor_panel_group = pygame.sprite.Group()
    background_blocks_group = pygame.sprite.Group()
    foreground_blocks_group = pygame.sprite.Group()
    interactible_blocks_group = pygame.sprite.Group()
    clouds_group = pygame.sprite.Group()

    log = Game.get_logger("TileManager")
    levelName = None
    max_width_size = 0
    max_height_size = 0
    count = 0
    already_defined = False
    per_line_count = 0
    per_line = 0
    nb_skip = 0
    check_back = False
    used_resources = []
    coords = None
    camera = None
    Game.available_tiles = []
    Game.available_tiles.extend(RessourceLoader.select_entries("dpt.blocks.*"))
    Game.available_tiles.remove("dpt.blocks.notfound")
    Game.available_tiles.extend(RessourceLoader.select_entries("dpt.entities.*"))
    loadlevel = False

    @classmethod
    def load_level(cls, level_name):
        cls.loadlevel = True
        if Game.player_sprite is not None:
            Game.player_sprite.kill()
            Game.player_sprite = None
        Game.player_group.empty()

        TileManager.editor_panel_group.empty()
        TileEditor.ghost_block_group.empty()
        TileManager.interactible_blocks_group.empty()

        for entity in TileManager.entity_group:
            entity.kill()

        for block in TileManager.environment_group:
            block.kill()

        for block in TileManager.background_blocks_group:
            block.kill()

        if TileEditor.in_editor:
            RessourceLoader.add_pending("dpt.blocks.*")
            RessourceLoader.add_pending("dpt.entities.*")
            RessourceLoader.add_pending("dpt.images.environment.*")
            RessourceLoader.add_pending("dpt.images.characters.*")
            RessourceLoader.add_pending("dpt.sounds.*")
            RessourceLoader.load()

        if type(level_name) == str:
            cls.log.info("Loading level " + level_name)
            cls.log.debug("Loading level main file")
            RessourceLoader.add_pending(level_name)
            RessourceLoader.load()
            level = RessourceLoader.get(level_name)
        else:
            cls.log.info("Loading unknown level")
            level = level_name
        cls.max_width_size = 0
        cls.max_height_size = 0
        if level is None:
            cls.log.critical("The level can't be loaded")
            return False

        if not TileEditor.in_editor:
            cls.log.debug("Loading level blocks and entities")
            for keys in level:
                if "class" in level[keys]:
                    RessourceLoader.add_pending(level[keys]["class"])
                if "backgroundClass" in level[keys]:
                    RessourceLoader.add_pending(level[keys]["backgroundClass"])
            RessourceLoader.load()

        if not TileEditor.in_editor:
            cls.log.debug("Loading textures")
            for keys in level:
                if "class" in level[keys]:
                    obj = RessourceLoader.get(level[keys]["class"])
                    RessourceLoader.add_pending(obj.texture)
                    if hasattr(obj, "textures"):
                        RessourceLoader.add_pending(obj.textures)
                    if hasattr(obj, "sounds"):
                        RessourceLoader.add_pending(obj.sounds)
                if "backgroundClass" in level[keys]:
                    obj = RessourceLoader.get(level[keys]["backgroundClass"])
                    RessourceLoader.add_pending(obj.texture)
                    if hasattr(obj, "textures"):
                        RessourceLoader.add_pending(obj.textures)
                    if hasattr(obj, "sounds"):
                        RessourceLoader.add_pending(obj.sounds)
            RessourceLoader.add_pending("dpt.images.characters.player.*")
            RessourceLoader.load()

        for keys in level:
            cls.coords = tuple(map(int, keys.split(", ")))
            if cls.coords[0] > cls.max_width_size:
                cls.max_width_size = cls.coords[0]
            elif cls.coords[1] > cls.max_height_size:
                cls.max_height_size = cls.coords[1]
            if cls.coords[0] < 0 or cls.coords[1] < 0:
                cls.log.warning("The tile position can't be negative : " + keys)
                continue
            if "class" in level[keys]:
                if "customPlace" in level[keys]:
                    try:
                        RessourceLoader.get(level[keys]["class"])(cls.coords[0], cls.coords[1])
                        cls.log.debug("Tile " + level[keys]["class"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["class"] + " for tile : " + keys)
                else:
                    try:
                        RessourceLoader.get(level[keys]["class"])(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE)
                        cls.log.debug("Tile " + level[keys]["class"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["class"] + " for tile : " + keys)
            if "backgroundClass" in level[keys]:
                if "customPlace" in level[keys]:
                    try:
                        BackgroundFakeBlocks(cls.coords[0], cls.coords[1], level[keys]["backgroundClass"])
                        cls.log.debug("Background tile " + level[keys]["backgroundClass"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["backgroundClass"] + " for tile : " + keys)
                else:
                    try:
                        BackgroundFakeBlocks(cls.coords[0] * Game.TILESIZE, cls.coords[1] * Game.TILESIZE, level[keys]["backgroundClass"])
                        cls.log.debug("Background tile " + level[keys]["backgroundClass"] + " placed at " + keys)
                    except UnreachableRessourceError:
                        cls.log.warning("Invalid class name : " + level[keys]["backgroundClass"] + " for tile : " + keys)

        if not TileEditor.in_editor:
            from dpt.engine.characters.yesOnceAgainThereIsANewPlayerFile import PlayerSprite
            Game.player_sprite = PlayerSprite(300, Game.surface.get_size()[1] - 500)
            Game.player_group.add(Game.player_sprite)
            if TileManager.max_width_size < math.floor(Game.surface.get_size()[0] / Game.TILESIZE):
                TileManager.max_width_size = math.floor(Game.surface.get_size()[0] / Game.TILESIZE) + 2
            cls.camera = Camera(TileManager.max_width_size, TileManager.max_height_size)
        elif TileEditor.in_editor:
            from dpt.engine.gui.editor.charEntity import CharEntity
            Game.player_sprite = CharEntity()
            Game.player_group.add(Game.player_sprite)
            cls.camera = EditorCamera(TileManager.max_width_size, TileManager.max_height_size)
        TileEditor.created_level = level
        cls.levelName = level_name
        Game.freeze_game = False
        cls.loadlevel = False
        cls.generate_clouds()
        cls.log.info("Done")
        return True

    @classmethod
    def ghost_block(cls, x_tile, y_tile, item):
        from dpt.engine.ghostFakeEntities import GhostFakeEntity
        ghost_block = GhostFakeEntity(x_tile, y_tile, 80, item)

    @classmethod
    def place_block(cls, x_tile, y_tile, item):
        if not TileEditor.custom_tile_placement:
            RessourceLoader.get(item)(x_tile * Game.TILESIZE, y_tile * Game.TILESIZE)
            cls.log.debug("Tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))
        elif TileEditor.custom_tile_placement:
            RessourceLoader.get(item)(x_tile, y_tile)
            cls.log.debug("Tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))

    @classmethod
    def place_back_block(cls, x_tile, y_tile, item):
        if not TileEditor.custom_tile_placement:
            BackgroundFakeBlocks(x_tile * Game.TILESIZE, y_tile * Game.TILESIZE, item)
            cls.log.debug("Background tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))
        elif TileEditor.custom_tile_placement:
            BackgroundFakeBlocks(x_tile, y_tile, item)
            cls.log.debug("Background tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))

    @classmethod
    def open_tile_panel(cls):
        TileManager.editor_panel_group.empty()
        Game.editor_tile_registry.clear()
        value = bool(cls.check_back)
        Checkbox.checkbox_group.empty()
        cls.check_back = Checkbox(Game.surface.get_size()[0] // 4 * 3 + Game.TILESIZE // 4, Game.TILESIZE // 4, 1)
        cls.check_back.value = value
        cls.count = 0
        panel = EditorPanel((255, 255, 255), Game.surface.get_size()[0] / 4 * 3, 0, Game.surface.get_size()[0] / 4, Game.surface.get_size()[1], 120)
        TileManager.editor_panel_group.add(panel)
        startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
        starty = 0 + Game.TILESIZE
        for element in Game.available_tiles:
            if cls.count == cls.nb_skip:
                sprite = PanelFakeEntity(startx, starty, 255, element)
                Game.editor_tile_registry[str(math.floor(startx / Game.TILESIZE)) + ", " + str(math.floor(starty / Game.TILESIZE))] = {"class": element}
                startx += Game.TILESIZE
                cls.per_line_count += 1
                if math.floor(startx) >= Game.surface.get_size()[0] - Game.TILESIZE:
                    startx = Game.surface.get_size()[0] / 4 * 3 + Game.TILESIZE
                    starty += Game.TILESIZE
                    if not cls.already_defined:
                        cls.per_line = cls.per_line_count
                        cls.already_defined = True
            else:
                cls.count += 1
                continue

    @classmethod
    def scroll_down(cls):
        if TileEditor.panel_open:
            cls.nb_skip += cls.per_line
            TileManager.open_tile_panel()

    @classmethod
    def scroll_up(cls):
        if TileEditor.panel_open:
            TileManager.editor_panel_group.empty()
            Checkbox.checkbox_group.empty()
            Game.editor_tile_registry.clear()
            if cls.nb_skip > 0:
                cls.nb_skip -= cls.per_line
            TileManager.open_tile_panel()

    @classmethod
    def out_of_window(cls):
        for enemy in TileManager.enemy_group:
            if enemy.rect.centery >= 3000:
                enemy.kill()
                del enemy

    @classmethod
    def get_sprite_count(cls):
        return len(cls.background_blocks_group) + len(cls.entity_group) + len(cls.environment_group)

    @classmethod
    def display_cam_info(cls):
        obj_count = TileManager.camera.sprite_count + len(TileManager.foreground_blocks_group) + len(
            TileManager.deadly_object_group) + len(Button.buttonsGroup) + len(Button.text_sprite_buttonsGroup) + len(
            Button.text_buttonsList) + len(Checkbox.checkbox_group) + len(ProgressBar.progress_bar_group) + len(
            ProgressBar.bar_group)

        Game.add_debug_info("CAMERA INFORMATIONS")
        Game.add_debug_info("Scrolling: " + str(-TileManager.camera.last_x))
        if not TileEditor.in_editor:
            Game.add_debug_info("Right: " + str(Game.player_sprite.right))
            Game.add_debug_info("Left: " + str(Game.player_sprite.left))
        Game.add_debug_info("Player X:" + str(TileManager.camera.target.rect.centerx))
        Game.add_debug_info("Player Y: " + str(TileManager.camera.target.rect.centery))
        Game.add_debug_info("Displaying " + str(obj_count) + " objects")
        Game.add_debug_info("World: ")
        Game.add_debug_info("   " + str(len(Game.player_group)) + " players")
        Game.add_debug_info("   " + str(len(TileManager.entity_group)) + " entities")
        Game.add_debug_info("   " + str(len(TileManager.environment_group)) + " blocks")
        Game.add_debug_info("   " + str(len(TileManager.background_blocks_group)) + " background blocks")
        Game.add_debug_info("   " + str(len(TileManager.foreground_blocks_group)) + " foreground blocks")
        Game.add_debug_info("   " + str(len(TileManager.deadly_object_group)) + " deadly objects")
        Game.add_debug_info("   " + str(len(Button.buttonsGroup)) + " buttons")
        Game.add_debug_info("       " + str(len(Button.text_sprite_buttonsGroup)) + " texts (sprites)")
        Game.add_debug_info("       " + str(len(Button.text_buttonsList)) + " texts")
        Game.add_debug_info("   " + str(len(Checkbox.checkbox_group)) + " checkbox")
        Game.add_debug_info("   " + str(len(ProgressBar.progress_bar_group)) + " progress bars")
        Game.add_debug_info("       " + str(len(ProgressBar.bar_group)) + " bars")
        Game.add_debug_info("----------")

    @classmethod
    def display_sprites(cls, self):
        rect = Game.surface.get_bounding_rect()
        rect.width += 200
        rect.x -= self.last_x + 100
        Game.display_rect = rect
        for sprite in TileManager.background_blocks_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_RECT:
                    pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.environment_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_RECT:
                    pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.entity_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_RECT:
                    pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        for sprite in Game.player_group:
            sprite.update()
            Game.surface.blit(sprite.image, self.apply(sprite))
            self.sprite_count += 1
            if Game.DISPLAY_RECT:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        for sprite in TileManager.deadly_object_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foreground_blocks_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.interactible_blocks_group:
            if sprite.rect.colliderect(rect):
                sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))

    @classmethod
    def generate_clouds(cls):
        from dpt.engine.gui.Cloud import Cloud
        xpos = 10
        for i in range(10):
            xpos += randint(Game.surface.get_size()[0] // 14, Game.surface.get_size()[0] // 8)
            ypos = randint(0, Game.surface.get_size()[1] // 4)
            sprite = Cloud(xpos, ypos)
            cls.clouds_group.add(sprite)
            cls.clouds_group.draw(Game.surface)

    @classmethod
    def update_clouds(cls):
        from dpt.engine.gui.Cloud import Cloud
        for cloud in cls.clouds_group:
            if cloud.rect.x <= 1:
                cls.clouds_group.remove(cloud)
                del cloud
                ypos = randint(0, Game.surface.get_size()[1] // 4)
                sprite = Cloud(Game.surface.get_size()[0], ypos)
                cls.clouds_group.add(sprite)
                cls.clouds_group.draw(Game.surface)

class Camera:
    def __init__(self, width, height):
        self.userConfirm = True
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("Camera")
        self.x = 0
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.sprite_count = 0
        self.target = target
        self.x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        calcul = (self.width * Game.TILESIZE) - Game.surface.get_size()[0]
        self.x = min(0, self.last_x, self.x)
        self.x = max(-calcul, self.x)
        self.camera = pygame.Rect(self.x, 0, self.width, self.height)
        TileManager.display_sprites(self)
        self.last_x = self.x

        TileManager.display_cam_info()


class EditorCamera:
    def __init__(self, width, height):
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("EditorCamera")
        self.x = 0
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.sprite_count = 0
        self.target = target
        self.x = -target.rect.x + int(Game.surface.get_size()[0] / 2)
        self.x = min(0, self.x)
        self.camera = pygame.Rect(self.x, 0, self.width, self.height)
        TileManager.display_sprites(self)
        self.last_x = self.x

        TileManager.display_cam_info()

    def enable_grid(self):
        for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
        for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))
