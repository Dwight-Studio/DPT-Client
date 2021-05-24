package fr.dwightstudio.dpt.engine.scripting;

import java.util.ArrayList;
import java.util.List;

public abstract class Scene {

    private boolean isRunning = false;
    public List<GameObject> gameObjects = new ArrayList<>();

    public Scene() {

    }

    public void init() {

    }

    public void start() {
        for (GameObject gameObject : gameObjects) {
            gameObject.init();
        }
    }

    public abstract void update(float dt);

    public void addGameObject(GameObject gameObject) {
        if (!isRunning) {
            gameObjects.add(gameObject);
        } else {
            gameObjects.add(gameObject);
            gameObject.init();
        }
    }
}
