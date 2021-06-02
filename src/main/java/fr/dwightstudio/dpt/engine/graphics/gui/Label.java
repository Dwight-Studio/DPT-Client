package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;
import org.lwjgl.BufferUtils;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.ByteBuffer;
import java.text.MessageFormat;

import static org.lwjgl.opengl.GL11.*;

public class Label extends Component {

    private int width;
    private int height;
    private boolean antiAliasing;
    private String string;
    private Font font;
    private Color color;
    private Texture texture;

    public Label(String string, Font font, Color color, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = antiAliasing;
        ByteBuffer image = createImageFromString(string, font, color, this.antiAliasing);
        this.texture = TextureLoader.createTexture(image, width, height);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font, Color color) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = false;
        ByteBuffer image = createImageFromString(string, font, color, false);
        this.texture = TextureLoader.createTexture(image, width, height);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = antiAliasing;
        ByteBuffer image = createImageFromString(string, font, this.color, this.antiAliasing);
        this.texture = TextureLoader.createTexture(image, width, height);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font) {
        this.string = string;
        this.font = font;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = false;
        ByteBuffer image = createImageFromString(string, font, this.color, false);
        this.texture = TextureLoader.createTexture(image, width, height);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Vector2f getScale() {
        return new Vector2f(width, height);
    }

    public String getText() {
        return this.string;
    }

    public Font getFont() {
        return this.font;
    }

    public Texture getTexture() {
        return this.texture;
    }

    public boolean isUsingAntialiasing() {
        return this.antiAliasing;
    }

    public Surface createSurface(float x, float y) {
        return new Surface(new Vector2f(x, y), this.width, this.height, this.texture);
    }

    public void setText(String string) {
        this.string = string;
        ByteBuffer image = createImageFromString(string, this.font, this.color, this.antiAliasing);
        this.texture = TextureLoader.reloadTexture(image, this.texture, width, height);
    }

    public void setFont(Font newFont) {
        this.font = newFont;
    }

    public void setColor(Color newColor) {
        this.color = newColor;
    }

    public void setAntiAliasing(boolean antiAliasing) {
        this.antiAliasing = antiAliasing;
    }
    
    private ByteBuffer createImageFromString(String string, Font font, Color color, boolean antiAliasing) {
        
        BufferedImage img = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = img.createGraphics();

        g2d.setFont(font);
        FontMetrics fm = g2d.getFontMetrics();
        width = fm.stringWidth(string);
        height = fm.getHeight();
        g2d.dispose();

        img = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        g2d = img.createGraphics();
        if (this.antiAliasing) {
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        }
        g2d.setFont(font);
        fm = g2d.getFontMetrics();
        g2d.setColor(new java.awt.Color(color.getRed() * 255, color.getGreen() * 255, color.getBlue() * 255));
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

    @Override
    public void update(float dt) {

    }
}
