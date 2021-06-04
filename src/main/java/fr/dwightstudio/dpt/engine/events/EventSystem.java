package fr.dwightstudio.dpt.engine.events;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.glfw.GLFW.*;

public class EventSystem implements Runnable {
    private final long window;

    protected static List<EventHandler> eventHandlers = new ArrayList<>();

    public EventSystem(long window) {
        this.window = window;
    }

    @Override
    public void run() {
        GameLogger.getLogger("EventSystem").debug("Event System Thread started");
        glfwSetKeyCallback(window, KeyboardListener.keyCallback); // Setup a key callback
        glfwSetMouseButtonCallback(window, MouseListener.mouseButtonCallback); // Setup a mouse buttons callback
        glfwSetCursorPosCallback(window, MouseListener.cursorPosCallback); // Setup a mouse cursor callback
        glfwSetScrollCallback(window, MouseListener.mouseScrollCallback); // Setup a mouse scroll wheel callback

        while (!glfwWindowShouldClose(GLFWWindow.getWindow())) {
            for (EventHandler eventHandler : eventHandlers) {
                eventHandler.update(); // This will update
            }
        }
    }
}
