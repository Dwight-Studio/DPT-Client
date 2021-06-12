/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import java.util.List;

public class Spritesheet {

    private final Texture texture;
    private final List<SpriteTexture> spriteTextures;

    /**
     * Create a new Spritesheet
     *
     * @param texture the Spritesheet Texture
     * @param sprites a list of all the Spritesheet textures
     */
    public Spritesheet(Texture texture, List<SpriteTexture> sprites) {
        this.texture = texture;
        this.spriteTextures = sprites;
    }

    /**
     * Return a specified SpriteTexture
     *
     * @param index the SpriteTexture index in the list
     * @return the specified SpriteTexture, if it does not exist, return null
     */
    public SpriteTexture getSprite(int index) {
        if (spriteTextures.size() > index) {
            return spriteTextures.get(index);
        }
        return null;
    }

    /**
     * @return the Spritesheet Texture
     */
    public Texture getTexture() {
        return texture;
    }

    /**
     * @return the number of SpriteTexture available in this Spritesheet
     */
    public int getNumberOfSprite() {
        return spriteTextures.size();
    }
}
