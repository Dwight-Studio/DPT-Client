package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.graphics.render.Glyph;
import fr.dwightstudio.dpt.engine.graphics.renderers.Renderer;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;
import org.lwjgl.system.MemoryUtil;

import java.awt.*;
import java.awt.Color;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;

public class GameFont {

    private final Map<Character, Glyph> glyphs;
    private final Texture texture;
    private int fontHeight;

    /**
     * Creates a font
     *
     * @param font the font to use
     * @param antiAlias whether the font should be antialiased or not
     */
    public GameFont(Font font, boolean antiAlias) {
        glyphs = new HashMap<>();
        texture = createFontTexture(font, antiAlias);
    }

    /**
     * Creates the font texture
     *
     * @param font the font
     * @param antiAlias whether the font should be antialiased or not
     *
     * @return font texture
     */
    private Texture createFontTexture(java.awt.Font font, boolean antiAlias) {
        int imageWidth = 0;
        int imageHeight = 0;

        // Loop through the characters and omit control codes
        for (int i = 32; i < 256; i++) {
            if (i == 127) {
                continue;
            }
            char c = (char) i;
            BufferedImage ch = createCharImage(font, c, antiAlias);
            if (ch == null) {
                continue;
            }

            imageWidth += ch.getWidth();
            imageHeight = Math.max(imageHeight, ch.getHeight());
        }

        fontHeight = imageHeight;

        BufferedImage image = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();

        int x = 0;

        // Loop through the characters and omit control codes
        for (int i = 32; i < 256; i++) {
            if (i == 127) {
                continue;
            }
            char c = (char) i;
            BufferedImage charImage = createCharImage(font, c, antiAlias);
            if (charImage == null) {
                continue;
            }

            int charWidth = charImage.getWidth();
            int charHeight = charImage.getHeight();

            // Create glyph and draw char on image
            Glyph ch = new Glyph(charWidth, charHeight, x, image.getHeight() - charHeight, 0f);
            g.drawImage(charImage, x, 0, null);
            x += ch.width;
            glyphs.put(c, ch);
        }

        // Flip image Horizontal to get the origin to bottom left
        AffineTransform transform = AffineTransform.getScaleInstance(1f, -1f);
        transform.translate(0, -image.getHeight());
        AffineTransformOp operation = new AffineTransformOp(transform,
                AffineTransformOp.TYPE_NEAREST_NEIGHBOR);
        image = operation.filter(image, null);

        // Get charWidth and charHeight of image
        int width = image.getWidth();
        int height = image.getHeight();

        // Get pixel data of image
        int[] pixels = new int[width * height];
        image.getRGB(0, 0, width, height, pixels, 0, width);

        // Put pixel data into a ByteBuffer
        ByteBuffer buffer = MemoryUtil.memAlloc(width * height * 4);
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                // Pixel as RGBA: 0xAARRGGBB
                int pixel = pixels[i * width + j];
                // Red component 0xAARRGGBB >> 16 = 0x0000AARR
                buffer.put((byte) ((pixel >> 16) & 0xFF));
                // Green component 0xAARRGGBB >> 8 = 0x00AARRGG
                buffer.put((byte) ((pixel >> 8) & 0xFF));
                // Blue component 0xAARRGGBB >> 0 = 0xAARRGGBB
                buffer.put((byte) (pixel & 0xFF));
                // Alpha component 0xAARRGGBB >> 24 = 0x000000AA
                buffer.put((byte) ((pixel >> 24) & 0xFF));
            }
        }

        buffer.flip();

        // Create texture
        Texture fontTexture = TextureLoader.createTexture(width, height, buffer);
        MemoryUtil.memFree(buffer);
        return fontTexture;
    }

    /**
     * Creates a char image from specified font and char.
     *
     * @param font the font
     * @param c the char
     * @param antiAlias whether the char should be antialiased or not
     *
     * @return the char image
     */
    private BufferedImage createCharImage(java.awt.Font font, char c, boolean antiAlias) {
        // Creating temporary image to extract character size
        BufferedImage image = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = image.createGraphics();
        if (antiAlias) {
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        }
        g.setFont(font);
        FontMetrics metrics = g.getFontMetrics();
        g.dispose();

        // Get char charWidth and charHeight
        int charWidth = metrics.charWidth(c);
        int charHeight = metrics.getHeight();

        // Check if charWidth is 0
        if (charWidth == 0) {
            return null;
        }

        // Create image for holding the char
        image = new BufferedImage(charWidth, charHeight, BufferedImage.TYPE_INT_ARGB);
        g = image.createGraphics();
        if (antiAlias) {
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        }
        g.setFont(font);
        g.setPaint(Color.WHITE);
        g.drawString(String.valueOf(c), 0, metrics.getAscent());
        g.dispose();
        return image;
    }

    /**
     * Gets the width of the specified text.
     *
     * @param text the text
     *
     * @return the width of text
     */
    public int getWidth(CharSequence text) {
        int width = 0;
        int lineWidth = 0;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '\n') {
                // Line end, set width to maximum from line width and stored width
                width = Math.max(width, lineWidth);
                lineWidth = 0;
                continue;
            }
            if (c == '\r') {
                // Line return, just skip it
                continue;
            }
            Glyph g = glyphs.get(c);
            lineWidth += g.width;
        }
        width = Math.max(width, lineWidth);
        return width;
    }

    /**
     * Gets the height of the specified text.
     *
     * @param text the text
     *
     * @return height of text
     */
    public int getHeight(CharSequence text) {
        int height = 0;
        int lineHeight = 0;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '\n') {
                // Line end, add line height to stored height
                height += lineHeight;
                lineHeight = 0;
                continue;
            }
            if (c == '\r') {
                // Line return, just skip it
                continue;
            }
            Glyph g = glyphs.get(c);
            lineHeight = Math.max(lineHeight, g.height);
        }
        height += lineHeight;
        return height;
    }

    /**
     * Draw text at the specified position and color.
     *
     * @param text the text to draw
     * @param x x-position
     * @param y y-position
     * @param c color to use
     */
    public void getTextSurface(CharSequence text, float x, float y, Color c) {
        int textHeight = getHeight(text);

        float drawX = x;
        float drawY = y;
        if (textHeight > fontHeight) {
            drawY += textHeight - fontHeight;
        }

        texture.bind();
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (ch == '\n') {
                // Line feed, set x and y to draw at the next line
                drawY -= fontHeight;
                drawX = x;
                continue;
            }
            if (ch == '\r') {
                // Line return, just skip it
                continue;
            }
            Glyph g = glyphs.get(ch);
            //TODO: Ajouter le draw en lui-même
            //renderer.drawTextureRegion(texture, drawX, drawY, g.x, g.y, g.width, g.height, c);
            drawX += g.width;
        }
    }

    /**
     * Disposes the font.
     */
    public void dispose() {
        texture.delete();
    }

}
