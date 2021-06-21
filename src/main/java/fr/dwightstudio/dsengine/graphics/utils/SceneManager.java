/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.utils;

import fr.dwightstudio.dsengine.scripting.Scene;

import java.util.ArrayList;
import java.util.List;

public class SceneManager {
    private static Scene currentScene;
    private static List<Scene> scenes = new ArrayList<>();

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

    public static void updateScenes(double dt) {
        for (Scene scene : scenes) {
            scene.update(dt);
        }
    }

    public static void add(Scene scene) {
        scenes.add(scene);
    }

    public static void remove(Scene scene) {
        scenes.remove(scene);
    }
}
