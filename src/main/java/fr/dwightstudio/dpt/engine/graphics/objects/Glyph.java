package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

public class Glyph {

    private final int width;
    private final int height;
    private final int x;
    private final int y;
    private final float advance;

    public Glyph(int width, int height, int x, int y, float advance) {
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
        this.advance = advance;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public float getAdvance() {
        return advance;
    }

    public Vector2f[] getTextureCoords(FontAtlas fontAtlas) {
        float top = (y + height) / (float) fontAtlas.getTexture().getHeight();
        float right = (x + width) / (float) fontAtlas.getTexture().getWidth();
        float left = x / (float) fontAtlas.getTexture().getWidth();
        float bottom = y / (float) fontAtlas.getTexture().getHeight();

        return new Vector2f[] {
                new Vector2f(right, bottom),
                new Vector2f(right, top),
                new Vector2f(left, top),
                new Vector2f(left, bottom),
        };
    }

}
