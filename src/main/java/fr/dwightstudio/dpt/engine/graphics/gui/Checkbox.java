/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.Spritesheet;
import org.joml.Vector2f;

public class Checkbox extends Button {

    private boolean state;
    private Spritesheet checkboxSpritesheet;

    /**
     * Create a new Checkbox
     *
     * @param position the position of the Checkbox
     * @param scale the scale of the Checkbox
     * @param color the color of the Checkbox
     */
    public Checkbox(Vector2f position, Vector2f scale, Color color) {
        super(position, scale, color);
        this.state = false;
    }

    /**
     * Create a new Checkbox
     *
     * NOTE: All the Texture will be scaled according to the scale parameter
     * The Spritesheet must contain at least 1 picture
     * The Spritesheet must respect the following structure :
     *
     * First sprite     (index 0) :     defaultCheckboxTexture
     * Second sprite    (index 1) :     checkedCheckboxTexture (optional)
     * Third sprite     (index 2) :     hoverCheckboxTexture (optional)
     * Fourth sprite    (index 3) :     checkedHoverCheckboxTexture (optional)
     *
     * @param position the position of the Checkbox
     * @param scale the scale of the Checkbox
     * @param checkboxSpritesheet the Spritesheet for the Checkbox
     */
    public Checkbox(Vector2f position, Vector2f scale, Spritesheet checkboxSpritesheet) {
        super(position, scale, checkboxSpritesheet);
        this.state = false;
        this.checkboxSpritesheet = checkboxSpritesheet;
    }

    /**
     * Create a new Checkbox
     *
     * @param position the position of the Checkbox
     * @param scale the scale of the Checkbox
     * @param color the color of the Checkbox
     * @param state the starting state of the Checkbox
     */
    public Checkbox(Vector2f position, Vector2f scale, Color color, boolean state) {
        super(position, scale, color);
        this.state = state;
    }

    /**
     * Create a new Checkbox
     *
     * NOTE: All the Texture will be scaled according to the scale parameter
     * The Spritesheet must contain at least 1 picture
     * The Spritesheet must respect the following structure :
     *
     * First sprite     (index 0) :     defaultCheckboxTexture
     * Second sprite    (index 1) :     checkedCheckboxTexture (optional)
     * Third sprite     (index 2) :     hoverCheckboxTexture (optional)
     * Fourth sprite    (index 3) :     checkedHoverCheckboxTexture (optional)
     *
     * @param position the position of the Checkbox
     * @param scale the scale of the Checkbox
     * @param checkboxSpritesheet the Spritesheet for the Checkbox
     * @param state the starting state of the Checkbox
     */
    public Checkbox(Vector2f position, Vector2f scale, Spritesheet checkboxSpritesheet, boolean state) {
        super(position, scale, checkboxSpritesheet);
        this.state = state;
        this.checkboxSpritesheet = checkboxSpritesheet;
    }

    /**
     * Set the clicked parameter, change textures and fire the appropriate events
     *
     * @param clicked the clicked value
     */
    @Override
    protected void setClicked(boolean clicked) {
        if (!clicked) {
            this.state = !state;
        }
        if (clicked != this.clicked) {
            super.setClicked(clicked);
        }
    }

    /**
     * Set the hover parameter, change textures and fire the appropriate events
     *
     * @param hover the hover value
     */
    @Override
    protected void setHover(boolean hover) {
        super.setHover(hover);
    }

    /**
     * Change the button texture
     *
     * @param clicked the clicked value
     * @param hover the hover value
     */
    @Override
    protected void changeTexture(boolean clicked, boolean hover) {
        // The Spritesheet should respect the following structure :
        // First sprite     (index 0) :     defaultCheckboxTexture
        // Second sprite    (index 1) :     checkedCheckboxTexture
        // Third sprite     (index 2) :     hoverCheckboxTexture
        // Fourth sprite    (index 3) :     checkedHoverCheckboxTexture
        if (state) {
            if (hover) {
                if (checkboxSpritesheet.getNumberOfSprite() >= 4) {
                    setTextureCoords(checkboxSpritesheet.getSprite(3).getTextureCoords());
                }
            } else {
                if (checkboxSpritesheet.getNumberOfSprite() >= 2) {
                    setTextureCoords(checkboxSpritesheet.getSprite(1).getTextureCoords());
                }
            }
        } else {
            if (hover) {
                if (checkboxSpritesheet.getNumberOfSprite() >= 3) {
                    setTextureCoords(checkboxSpritesheet.getSprite(2).getTextureCoords());
                }
            } else {
                setTextureCoords(checkboxSpritesheet.getSprite(0).getTextureCoords());
            }
        }
    }

    /**
     * @return the current state of this Checkbox
     */
    public boolean getState() {
        return state;
    }
}
