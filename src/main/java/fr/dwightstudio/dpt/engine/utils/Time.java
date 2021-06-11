/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.utils;

import static org.lwjgl.glfw.GLFW.glfwGetTime;

public class Time {

    public static float dTime;

    /**
     * @return the delta time
     */
    public static float getDeltaTime() {
        return (float) glfwGetTime();
    }

    /**
     * Set the delta time
     *
     * @param dt the new delta time value
     */
    public static void setDTime(float dt) {
        dTime = dt;
    }

    /**
     * @return the delta time
     */
    public static float getDTime() {
        return dTime;
    }
}
