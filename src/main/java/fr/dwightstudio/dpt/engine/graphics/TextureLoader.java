package fr.dwightstudio.dpt.engine.graphics;

import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.stb.STBImage.stbi_image_free;
import static org.lwjgl.stb.STBImage.stbi_load;

public class TextureLoader {
    private final int[] width;
    private final int[] height;
    private final int[] nbChannel;
    private int id;

    public TextureLoader(String file) {
        this.width = new int[1];
        this.height = new int[1];
        this.nbChannel = new int[1];
        load_texture(file);
    }

    private void load_texture(String file) {
        ByteBuffer texture = stbi_load(file, width, height, nbChannel, 4);
        if (texture == null) {
            GameLogger.logger.log(Level.WARNING, "File not found : {0}", new Object[] {file});
        } else {
            id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width[0], height[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture);
            stbi_image_free(texture);
            GameLogger.logger.log(Level.FINE, "Finished loading texture : {0}", new Object[] {file});
        }
    }

    public void bind() {
        glBindTexture(GL_TEXTURE_2D, id);
    }
}
