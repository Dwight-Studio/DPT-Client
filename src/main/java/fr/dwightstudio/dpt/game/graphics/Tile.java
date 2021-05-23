package fr.dwightstudio.dpt.game.graphics;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.VBO;

public class Tile {
    private final Texture texture;
    private final Color color;
    private final VBO vbo;

    public Tile(int x, int y, int size, Color color) {
        this.texture = null;
        this.color = null;
        float[] vertexArray = new float[] {
                // Position             // Color
                x + size, y, 0,         color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(), // BOTTOM RIGHT 0
                x, y + size, 0,         color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(), // TOP LEFT     1
                x + size, y + size, 0,  color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(), // TOP RIGHT    2
                x, y, 0,                color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha()  // BOTTOM LEFT  3
        };
        int[] elementArray = new int[]{
                // Two triangles
                2, 1, 0,
                0, 1, 3
        };
        this.vbo = new VBO(vertexArray, elementArray);
        // Assigning this variables to null to free up some memory
        vertexArray = null;
        elementArray = null;
    }

    public void render() {
        if (texture != null) texture.bind();
        vbo.render();
        if (texture != null) texture.unbind();
    }

    public Color getColor() {
        return color;
    }

    public Texture getTexture() {
        return texture;
    }
}
