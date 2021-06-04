package fr.dwightstudio.dpt.engine.inputs;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import org.joml.Vector2f;
import org.lwjgl.glfw.GLFWCursorPosCallbackI;
import org.lwjgl.glfw.GLFWMouseButtonCallbackI;
import org.lwjgl.glfw.GLFWScrollCallbackI;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;

public class MouseListener {

    private static MouseListener instance;

    private static float xPos;
    private static float yPos;
    private static final boolean[] mouseButtons = new boolean[3];
    private static float scrollX;
    private static float scrollY;

    private MouseListener() {
        xPos = 0.0F;
        yPos = 0.0F;
        scrollX = 0.0F;
        scrollY = 0.0F;
    }

    public static GLFWMouseButtonCallbackI mouseButtonCallback = (window, button, action, mods) -> {
        if (button < mouseButtons.length) {
            mouseButtons[button] = action == GLFW_PRESS;
        }
        Button.checkClickAll();
    };

    public static GLFWCursorPosCallbackI cursorPosCallback = (window, xpos, ypos) -> {
        xPos = (float) xpos;
        yPos = (float) Math.abs(ypos - GLFWWindow.getHeight());
    };

    public static GLFWScrollCallbackI mouseScrollCallback = (window, xoffset, yoffset) -> {
        scrollX = (float) xoffset;
        scrollY = (float) yoffset;
    };

    public static void endFrame() {
        scrollX = 0.0F;
        scrollY = 0.0F;
    }

    public static Vector2f getCursorPos() {
        return new Vector2f(xPos, yPos);
    }

    public static boolean isButtonPressed(int button) {
        if (button < mouseButtons.length) {
            return mouseButtons[button];
        }
        return false;
    }

    public static float getScrollX() {
        return scrollX;
    }

    public static float getScrollY() {
        return scrollY;
    }
}
