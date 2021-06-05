package fr.dwightstudio.dpt.engine.graphics.objects;

import java.nio.ByteBuffer;

import static org.lwjgl.opengl.GL11.*;

public class Texture {
    private final int width;
    private final int height;
    private final int id;
    private final int nbChannel;
    private final String filepath;
    private final ByteBuffer imageByteBuffer;

    public Texture(int width, int height, int id, int nbChannel, String filepath, ByteBuffer imageByteBuffer) {
        this.width = width;
        this.height = height;
        this.id = id;
        this.nbChannel = nbChannel;
        this.filepath = filepath;
        this.imageByteBuffer = imageByteBuffer;
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

    public int getID() {
        return this.id;
    }

    public String getFilepath() {
        return this.filepath;
    }

    public ByteBuffer getImageByteBuffer() {
        return this.imageByteBuffer;
    }

    public void delete() {
        glDeleteTextures(id);
    }

    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Texture)) return false;

        Texture texture = (Texture) object;

        return texture.getID() == this.getID();
    }
}
