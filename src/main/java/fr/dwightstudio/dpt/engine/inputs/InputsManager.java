package fr.dwightstudio.dpt.engine.inputs;

import org.lwjgl.glfw.GLFWCharCallbackI;
import org.lwjgl.glfw.GLFWCharModsCallbackI;
import org.lwjgl.glfw.GLFWKeyCallbackI;

import static org.lwjgl.glfw.GLFW.*;

public class InputsManager {

    public GLFWCharModsCallbackI keyCallback = (window, codepoint, mods) -> {
        if (codepoint == GameInputs.MOVE_RIGHT.getKey()) {
            System.out.println("MOVE_RIGHT");
        }
        if (codepoint == GameInputs.MOVE_LEFT.getKey()) {
            System.out.println("MOVE_LEFT");
        }
        if (codepoint == GameInputs.JUMP.getKey()) {
            System.out.println("JUMP");
        }
        if (codepoint == GameInputs.INTERACT.getKey()) {
            System.out.println("INTERACT");
        }
    };

    // Default Singleton class
    private InputsManager() {}

    private static final InputsManager instance = new InputsManager();

    public static InputsManager getInstance() {
        return instance;
    }
}
