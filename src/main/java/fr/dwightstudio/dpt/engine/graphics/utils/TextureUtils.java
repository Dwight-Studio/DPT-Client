package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import org.lwjgl.BufferUtils;

import java.awt.image.BufferedImage;
import java.nio.ByteBuffer;
import java.text.MessageFormat;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.stb.STBImage.*;

public class TextureUtils {

    private static final int[] width = new int[1];
    private static final int[] height = new int[1];
    private static final int[] nbChannel = new int[1];

    public static Texture loadTexture(String file) {
        ByteBuffer texture = stbi_load(file, width, height, nbChannel, 4);
        if (texture == null) {
            GameLogger.getLogger("TextureLoader").warn(MessageFormat.format("File not found : {0}", file));
            return null;
        } else {
            int id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width[0], height[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture);
            stbi_image_free(texture);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            GameLogger.getLogger("TextureLoader").debug(MessageFormat.format("Finished loading texture : {0}", file));
            return new Texture(width[0], height[0], id, nbChannel[0], file, texture);
        }
    }

    public static Texture createTexture(ByteBuffer image, int width, int height) {
        if (image != null) {
            int id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            return new Texture(width, height, id, 4, null, image); // Since we are creating a PNG image, there is four channels
        }
        return null;
    }

    public static Texture createTexture(BufferedImage image, int width, int height) {
        if (image != null) {
            int[] pixels = new int[image.getWidth() * image.getHeight()];
            image.getRGB(0, 0, image.getWidth(), image.getHeight(), pixels, 0, image.getWidth());
            ByteBuffer buffer = BufferUtils.createByteBuffer(image.getWidth() * image.getHeight() * 4);
            // Iterate through all the pixels and add them to the ByteBuffer
            for (int y = 0; y < image.getHeight(); y++) {
                for (int x1 = 0; x1 < image.getWidth(); x1++) {
                    // Select the pixel
                    int pixel = pixels[y * image.getWidth() + x1];
                    // Add the RED component
                    buffer.put((byte) ((pixel >> 16) & 0xFF));
                    // Add the GREEN component
                    buffer.put((byte) ((pixel >> 8) & 0xFF));
                    // Add the BLUE component
                    buffer.put((byte) (pixel & 0xFF));
                    // Add the ALPHA component
                    buffer.put((byte) ((pixel >> 24) & 0xFF));
                }
            }
            // Reset the read location in the buffer so that GL can read from
            // beginning.
            buffer.flip();
            int id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            return new Texture(width, height, id, 4, null, buffer); // Since we are creating a PNG image, there is four channels
        }
        return null;
    }

    public static Texture reloadTexture(ByteBuffer image, Texture texture, int width, int height) {
        if (image != null) {
            glBindTexture(GL_TEXTURE_2D, texture.getTextureID());
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            return new Texture(width, height, texture.getTextureID(), 4, null, image);
        }
        return null;
    }
}
