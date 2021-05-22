package fr.dwightstudio.dpt.game.graphics;

import fr.dwightstudio.dpt.engine.graphics.Texture;

import static org.lwjgl.opengl.GL11.*;

public class Tile {
    private final int size;
    private final int x;
    private final int y;
    private final Texture texture;

    public Tile(int x, int y, int size, Texture texture) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.texture = texture;
    }

    public void blit() {
        texture.bind();
        glBegin(GL_QUADS);
        glTexCoord2f(0, 0);
        glVertex2f(x,  y);
        glTexCoord2f(1, 0);
        glVertex2f(x + size,  y);
        glTexCoord2f(1, 1);
        glVertex2f(x + size,  y + size);
        glTexCoord2f(0, 1);
        glVertex2f(x,  y + size);
        glEnd();
    }
}
