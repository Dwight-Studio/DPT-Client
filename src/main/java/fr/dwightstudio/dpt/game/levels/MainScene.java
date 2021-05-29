package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
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
        this.tiles = new GameObject("tiles", 0);
        ResourceManager.load("./src/main/resources/textures/test.png", "texture");
        this.tiles.addComponent(new Tile(0, 0, 32, ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        setBackgroundColor(new Color(1.0f, 1.0f, 1.0f, 0.0f));
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
