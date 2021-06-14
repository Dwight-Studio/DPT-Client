/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.objects.Glyph;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import org.lwjgl.BufferUtils;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.lwjgl.opengl.GL11.GL_LINEAR;

public class FontUtils {

    private static final List<FontAtlas> fontAtlasList = new ArrayList<>();

    /**
     * Create a FontAtlas with a Font
     *
     * @param font the Font used in the FontAtlas
     * @param antiAliasing enable or disable anti aliasing
     * @return a FontAtlas
     */
    public static FontAtlas createFontAtlas(Font font, boolean antiAliasing) {
        for (FontAtlas fontAtlas : fontAtlasList) {
            if (fontAtlas.getFont().equals(font) && fontAtlas.isAntiAliasing() == antiAliasing && font.getSize() == fontAtlas.getFont().getSize()) {
                return fontAtlas;
            }
        }
        int imageWidth = 0;
        int imageHeight = 0;
        Map<Character, Glyph> glyphMap = new HashMap<>();

        for (int i = 32; i < 256; i++) {
            if (i == 127) {
                continue;
            }
            char character = (char) i;
            BufferedImage charactersImage = createCharImage(font, character, antiAliasing);
            if (charactersImage == null) {
                continue;
            }

            imageWidth += charactersImage.getWidth();
            imageHeight = Math.max(imageHeight, charactersImage.getHeight());
        }

        BufferedImage fontImage = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics2D = fontImage.createGraphics();

        int x = 0;

        for (int i = 32; i < 256; i++) {
            if (i == 127) {
                continue;
            }
            char character = (char) i;
            BufferedImage characterImage = createCharImage(font, character, antiAliasing);
            if (characterImage == null) {
                continue;
            }


            int charWidth = characterImage.getWidth();
            int charHeight = characterImage.getHeight();
            Glyph glyph = new Glyph(charWidth, charHeight, x, characterImage.getHeight() - charHeight);
            glyphMap.put(character, glyph);

            graphics2D.drawImage(characterImage, x, 0, null);
            x += charWidth;
        }

        graphics2D.dispose();

        int[] pixels = new int[fontImage.getWidth() * fontImage.getHeight()];
        fontImage.getRGB(0, 0, fontImage.getWidth(), fontImage.getHeight(), pixels, 0, fontImage.getWidth());
        ByteBuffer buffer = BufferUtils.createByteBuffer(fontImage.getWidth() * fontImage.getHeight() * 4);
        // Iterate through all the pixels and add them to the ByteBuffer
        for (int y = 0; y < fontImage.getHeight(); y++) {
            for (int x1 = 0; x1 < fontImage.getWidth(); x1++) {
                // Select the pixel
                int pixel = pixels[y * fontImage.getWidth() + x1];
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
        Texture texture = TextureUtils.createTexture(buffer, fontImage.getWidth(), fontImage.getHeight(), GL_LINEAR);
        FontAtlas fontAtlas = new FontAtlas(texture, font, antiAliasing, glyphMap);
        fontAtlasList.add(fontAtlas);
        return fontAtlas;
    }

    /**
     * Create an image containing the specified character with the specified Font
     *
     * @param font a character Font
     * @param c a character
     * @param antiAliasing enable or disable anti aliasing
     * @return a BufferedImage containing the character image
     */
    public static BufferedImage createCharImage(Font font, char c, boolean antiAliasing) {
        BufferedImage image = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics2D = image.createGraphics();
        if (antiAliasing) {
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        }
        graphics2D.setFont(font);
        FontMetrics fontMetrics = graphics2D.getFontMetrics();
        graphics2D.dispose();

        int charWidth = fontMetrics.charWidth(c);
        int charHeight = fontMetrics.getHeight();

        if (charWidth == 0) {
            return null;
        }

        image = new BufferedImage(charWidth, charHeight, BufferedImage.TYPE_INT_ARGB);
        graphics2D = image.createGraphics();
        if (antiAliasing) {
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        }
        graphics2D.setFont(font);
        graphics2D.setPaint(java.awt.Color.WHITE);
        graphics2D.drawString(String.valueOf(c), 0, fontMetrics.getAscent());
        graphics2D.dispose();
        return image;
    }
}
