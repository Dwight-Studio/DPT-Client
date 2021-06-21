/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.inputs;

import org.lwjgl.glfw.GLFWKeyCallbackI;

import java.awt.event.KeyListener;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class KeyboardListener {

    private static final boolean[] keys = new boolean[350];

    public static GLFWKeyCallbackI keyCallback = (window, key, scancode, action, mods) -> {
        if (key < keys.length) {
            keys[key] = action == GLFW_PRESS;
        }
    };

    /**
     * @param key the key code
     * @return wheither the specified key is pressed or not
     */
    public static boolean isKeyPressed(int key) {
        if (key < keys.length) {
            return keys[key];
        }
        return false;
    }
}