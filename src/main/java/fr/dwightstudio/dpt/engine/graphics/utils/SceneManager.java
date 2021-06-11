/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import fr.dwightstudio.dpt.game.levels.MainScene;
import fr.dwightstudio.dpt.game.levels.TestScene;

import java.text.MessageFormat;

public class SceneManager {
    private static Scene currentScene;

    /**
     * Change the current Scene to the Scene ID
     *
     * @param sceneID a Scene ID
     */
    // TODO: The Scene system should be modified to input a Scene instead of an ID
    public static void changeScene(int sceneID) {
        GameLogger.getLogger("SceneManager").info(MessageFormat.format("Changing to scene : {0}", sceneID));
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
            default -> GameLogger.getLogger("SceneManager").warn(MessageFormat.format("The scene with id : {0} cannot be found.", sceneID));
        }
    }

    /**
     * @return the current shown Scene
     */
    public static Scene getCurrentScene() {
        return currentScene;
    }
}
