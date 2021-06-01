package fr.dwightstudio.dpt.engine.utils;

import static org.lwjgl.glfw.GLFW.glfwGetTime;

public class Time {

    public static float dTime;

    public static float getDeltaTime() {
        return (float) glfwGetTime();
    }

    public static void setDTime(float dt) {
        dTime = dt;
    }

    public static float getDTime() {
        return dTime;
    }
}
