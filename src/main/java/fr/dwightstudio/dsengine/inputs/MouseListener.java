/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.inputs;

import fr.dwightstudio.dsengine.graphics.GLFWWindow;
import fr.dwightstudio.dsengine.graphics.gui.Button;
import fr.dwightstudio.dsengine.graphics.utils.SceneManager;
import org.joml.Vector2f;
import org.joml.Vector4f;
import org.lwjgl.glfw.GLFWCursorPosCallbackI;
import org.lwjgl.glfw.GLFWMouseButtonCallbackI;
import org.lwjgl.glfw.GLFWScrollCallbackI;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class MouseListener {

    private static float xPos;
    private static float yPos;
    private static final boolean[] mouseButtons = new boolean[3];
    private static float scrollX;
    private static float scrollY;

    public static GLFWMouseButtonCallbackI mouseButtonCallback = (window, button, action, mods) -> {
        if (button < mouseButtons.length) {
            mouseButtons[button] = action == GLFW_PRESS;
        }
        Button.checkClickAll();
    };

    public static GLFWCursorPosCallbackI cursorPosCallback = (window, xpos, ypos) -> {
        xPos = (float) xpos;
        yPos = (float) Math.abs(ypos - GLFWWindow.getHeight());
        Button.checkHoverAll();
    };

    public static GLFWScrollCallbackI mouseScrollCallback = (window, xoffset, yoffset) -> {
        scrollX = (float) xoffset;
        scrollY = (float) yoffset;
    };

    /**
     * @return cursor X and Y screen coordinates
     */
    public static Vector2f getCursorPos() {
        return new Vector2f(xPos, yPos);
    }

    /**
     * @return cursor X and Y orthonormal coordinates
     */
    public static Vector2f getOrthoCursorPos() {
        float currentX = getCursorPos().x;
        float currentY = getCursorPos().y;
        currentX = (currentX / (float) GLFWWindow.getWidth()) * 2.0f - 1.0f;
        currentY = (currentY / (float) GLFWWindow.getHeight()) * 2.0f - 1.0f;
        Vector4f tmpX = new Vector4f(currentX, 0, 0, 1);
        Vector4f tmpY = new Vector4f(0, currentY, 0, 1);
        tmpX.mul(SceneManager.getCurrentScene().getCamera().getInverseProjectionMatrix()).mul(SceneManager.getCurrentScene().getCamera().getInverseViewMatrix());
        tmpY.mul(SceneManager.getCurrentScene().getCamera().getInverseProjectionMatrix()).mul(SceneManager.getCurrentScene().getCamera().getInverseViewMatrix());
        currentX = tmpX.x;
        currentY = tmpY.y;
        return new Vector2f(currentX, currentY);
    }

    /**
     * @param button the button code
     * @return wheither the button is pressed or not
     */
    public static boolean isButtonPressed(int button) {
        if (button < mouseButtons.length) {
            return mouseButtons[button];
        }
        return false;
    }

    /**
     * @return the scroll value in the X axis
     */
    public static float getScrollX() {
        return scrollX;
    }

    /**
     * @return the scroll value in the Y axis
     */
    public static float getScrollY() {
        return scrollY;
    }
}
