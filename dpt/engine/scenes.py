from dpt.game import Game


class Scenes:
    @classmethod
    def editor(cls, level):
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Gestion des ressources
        RessourceLoader.unload()
        RessourceLoader.add_pending("dpt.images.gui.buttons.BTN_GREEN_RECT_*")
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_out")
        RessourceLoader.add_pending("dpt.images.gui.buttons.btn_checkbox_in")

        # Initialisation du TileManager
        TileEditor.in_editor = True
        if not TileManager.load_level(level):
            return False

        # Ajout du bouton d'éditeur
        from dpt.engine.gui.menu.button import Button
        Game.gui = {"editor_button": Button(0, Game.surface.get_size()[1] - 50, 127, 46,
                                            RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"),
                                            pushed_image=RessourceLoader.get(
                                                "dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Jouer")}

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def level(cls, level):
        from dpt.engine.loader import RessourceLoader
        from dpt.engine.tileManager import TileManager
        from dpt.engine.gui.editor.tileEditor import TileEditor

        # Gestion des ressources
        RessourceLoader.unload()

        # Initialisation du TileManager
        TileEditor.in_editor = False
        if not TileManager.load_level(level):
            return False

        # Loops
        from dpt.engine.mainLoop import level_loop
        Game.loop = level_loop
        return True

    @classmethod
    def pause(cls):
        # Loops
        from dpt.engine.mainLoop import pause_loop
        Game.loop = pause_loop
        return True

    @classmethod
    def main_menu(cls):
        from dpt.engine.loader import RessourceLoader

        # Gestion des ressources
        RessourceLoader.unload()
        RessourceLoader.add_pending("dpt.images.environment.background.default_sky")
        RessourceLoader.add_pending("dpt.images.gui.ui.UI_WINDOW_*")
        RessourceLoader.add_pending("dpt.images.gui.buttons.*")
        RessourceLoader.add_pending("dpt.images.dpt")
        RessourceLoader.add_pending("dpt.sounds.musics.story_time")
        RessourceLoader.load()

        # Ajout du GUI
        Game.gui = {}

        # Loops
        from dpt.engine.mainLoop import main_menu_loop
        Game.loop = main_menu_loop
        return True
