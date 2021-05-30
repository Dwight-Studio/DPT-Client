package fr.dwightstudio.dpt.engine.graphics.render;

import static org.lwjgl.opengl.GL11.*;

public class Texture {
    private final int width;
    private final int height;
    private final int id;
    private final int nbChannel;

    public Texture(int width, int height, int id, int nbChannel) {
        this.width = width;
        this.height = height;
        this.id = id;
        this.nbChannel = nbChannel;
    }

    public void bind() {
        glBindTexture(GL_TEXTURE_2D, id);
    }

    public void unbind() {
        glBindTexture(GL_TEXTURE_2D, 0);
    }

    public int getWidth() {
        return this.width;
    }

    public int getHeight() {
        return this.height;
    }

    public int getChannelsNumber() {
        return this.nbChannel;
    }

    public int getTextureID() {
        return this.id;
    }

    public void delete() {
        glDeleteTextures(id);
    }

    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Texture)) return false;

        Texture texture = (Texture) object;

        return texture.getTextureID() == this.getTextureID();
    }
}
