package fr.dwightstudio.dpt.game.graphics;

import fr.dwightstudio.dpt.engine.graphics.render.Shader;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.VBO;

public class Tile {
    private final Texture texture;
    private final VBO vbo;
    private Shader shader = null;

    public Tile(int x, int y, int size, Texture texture) {
        this.texture = texture;
        float[] vertices = new float[] {
                // Position             // Color
                672.0f, 0.0f, 0.0f,      1.0f, 0.0f, 0.0f, 1.0f, // BOTTOM RIGHT 0
                0.0f, 672.0f, 0.0f,      0.0f, 1.0f, 0.0f, 1.0f, // TOP LEFT     1
                672.0f, 672.0f, 0.0f,     0.0f, 0.0f, 1.0f, 1.0f, // TOP RIGHT    2
                0.0f, 0.0f, 0.0f,       1.0f, 1.0f, 0.0f, 1.0f  // BOTTOM LEFT  3
        };
        int[] indices = new int[]{
                // Two triangles
                2, 1, 0,
                0, 1, 3
        };
        this.vbo = new VBO(vertices, indices);
        // Assigning this variables to null to free up some memory
        vertices = null;
        indices = null;
    }

    public void render() {
        texture.bind();
        vbo.render();
        texture.unbind();
    }
}
