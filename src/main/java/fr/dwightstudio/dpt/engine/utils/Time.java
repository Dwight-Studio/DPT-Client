package fr.dwightstudio.dpt.engine.utils;

import static org.lwjgl.glfw.GLFW.glfwGetTime;

public class Time {

    public static float dTime;

    /**
     * @return the delta time
     */
    public static float getDeltaTime() {
        return (float) glfwGetTime();
    }

    /**
     * Set the delta time
     *
     * @param dt the new delta time value
     */
    public static void setDTime(float dt) {
        dTime = dt;
    }

    /**
     * @return the delta time
     */
    public static float getDTime() {
        return dTime;
    }
}
