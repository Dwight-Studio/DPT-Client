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
from dpt.engine.gui.menu import Text
from random import randrange


#          {"x, y": {"blockClass": Classe}}
class TileManager:
    """Gestionnaire des tiles"""
    deadly_object_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    environment_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()
    editor_panel_group = pygame.sprite.Group()
    background_blocks_group = pygame.sprite.Group()
    foreground_blocks_group = pygame.sprite.Group()
    interactible_blocks_group = pygame.sprite.Group()
    heart_group = pygame.sprite.Group()
    clouds_group = pygame.sprite.LayeredUpdates()

    log = Game.get_logger(__name__)
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
    clouds_last_x = None
    try:
        Game.available_tiles = []
        Game.available_tiles.extend(RessourceLoader.select_entries("dpt.blocks.*"))
        Game.available_tiles.remove("dpt.blocks.notfound")
        Game.available_tiles.extend(RessourceLoader.select_entries("dpt.entities.*"))
    except:
        pass
    is_loading_level = False

    @classmethod
    def load_level(cls, level_name):
        """Charge un niveau

        :param checkpoint: Checkpoint à charger
        :param level_name: Niveau à charger
        :type level_name: str, dict

        :return: True si le niveau est chargée sans problème, sinon False
        :rtype: bool
        """

        cls.is_loading_level = True
        if Game.player_sprite is not None:
            Game.player_sprite.kill()
            Game.player_sprite = None
        Game.player_group.empty()

        TileManager.editor_panel_group.empty()
        TileEditor.ghost_block_group.empty()
        TileManager.interactible_blocks_group.empty()
        TileManager.clouds_group.empty()

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
            RessourceLoader.add_pending("dpt.entities.Flag*")
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
            RessourceLoader.add_pending("dpt.images.environment.flag.*")
            RessourceLoader.add_pending("dpt.images.environment.background.Cloud_full_*")
            RessourceLoader.add_pending("dpt.images.gui.ui.UI_HEART*")
            RessourceLoader.load()

        from dpt.engine.scenes import Scenes
        Scenes.loading()

        RessourceLoader.get("dpt.entities.FlagBlue").checkpoint_list = []

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

        RessourceLoader.get("dpt.entities.FlagBlue").compute_ids()

        if not TileEditor.in_editor:
            player_x = 300
            player_y = Game.surface.get_size()[1] - 500

            sf = RessourceLoader.get("dpt.entities.FlagGreen").spawn_flag

            if sf is not None:
                player_x = sf.rect.x - sf.offset_x
                player_y = sf.rect.y - sf.offset_y

            if "last_checkpoint" in Game.temp:
                cp = RessourceLoader.get("dpt.entities.FlagBlue").checkpoint_list[Game.temp["last_checkpoint"]]
                player_x = cp.rect.x - cp.offset_x
                player_y = cp.rect.y - cp.offset_y

            from dpt.engine.characters.PlayerSprite import PlayerSprite
            Game.player_sprite = PlayerSprite(player_x, player_y)

            if TileManager.max_width_size < math.floor(Game.surface.get_size()[0] / Game.TILESIZE):
                TileManager.max_width_size = math.floor(Game.surface.get_size()[0] / Game.TILESIZE) + 2
            cls.camera = Camera(TileManager.max_width_size, TileManager.max_height_size)
        elif TileEditor.in_editor:
            from dpt.engine.gui.editor.charEntity import CharEntity
            Game.player_sprite = CharEntity()
            cls.camera = EditorCamera(TileManager.max_width_size, TileManager.max_height_size)
        TileEditor.created_level = level
        cls.levelName = level_name
        Game.freeze_game = False
        cls.is_loading_level = False
        cls.clouds_last_x = 0
        cls.generate_clouds()
        cls.log.info("Done")
        Game.loading = False
        return True

    @classmethod
    def ghost_block(cls, x_tile, y_tile, item):
        """Crée un faux block / fausse entitée

        :param x_tile: Abscisse (Tile)
        :type x_tile: int
        :param y_tile: Ordonnée (Tile)
        :type y_tile: int
        :param item: Type d'entitée à utiliser
        :type item: str
        """

        from dpt.engine.ghostFakeEntities import GhostFakeEntity
        GhostFakeEntity(x_tile, y_tile, 80, item)

    @classmethod
    def place_block(cls, x_tile, y_tile, item):
        """Crée un bloc

        :param x_tile: Abscisse (Tile)
        :type x_tile: int
        :param y_tile: Ordonnée (Tile)
        :type y_tile: int
        :param item: Type d'entitée à utiliser
        :type item: str
        """

        if not TileEditor.custom_tile_placement:
            RessourceLoader.get(item)(x_tile * Game.TILESIZE, y_tile * Game.TILESIZE)
            cls.log.debug("Tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))
        elif TileEditor.custom_tile_placement:
            RessourceLoader.get(item)(x_tile, y_tile)
            cls.log.debug("Tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))

    @classmethod
    def place_back_block(cls, x_tile, y_tile, item):
        """Crée un bloc d'arrière plan

        :param x_tile: Abscisse (Tile)
        :type x_tile: int
        :param y_tile: Ordonnée (Tile)
        :type y_tile: int
        :param item: Type d'entitée à utiliser
        :type item: str
        """

        if not TileEditor.custom_tile_placement:
            BackgroundFakeBlocks(x_tile * Game.TILESIZE, y_tile * Game.TILESIZE, item)
            cls.log.debug("Background tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))
        elif TileEditor.custom_tile_placement:
            BackgroundFakeBlocks(x_tile, y_tile, item)
            cls.log.debug("Background tile " + item + " placed at " + str(x_tile) + ", " + str(y_tile))

    @classmethod
    def open_tile_panel(cls):
        """Génère le panneau d'édition"""

        TileManager.editor_panel_group.empty()
        EditorPanel.editor_tile_registry.clear()
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
                EditorPanel.editor_tile_registry[str(math.floor(startx / Game.TILESIZE)) + ", " + str(math.floor(starty / Game.TILESIZE))] = {"class": element}
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
        """Gère le déroulement du panneau d'édition vers le bas"""
        if TileEditor.panel_open:
            cls.nb_skip += cls.per_line
            TileManager.open_tile_panel()

    @classmethod
    def scroll_up(cls):
        """Gère le déroulement du panneau d'édition vers le haut"""
        if TileEditor.panel_open:
            TileManager.editor_panel_group.empty()
            Checkbox.checkbox_group.empty()
            EditorPanel.editor_tile_registry.clear()
            if cls.nb_skip > 0:
                cls.nb_skip -= cls.per_line
            TileManager.open_tile_panel()

    @classmethod
    def out_of_window(cls):
        """Tue les ennemis sorties de la carte"""
        for enemy in TileManager.enemy_group:
            if enemy.rect.centery >= 3000:
                enemy.kill()
                del enemy

    @classmethod
    def display_cam_info(cls):
        """Affiche les informations de déboggage de la caméra"""
        obj_count = TileManager.camera.sprite_count + len(Button.buttonsGroup) + len(Button.text_sprite_buttonsGroup) + len(
            Button.text_buttonsList) + len(Checkbox.checkbox_group) + len(ProgressBar.progress_bar_group) + len(
            ProgressBar.bar_group) + len(TileManager.clouds_group) + len(TileManager.interactible_blocks_group)

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
        Game.add_debug_info("   " + str(len(TileManager.clouds_group)) + " clouds")
        Game.add_debug_info("   " + str(len(TileManager.entity_group)) + " entities")
        Game.add_debug_info("   " + str(len(TileManager.environment_group)) + " blocks")
        Game.add_debug_info("   " + str(len(TileManager.background_blocks_group)) + " background blocks")
        Game.add_debug_info("   " + str(len(TileManager.foreground_blocks_group)) + " foreground blocks")
        Game.add_debug_info("   " + str(len(TileManager.interactible_blocks_group)) + " interactible blocks")
        Game.add_debug_info("   " + str(len(TileManager.deadly_object_group)) + " deadly objects")
        Game.add_debug_info("   " + str(len(Button.buttonsGroup)) + " buttons")
        Game.add_debug_info("       " + str(len(Button.text_sprite_buttonsGroup)) + " texts (sprites)")
        Game.add_debug_info("       " + str(len(Button.text_buttonsList)) + " texts")
        Game.add_debug_info("   " + str(len(Checkbox.checkbox_group)) + " checkbox")
        Game.add_debug_info("   " + str(len(ProgressBar.progress_bar_group)) + " progress bars")
        Game.add_debug_info("       " + str(len(ProgressBar.bar_group)) + " bars")
        Game.add_debug_info("   " + str(len(Text.text_list)) + " Texts")
        Game.add_debug_info("----------")

    @classmethod
    def display_sprites(cls, self, freeze):
        """Affiche les sprites en utilisant une caméra

        :param self: Caméra à utiliser
        :type self: Camera, EditorCamera
        :param freeze: Désactiver l'actualisation des sprites
        :type freeze: bool
        """

        rect = Game.surface.get_bounding_rect()
        rect.width += 200
        rect.x -= self.last_x + 100
        Game.display_rect = rect
        for sprite in TileManager.background_blocks_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_DEBUG_RECTS:
                    pygame.draw.rect(Game.surface, (0, 0, 255), self.apply(sprite), width=2)
        for sprite in TileManager.entity_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_DEBUG_RECTS:
                    pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        for sprite in Game.player_group:
            self.sprite_count += 1
            if not freeze:
                sprite.update()
            Game.surface.blit(sprite.image, self.apply(sprite))
            if Game.DISPLAY_DEBUG_RECTS:
                pygame.draw.rect(Game.surface, (0, 255, 0), self.apply(sprite), width=2)
        for sprite in TileManager.environment_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
                self.sprite_count += 1
                if Game.DISPLAY_DEBUG_RECTS:
                    pygame.draw.rect(Game.surface, (255, 0, 0), self.apply(sprite), width=2)
        for sprite in TileManager.deadly_object_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.foreground_blocks_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))
        for sprite in TileManager.interactible_blocks_group:
            if sprite.rect.colliderect(rect):
                if not freeze:
                    sprite.update()
                Game.surface.blit(sprite.image, self.apply(sprite))

    @classmethod
    def generate_clouds(cls):
        """Génère les nuages"""
        from dpt.engine.gui.Cloud import Cloud
        xpos = 10
        for i in range(3):
            speed = randrange(1, 6)
            ypos = randrange(10, Game.TILESIZE + 11, Game.TILESIZE // 2)

            c = Cloud(xpos, ypos, speed)

            xpos += math.floor(3 * c.rect.width / 4)

            if xpos > Game.SCREEN_WIDTH - 50:
                xpos = 10

    @classmethod
    def update_clouds(cls):
        """Actualise les nuages"""

        TileManager.clouds_group.update()
        TileManager.clouds_group.draw(Game.surface)

        from dpt.engine.gui.Cloud import Cloud
        for cloud in cls.clouds_group:
            cloud.rect.x += cls.camera.last_x - cls.clouds_last_x
            if cloud.rect.midright[0] <= 0:
                cloud.kill()
                del cloud
                speed = randrange(1, 6)
                ypos = randrange(10, Game.TILESIZE + 11, Game.TILESIZE // 2)
                Cloud(Game.surface.get_size()[0], ypos, speed)

        cls.clouds_last_x = cls.camera.last_x


class Camera:
    def __init__(self, width, height):
        """Crée une nouvelle caméra

        :param width: Largeur de l'écran (Tile)
        :type width: int
        :param height: Hauteur de l'écran (Tile)
        :type height: int

        :rtype: Camera
        """

        self.userConfirm = True
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("Camera")
        self.x = 0
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        """Applique la translation de défilement

        :param entity: Surface à déplacer
        :type entity: pygame.Surface

        :return: Surface déplacée
        :rtype: pygame.Surface
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, target, freeze=False):
        """Actualisation de la caméra

        :param target: Objectif
        :type target: pygame.sprite.Sprite
        :param freeze: Désactiver l'actualisation des sprites
        :type freeze: bool
        """
        self.sprite_count = 0
        self.target = target
        self.x = -target.rect.x + int(Game.surface.get_size()[0] / 2)

        calcul = (self.width * Game.TILESIZE) - Game.surface.get_size()[0]
        self.x = min(0, self.last_x, self.x)
        self.x = max(-calcul, self.x)
        self.camera = pygame.Rect(self.x, 0, self.width, self.height)
        TileManager.display_sprites(self, freeze)
        self.last_x = self.x

        TileManager.display_cam_info()


class EditorCamera:
    def __init__(self, width, height):
        """Crée une nouvelle caméra d'éditeur

        :param width: Largeur de l'écran (Tile)
        :type width: int
        :param height: Hauteur de l'écran (Tile)
        :type height: int

        :rtype: EditorCamera
        """
        self.camera = None
        self.width = width
        self.height = height
        self.log = Game.get_logger("EditorCamera")
        self.x = 0
        self.last_x = 0
        self.sprite_count = 0

    def apply(self, entity):
        """Applique la translation de défilement

        :param entity: Surface à déplacer
        :type entity: pygame.Surface

        :return: Surface déplacée
        :rtype: pygame.Surface
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, target, freeze=False):
        """Actualisation de la caméra

        :param target: Objectif
        :type target: pygame.sprite.Sprite
        :param freeze: Désactiver l'actualisation des sprites
        :type freeze: bool
        """
        self.sprite_count = 0
        self.target = target
        self.x = -target.rect.x + int(Game.surface.get_size()[0] / 2)
        self.x = min(0, self.x)
        self.camera = pygame.Rect(self.x, 0, self.width, self.height)
        TileManager.display_sprites(self, freeze)
        self.last_x = self.x

        TileManager.display_cam_info()

    def enable_grid(self):
        """Ajoute la grille de placement"""
        for x in range(self.last_x, Game.surface.get_size()[0], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (x, 0), (x, Game.surface.get_size()[1]))
        for y in range(0, Game.surface.get_size()[1], Game.TILESIZE):
            pygame.draw.line(Game.surface, (220, 220, 220), (0, y), (Game.surface.get_size()[0], y))
