package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.components.Tile;

public class TestScene extends Scene {

    private GameObject tiles;

    public TestScene() {

    }

    @Override
    public void init() {
        this.tiles = new GameObject("tiles");
        this.tiles.addComponent(new Tile(100, 100, 32, new Color(0, 1, 1, 1)));
        this.addGameObject(tiles);
    }

    @Override
    public void update(float dt) {
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }
    }
}
