package fr.dwightstudio.dpt.engine.scripting;

import fr.dwightstudio.dpt.engine.graphics.objects.Camera;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.renderers.RendererHelper;
import org.joml.Vector2f;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL11.glClearColor;

public abstract class Scene {

    protected Camera camera;
    private boolean isRunning = false;
    protected List<GameObject> gameObjects = new ArrayList<>();
    protected RendererHelper rendererHelper = new RendererHelper();

    /**
     * Create a new Scene
     */
    public Scene() {
        this.camera = new Camera(new Vector2f());
        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    }

    /**
     * Initialize the Scene
     * This will initialize all the GameObject
     */
    public void start() {
        for (GameObject gameObject : gameObjects) {
            gameObject.init();
            rendererHelper.addGameObject(gameObject);
        }
    }

    public void init() {

    }

    public abstract void update(float dt);

    /**
     * Add a GameObject to the Scene
     *
     * @param gameObject the GameObject to add
     */
    public void addGameObject(GameObject gameObject) {
        if (!isRunning) {
            gameObjects.add(gameObject);
        } else {
            gameObjects.add(gameObject);
            gameObject.init();
            rendererHelper.addGameObject(gameObject);
        }
    }

    /**
     * Set the background color of the Scene
     *
     * @param color a color
     */
    public void setBackgroundColor(Color color) {
        glClearColor(color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha());
    }

    /**
     * @return the camera used in the Scene
     */
    public Camera getCamera() {
        return this.camera;
    }
}
