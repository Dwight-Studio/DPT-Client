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

        # Initialisation du TileManager
        TileEditor.in_editor = True
        if not TileManager.load_level(level):
            return False

        # Ajout du bouton d'éditeur
        from dpt.engine.gui.menu.button import Button
        Game.button = Button(0, Game.surface.get_size()[1] - 50, 127, 46, RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_OUT"), pushed_image=RessourceLoader.get("dpt.images.gui.buttons.BTN_GREEN_RECT_IN"), text="Jouer")

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
