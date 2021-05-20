package fr.dwightstudio.dpt.engine.inputs;

import org.lwjgl.glfw.GLFWKeyCallbackI;

import static org.lwjgl.glfw.GLFW.*;

public class InputsManager {

    public GLFWKeyCallbackI key_callback = (window, key, scancode, action, mods) -> {
        if ( key == GLFW_KEY_ESCAPE && action == GLFW_RELEASE ) {
            glfwSetWindowShouldClose(window, true); // We will detect this in the rendering loop
        }
    };

    private InputsManager(){}

    private static final InputsManager instance = new InputsManager();

    public static InputsManager getInstance() {
        return instance;
    }
}
