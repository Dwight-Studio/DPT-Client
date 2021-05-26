package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.levels.MainScene;
import fr.dwightstudio.dpt.game.levels.TestScene;

import java.text.MessageFormat;
import java.util.logging.Level;

public class SceneManager {
    private static Scene currentScene;

    public static void changeScene(int sceneID) {
        GameLogger.getLogger().info(MessageFormat.format("Changing to scene : {0}", sceneID));
        switch (sceneID) {
            case 0 -> {
                currentScene = new MainScene();
                currentScene.init();
                currentScene.start();
            }
            case 1 -> {
                currentScene = new TestScene();
                currentScene.init();
                currentScene.start();
            }
            default -> GameLogger.getLogger().warn(MessageFormat.format("The scene with id : {0} cannot be found.", sceneID));
        }
    }

    public static Scene getCurrentScene() {
        return currentScene;
    }
}
