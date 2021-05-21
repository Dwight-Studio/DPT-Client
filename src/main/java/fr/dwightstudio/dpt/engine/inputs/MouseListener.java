package fr.dwightstudio.dpt.engine.inputs;

import org.lwjgl.glfw.GLFWCursorPosCallbackI;
import org.lwjgl.glfw.GLFWMouseButtonCallbackI;
import org.lwjgl.glfw.GLFWScrollCallbackI;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class MouseListener {

    private static MouseListener instance;

    private float xPos;
    private float yPos;
    private final boolean[] mouseButtons = new boolean[3];
    private float scrollX;
    private float scrollY;

    private MouseListener() {
        this.xPos = 0.0F;
        this.yPos = 0.0F;
        this.scrollX = 0.0F;
        this.scrollY = 0.0F;
    }

    public static MouseListener getInstance() {
        if (MouseListener.instance == null) {
            MouseListener.instance = new MouseListener();
        }

        return MouseListener.instance;
    }

    public static GLFWMouseButtonCallbackI mouseButtonCallback = (window, button, action, mods) -> {
        if (button < getInstance().mouseButtons.length) {
            getInstance().mouseButtons[button] = action == GLFW_PRESS;
        }
    };

    public static GLFWCursorPosCallbackI cursorPosCallback = (window, xpos, ypos) -> {
        getInstance().xPos = (float) xpos;
        getInstance().yPos = (float) ypos;
    };

    public static GLFWScrollCallbackI mouseScrollCallback = (window, xoffset, yoffset) -> {
        getInstance().scrollX = (float) xoffset;
        getInstance().scrollY = (float) yoffset;
    };

    public static void endFrame() {
        getInstance().scrollX = 0.0F;
        getInstance().scrollY = 0.0F;
    }

    public static float getX() {
        return getInstance().xPos;
    }

    public static float getY() {
        return getInstance().yPos;
    }

    public static boolean isButtonPressed(int button) {
        if (button < getInstance().mouseButtons.length) {
            return getInstance().mouseButtons[button];
        }
        return false;
    }

    public static float getScrollX() {
        return getInstance().scrollX;
    }

    public static float getScrollY() {
        return getInstance().scrollY;
    }
}
