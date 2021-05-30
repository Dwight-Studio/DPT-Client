package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.render.Camera;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.inputs.GameInputs;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.primitives.Surface;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import org.joml.Vector2f;

public class MainScene extends Scene {

    private GameObject tiles;

    public MainScene() {

    }

    @Override
    public void init() {
        camera = new Camera(new Vector2f());
        tiles = new GameObject("tiles", 0);
        ResourceManager.load("./src/main/resources/textures/test.png", Texture.class);
        tiles.addComponent(new Surface(0, 0, 64, 64, new Color(1, 0, 0, 1)));
        tiles.addComponent(new Surface(100, 100, 64, 64, new Color(0, 1, 0, 1)));
        tiles.addComponent(new Surface(200, 200, 64, 64, ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        setBackgroundColor(new Color(1.0f, 1.0f, 1.0f, 0.0f));
        this.addGameObject(tiles);
    }

    @Override
    public void update(float dt) {
        if (KeyboardListener.isKeyPressed(GameInputs.JUMP.getKey())) {
            SceneManager.changeScene(1);
        }
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }

        renderer.render();
    }
}
