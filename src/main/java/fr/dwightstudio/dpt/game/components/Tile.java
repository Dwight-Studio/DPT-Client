package fr.dwightstudio.dpt.game.components;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.VBO;
import fr.dwightstudio.dpt.engine.scripting.Component;

public class Tile extends Component {
    private final Texture texture;
    private final Color color;
    private final VBO vbo;

    public Tile(int x, int y, int size, Color color) {
        this.texture = null;
        this.color = color;
        float[] vertexArray = new float[] {
                // Position             // Color                                                                // Texture coordinates
                x + size, y, 0,         color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(),    1, 0,   // BOTTOM RIGHT 0
                x, y + size, 0,         color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(),    0, 1,   // TOP LEFT     1
                x + size, y + size, 0,  color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(),    1, 1,   // TOP RIGHT    2
                x, y, 0,                color.getRed(), color.getGreen(), color.getBlue(), color.getAlpha(),    0, 0    // BOTTOM LEFT  3
        };
        int[] elementArray = new int[]{
                // Two triangles
                2, 1, 0,
                0, 1, 3
        };
        this.vbo = new VBO(vertexArray, elementArray);
    }

    public Tile(int x, int y, int size, Texture texture) {
        this.texture = texture;
        this.color = null;
        float[] vertexArray = new float[] {
                // Position             // Color       // Texture coordinates
                x + size, y, 0,         0, 0, 0, 1,    1, 1,   // BOTTOM RIGHT 0
                x, y + size, 0,         0, 0, 0, 1,    0, 0,   // TOP LEFT     1
                x + size, y + size, 0,  0, 0, 0, 1,    1, 0,   // TOP RIGHT    2
                x, y, 0,                0, 0, 0, 1,    0, 1    // BOTTOM LEFT  3
        };
        int[] elementArray = new int[]{
                // Two triangles
                2, 1, 0,
                0, 1, 3
        };
        this.vbo = new VBO(vertexArray, elementArray);
    }

    public Color getColor() {
        return color;
    }

    public Texture getTexture() {
        return texture;
    }

    @Override
    public void update(float dt) {
        if (texture != null) {
            texture.bind();
            vbo.render(true, false);
        } else if (color != null) {
            vbo.render(false, true);
        }
        if (texture != null) texture.unbind();
    }
}
