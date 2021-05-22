package fr.dwightstudio.dpt.engine.inputs;

import org.lwjgl.glfw.GLFWKeyCallbackI;

import java.awt.event.KeyListener;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class KeyboardListener {

    private static final boolean[] keys = new boolean[350];

    private KeyboardListener() {}

    public static GLFWKeyCallbackI keyCallback = (window, key, scancode, action, mods) -> {
        if (key < keys.length) {
            keys[key] = action == GLFW_PRESS;
        }
    };

    public static boolean isKeyPressed(int key) {
        if (key < keys.length) {
            return keys[key];
        }
        return false;
    }
}