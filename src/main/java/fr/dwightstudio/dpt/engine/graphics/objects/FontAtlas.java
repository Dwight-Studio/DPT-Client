/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import java.awt.*;
import java.util.Map;

public class FontAtlas {

    private final Texture texture;
    private final Font font;
    private final boolean antiAliasing;
    private final Map<Character, Glyph> glyphMap;

    /**
     * Create a new FontAtlas
     *
     * @param texture the FontAtlas Texture
     * @param font the FontAtlas font
     * @param antiAliasing the FontAtlas is using antialiasing
     * @param glyphMap a map containing all the FontAtlas glyphs
     */
    public FontAtlas(Texture texture, Font font, boolean antiAliasing, Map<Character, Glyph> glyphMap) {
        this.texture = texture;
        this.font = font;
        this.antiAliasing = antiAliasing;
        this.glyphMap = glyphMap;
    }

    /**
     * @return the FontAtlas texture
     */
    public Texture getTexture() {
        return texture;
    }

    /**
     * @return the FontAtlas font
     */
    public Font getFont() {
        return font;
    }

    /**
     * @return if the FontAtlas is using antialiasing
     */
    public boolean isAntiAliasing() {
        return antiAliasing;
    }

    /**
     * @return the FontAtlas glyphs map
     */
    public Map<Character, Glyph> getGlyphMap() {
        return glyphMap;
    }

    /**
     * Gets a specific character in the FontAtlas
     *
     * @param character the glyph to get
     * @return the specified glyph, if it does not exist it return null
     */
    public Glyph getGlyph(char character) {
        if (this.glyphMap.containsKey(character)) {
            return this.glyphMap.get(character);
        }
        return null;
    }

}
