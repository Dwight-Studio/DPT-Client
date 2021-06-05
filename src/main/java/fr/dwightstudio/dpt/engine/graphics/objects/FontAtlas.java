package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

import java.awt.*;
import java.util.Map;

public class FontAtlas {

    private final Texture texture;
    private final Font font;
    private final boolean antiAliasing;
    private final Map<Character, Glyph> glyphMap;

    public FontAtlas(Texture texture, Font font, boolean antiAliasing, Map<Character, Glyph> glyphMap) {
        this.texture = texture;
        this.font = font;
        this.antiAliasing = antiAliasing;
        this.glyphMap = glyphMap;
    }

    public Texture getTexture() {
        return texture;
    }

    public Font getFont() {
        return font;
    }

    public boolean isAntiAliasing() {
        return antiAliasing;
    }

    public Map<Character, Glyph> getGlyphMap() {
        return glyphMap;
    }

    public Glyph getGlyph(char character) {
        if (this.glyphMap.containsKey(character)) {
            return this.glyphMap.get(character);
        }
        return null;
    }

}
