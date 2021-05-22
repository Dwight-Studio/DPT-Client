package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.stb.STBImage.stbi_image_free;
import static org.lwjgl.stb.STBImage.stbi_load;

public class TextureLoader {

    public static List<Integer> texturesList = new ArrayList<>();

    private static final int[] width = new int[1];
    private static final int[] height = new int[1];
    private static final int[] nbChannel = new int[1];

    public static Texture loadTexture(String file) {
        ByteBuffer texture = stbi_load(file, width, height, nbChannel, 4);
        if (texture == null) {
            GameLogger.logger.log(Level.WARNING, "File not found : {0}", new Object[] {file});
            return null;
        } else {
            int id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width[0], height[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture);
            stbi_image_free(texture);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            texturesList.add(id);
            GameLogger.logger.log(Level.FINE, "Finished loading texture : {0}", new Object[] {file});
            return new Texture(width[0], height[0], id, nbChannel[0]);
        }
    }
}
