package fr.dwightstudio.dpt.game.graphics;

import fr.dwightstudio.dpt.engine.graphics.Texture;
import fr.dwightstudio.dpt.engine.graphics.TexturedVBO;

public class Tile {
    private final int size;
    private final int x;
    private final int y;
    private final Texture texture;
    private final TexturedVBO vbo;

    public Tile(int x, int y, int size, Texture texture) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.texture = texture;
        float[] vertices = new float[] {
                x, y,               // TOP LEFT     0
                x + size, y,        // TOP RIGHT    1
                x + size, y + size, // BOTTOM RIGHT 2
                x, y + size         // BOTTOM LEFT  3
        };
        float[] textureCoordinates = new float[] {
                0, 0, // TOP LEFT       0
                1, 0, // TOP RIGHT      1
                1, 1, // BOTTOM RIGHT   2
                0, 1 // BOTTOM LEFT     3
        };
        int[] indices = new int[] {
                // Two triangles
                0, 1, 2,
                2, 3, 0
        };
        this.vbo = new TexturedVBO(vertices, textureCoordinates, indices);
    }

    public void render() {
        texture.bind();
        vbo.render();
    }
}
