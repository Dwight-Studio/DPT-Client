package fr.dwightstudio.dpt.engine.graphics.render;

public class Color {

    private final float red;
    private final float green;
    private final float blue;
    private final float alpha;

    public Color(float r, float g, float b) {
        this.red = r;
        this.green = g;
        this.blue = b;
        this.alpha = 1;
    }

    public Color(float r, float g, float b, float a) {
        this.red = r;
        this.green = g;
        this.blue = b;
        this.alpha = a;
    }

    public float getRed() {
        return red;
    }

    public float getGreen() {
        return green;
    }

    public float getBlue() {
        return blue;
    }

    public float getAlpha() {
        return alpha;
    }
}
