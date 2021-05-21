package fr.dwightstudio.dpt.engine.inputs;

import org.lwjgl.glfw.GLFWKeyCallbackI;

import java.awt.event.KeyListener;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class KeyboardListener {

    private static KeyboardListener instance = null;
    private final boolean[] keys = new boolean[350];

    private KeyboardListener() {}

    public static KeyboardListener getInstance() {
        if (KeyboardListener.instance == null) {
            KeyboardListener.instance = new KeyboardListener();
        }

        return KeyboardListener.instance;
    }

    public static GLFWKeyCallbackI keyCallback = (window, key, scancode, action, mods) -> {
        if (key < getInstance().keys.length) {
            getInstance().keys[key] = action == GLFW_PRESS;
        }
    };

    public static boolean isKeyPressed(int key) {
        if (key < getInstance().keys.length) {
            return getInstance().keys[key];
        }
        return false;
    }
}