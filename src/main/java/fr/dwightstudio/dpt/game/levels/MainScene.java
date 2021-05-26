package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.utils.RessourceManager;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.inputs.GameInputs;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.components.Tile;

public class MainScene extends Scene {

    private GameObject tiles;

    public MainScene() {

    }

    @Override
    public void init() {
        this.tiles = new GameObject("tiles");
        this.tiles.addComponent(new Tile(0, 0, 32, RessourceManager.getTexture("./src/main/resources/textures/test.png")));
        this.addGameObject(this.tiles);
    }

    @Override
    public void update(float dt) {
        if (KeyboardListener.isKeyPressed(GameInputs.JUMP.getKey())) {
            SceneManager.changeScene(1);
        }
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }
    }
}
