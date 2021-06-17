/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.primitives;

import fr.dwightstudio.dpt.engine.DSEngine;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.graphics.objects.Transform;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

import java.util.Arrays;

public class Surface extends Component {

    private Color color;
    private Transform transform = new Transform();
    private Transform lastTransform;
    private Texture texture;
    private Vector2f[] textureCoords;

    private boolean dirty = true;

    /**
     * Create a new Surface
     *
     * @param position the Surface position
     * @param scale the Surface scale
     * @param texture the Surface Texture
     * @param textureCoords the Texture coordinates to get on the given Texture
     */
    public Surface(Vector2f position, Vector2f scale, Texture texture, Vector2f[] textureCoords) {
        this.color = DSEngine.COLORS.WHITE;
        this.transform.position = position;
        this.transform.scale = scale;
        this.lastTransform = new Transform();
        this.texture = texture;
        this.textureCoords = textureCoords;
    }

    /**
     * Create a new Surface
     *
     * @param position the Surface position
     * @param scale the Surface scale
     * @param color the Surface color
     */
    public Surface(Vector2f position, Vector2f scale, Color color) {
        this.color = color;
        this.transform.position = position;
        this.transform.scale = scale;
        this.lastTransform = new Transform();
        this.texture = null;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 0),
                new Vector2f(1, 1),
                new Vector2f(0, 1),
                new Vector2f(0, 0),
        };
    }

    /**
     * Create a new Surface
     *
     * @param position the Surface position
     * @param scale the Surface scale
     * @param texture the Surface Texture
     */
    public Surface(Vector2f position, Vector2f scale, Texture texture) {
        this.color = DSEngine.COLORS.WHITE;
        this.transform.position = position;
        this.transform.scale = scale;
        this.lastTransform = new Transform();
        this.texture = texture;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 0),
                new Vector2f(1, 1),
                new Vector2f(0, 1),
                new Vector2f(0, 0),
        };
    }

    @Override
    public void update(double dt) {
        if (!this.lastTransform.equals(this.transform)) {
            this.lastTransform = this.transform.copy();
            dirty = true;
        }
    }

    /**
     * @return the Surface color
     */
    public Color getColor() {
        return color;
    }

    /**
     * @return the Surface Transform object
     */
    public Transform getTransform() {
        return transform;
    }

    /**
     * @return the Surface Texture
     */
    public Texture getTexture() {
        return texture;
    }

    /**
     * @return the Surface Texture coordinates
     */
    public Vector2f[] getTextureCoords() {
        return textureCoords;
    }

    /**
     * Set a new color to the Surface
     *
     * @param newColor a color
     */
    public void setColor(Color newColor) {
        if (!newColor.equals(this.color)) {
            this.color = newColor;
            this.dirty = true;
        }
    }

    /**
     * Set a new Transform objec to the Surface
     *
     * @param transform a Transform object
     */
    public void setTransform(Transform transform) {
        this.transform = transform;
        this.dirty = true;
    }

    /**
     * Set another Texture for the Surface
     *
     * @param texture a Texture
     */
    public void setTexture(Texture texture) {
        if (!texture.equals(this.texture)) {
            this.texture = texture;
            this.dirty = true;
        }
    }

    /**
     * Set specific Texture coordinates to use with the Texture
     *
     * @param textureCoords a new Texture coordinates Vector
     */
    public void setTextureCoords(Vector2f[] textureCoords) {
        if (!Arrays.equals(textureCoords, this.textureCoords)) {
            this.textureCoords = textureCoords;
            this.dirty = true;
        }
    }

    /**
     *
     * @return the dirty flag value
     */
    public boolean isDirty() {
        return dirty;
    }

    /**
     * Mark this object as clean (it will not be rebuffered)
     */
    public void markClean() {
        dirty = false;
    }

    /**
     * @return the center X and Y point of the Surface
     */
    public Vector2f getCenterPoint() {
        return new Vector2f((transform.scale.x + gameObject.getTransform().scale.x) / 2, (transform.scale.y + gameObject.getTransform().scale.y) / 2);
    }
}
