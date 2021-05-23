package fr.dwightstudio.dpt.engine.utils;

public class Time {

    private static Time instance;
    public static float dTime;
    public static final float startTime = System.nanoTime();

    public static float getDeltaTime() {
        return (float) ((System.nanoTime() - startTime) * 1E-9);
    }

    public static void setDTime(float dt) {
        dTime = dt;
    }

    public static float getDTime() {
        return dTime;
    }
}
