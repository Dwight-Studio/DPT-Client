package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.levels.MainLevel;

import java.util.logging.Level;

public class SceneManager {
    private static Scene currentScene;

    public static void changeScene(int sceneID) {
        GameLogger.logger.log(Level.INFO, "Changing to scene : {0}", new Object[] {sceneID});
        switch (sceneID) {
            case 0 :
                currentScene = new MainLevel();
                currentScene.init();
                currentScene.start();
                break;
            default:
                GameLogger.logger.log(Level.WARNING, "The scene with id : {0} cannot be found.", new Object[] {sceneID});
        }
    }

    public static Scene getCurrentScene() {
        return currentScene;
    }
}
