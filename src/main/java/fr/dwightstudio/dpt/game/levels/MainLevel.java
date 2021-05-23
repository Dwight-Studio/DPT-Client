package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.components.Tile;

public class MainLevel extends Scene {

    private GameObject tiles;

    public MainLevel() {

    }

    @Override
    public void init() {
        this.tiles = new GameObject("tiles");
        this.tiles.addComponent(new Tile(0, 0, 32, new Color(1, 0, 0)));
        this.tiles.addComponent(new Tile(100, 100, 32, TextureLoader.loadTexture("./src/ressources/textures/test.png")));
        this.addGameObject(this.tiles);
    }

    @Override
    public void update(float dt) {
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }
    }
}
