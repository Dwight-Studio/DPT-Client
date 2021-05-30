package fr.dwightstudio.dpt.engine.scripting;

import fr.dwightstudio.dpt.engine.graphics.render.Camera;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.renderers.Renderer;
import org.joml.Vector2f;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL11.glClearColor;

public abstract class Scene {

    protected Camera camera;
    private boolean isRunning = false;
    protected List<GameObject> gameObjects = new ArrayList<>();
    protected Renderer renderer = new Renderer();

    public Scene() {
        this.camera = new Camera(new Vector2f());
        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    }

    public void init() {

    }

    public void start() {
        for (GameObject gameObject : gameObjects) {
            gameObject.init();
            renderer.addGameObject(gameObject);
        }
    }

    public abstract void update(float dt);

    public void addGameObject(GameObject gameObject) {
        if (!isRunning) {
            gameObjects.add(gameObject);
        } else {
            gameObjects.add(gameObject);
            gameObject.init();
            renderer.addGameObject(gameObject);
        }
    }

    public void setBackgroundColor(Color color) {
        glClearColor(color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha());
    }

    public Camera getCamera() {
        return this.camera;
    }
}
