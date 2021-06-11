package fr.dwightstudio.dpt.engine.inputs;

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