package fr.dwightstudio.dpt.engine.inputs;

import static org.lwjgl.glfw.GLFW.*;

public enum GameInputs {
    MOVE_RIGHT(GLFW_KEY_D),
    MOVE_LEFT(GLFW_KEY_Q),
    JUMP(GLFW_KEY_SPACE),
    INTERACT(GLFW_KEY_E);

    private int glfw_Key;

    GameInputs(int glfw_Key) {
        this.glfw_Key = glfw_Key;
    }

    public int get_key() {
        return this.glfw_Key;
    }

    public void set_key(int key) {
        this.glfw_Key = key;
    }
}
