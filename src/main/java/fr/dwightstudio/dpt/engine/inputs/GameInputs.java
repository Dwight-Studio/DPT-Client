package fr.dwightstudio.dpt.engine.inputs;

import static org.lwjgl.glfw.GLFW.*;

public enum GameInputs {
    MOVE_RIGHT('d'),
    MOVE_LEFT('q'),
    JUMP(' '),
    INTERACT('e');

    private int glfwKey;

    GameInputs(int glfwKey) {
        this.glfwKey = glfwKey;
    }

    public int getKey() {
        return this.glfwKey;
    }

    public void setKey(int key) {
        this.glfwKey = key;
    }
}
