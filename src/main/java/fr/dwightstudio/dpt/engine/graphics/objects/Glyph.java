/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

public class Glyph {

    private final int width;
    private final int height;
    private final int x;
    private final int y;

    /**
     * Create a new Glyph
     *
     * @param width the width of the Glyph
     * @param height the height of the Glyph
     * @param x the x coordinate on the FontAltas Texture
     * @param y the y coordinate on the FontAtlas Texture
     */
    public Glyph(int width, int height, int x, int y) {
        this.width = width;
        this.height = height;
        this.x = x;
        this.y = y;
    }

    /**
     * @return the Glyph width
     */
    public int getWidth() {
        return width;
    }

    /**
     * @return the Glyph height
     */
    public int getHeight() {
        return height;
    }

    /**
     * @return the Glyph x coordinate on the FontAtlas Texture
     */
    public int getX() {
        return x;
    }

    /**
     * @return the Glyph y coordinate on the FontAtlas Texture
     */
    public int getY() {
        return y;
    }

    /**
     * Gets the Texture coordinates of this Glyph on the specified FontAtlas
     *
     * @param fontAtlas a FontAtlas containing this Glyph
     * @return the Texture coordinates of this Glyph
     */
    public Vector2f[] getTextureCoords(FontAtlas fontAtlas) {
        float top = (y + height) / (float) fontAtlas.getTexture().getHeight();
        float right = (x + width) / (float) fontAtlas.getTexture().getWidth();
        float left = x / (float) fontAtlas.getTexture().getWidth();
        float bottom = y / (float) fontAtlas.getTexture().getHeight();

        return new Vector2f[] {
                new Vector2f(right, bottom),
                new Vector2f(right, top),
                new Vector2f(left, top),
                new Vector2f(left, bottom),
        };
    }

}
