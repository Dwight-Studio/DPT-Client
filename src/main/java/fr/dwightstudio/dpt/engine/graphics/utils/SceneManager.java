/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
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
     * Change the current Scene to the specified Scene
     *
     * @param scene a Scene
     */
    public static void changeScene(Scene scene) {
        currentScene = scene;
        currentScene.init();
        currentScene.start();
    }

    /**
     * @return the current shown Scene
     */
    public static Scene getCurrentScene() {
        return currentScene;
    }
}
