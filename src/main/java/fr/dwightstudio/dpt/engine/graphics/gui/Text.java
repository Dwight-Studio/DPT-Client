package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.primitives.Surface;
import org.joml.Vector2f;
import org.lwjgl.BufferUtils;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.ByteBuffer;

import static org.lwjgl.opengl.GL11.*;

public class Text {

    private static Texture texture;
    private static int width;
    private static int height;

    public static Surface createSurface(float x, float y, String string, Font font, Color color) {
        ByteBuffer image = createImageFromString(string, font, color);
        Text.texture = createTexture(image);
        return new Surface(x, y, width, height, texture);
    }

    public static Texture getTexture(String string, Font font, Color color) {
        ByteBuffer image = createImageFromString(string, font, color);
        return createTexture(image);
    }

    public static Vector2f getLastSize() {
        return new Vector2f(width, height);
    }
    
    private static ByteBuffer createImageFromString(String string, Font font, Color color) {
        
        BufferedImage img = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = img.createGraphics();

        g2d.setFont(font);
        FontMetrics fm = g2d.getFontMetrics();
        width = fm.stringWidth(string);
        height = fm.getHeight();
        g2d.dispose();

        img = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        g2d = img.createGraphics();
        g2d.setFont(font);
        fm = g2d.getFontMetrics();
        g2d.setColor(color);
        g2d.drawString(string, 0, fm.getAscent());
        g2d.dispose();

        int[] pixels = new int[img.getWidth() * img.getHeight()];
        img.getRGB(0, 0, img.getWidth(), img.getHeight(), pixels, 0, img.getWidth());
        ByteBuffer buffer = BufferUtils.createByteBuffer(img.getWidth() * img.getHeight() * 4);
        // Iterate through all the pixels and add them to the ByteBuffer
        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                // Select the pixel
                int pixel = pixels[y * img.getWidth() + x];
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
        return buffer;
    }
    
    private static Texture createTexture(ByteBuffer image) {
        if (image == null) {
            return null;
        } else {
            int id = glGenTextures();
            glBindTexture(GL_TEXTURE_2D, id);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
            glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
            return new Texture(width, height, id, 4); // Since we are creating a PNG image, there is four channels
        }
    }
}
