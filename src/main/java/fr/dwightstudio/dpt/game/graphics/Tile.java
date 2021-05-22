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
                x, y,
                x + size, y,
                x + size, y + size,
                x, y + size,
                x + size, y + size,
                x, y
        };
        float[] textureCoordinates = new float[] {
                0, 0,
                1, 0,
                1, 1,
                0, 1,
                1, 1,
                0, 0
        };
        this.vbo = new TexturedVBO(vertices, textureCoordinates);
    }

    public void render() {
        texture.bind();
        vbo.render();
    }
}
