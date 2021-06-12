/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.primitives;

import fr.dwightstudio.dpt.engine.Engine;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.Transform;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

public class Line extends Component {

    private Vector2f startPosition;
    private Vector2f endPosition;
    private float thickness;
    private Color color;
    private final Transform transform;
    private Transform lastTransform;
    private boolean dirty = true;

    /**
     * Create a new Line
     *
     * @param startPosition the Line start position
     * @param endPosition the Line end position
     * @param color the Line color
     * @param thickness the Line thickness
     */
    public Line(Vector2f startPosition, Vector2f endPosition, Color color, float thickness) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = color;
        this.thickness = thickness;
        this.transform = new Transform();
        this.lastTransform = new Transform();
    }

    /**
     * Create a new Line
     *
     * @param startPosition the Line start position
     * @param endPosition the Line end position
     * @param color the Line color
     */
    public Line(Vector2f startPosition, Vector2f endPosition, Color color) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = color;
        this.thickness = 1.0f;
        this.transform = new Transform();
        this.lastTransform = new Transform();
    }

    /**
     * Create a new Line
     *
     * @param startPosition the Line start position
     * @param endPosition the Line end position
     * @param thickness the Line thickness
     */
    public Line(Vector2f startPosition, Vector2f endPosition, float thickness) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = Engine.COLORS.BLACK;
        this.thickness = thickness;
        this.transform = new Transform();
        this.lastTransform = new Transform();
    }

    /**
     * Create a new Line
     *
     * @param startPosition the Line start position
     * @param endPosition the Line end position
     */
    public Line(Vector2f startPosition, Vector2f endPosition) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = Engine.COLORS.BLACK;
        this.thickness = 1.0f;
        this.transform = new Transform();
        this.lastTransform = new Transform();
    }

    @Override
    public void update(float dt) {
        if (!this.lastTransform.equals(this.transform)) {
            this.lastTransform = this.transform.copy();
            dirty = true;
        }
    }

    /**
     * @return the Line start position
     */
    public Vector2f getStartPosition() {
        return startPosition;
    }

    /**
     * @return the Line end position
     */
    public Vector2f getEndPosition() {
        return endPosition;
    }

    /**
     * @return the Line position
     */
    public Color getColor() {
        return color;
    }

    /**
     * @return the Line thickness
     */
    public float getThickness() {
        return thickness;
    }

    /**
     * @return the Line Transform
     */
    public Transform getTransform() {
        return this.transform;
    }

    /**
     * @return the X and Y center point of the Line
     */
    public Vector2f getCenterPoints() {
        return new Vector2f((this.endPosition.x - this.startPosition.x) / 2, this.thickness / 2);
    }

    /**
     * Set the Line color
     *
     * @param newColor the new color
     */
    public void setColor(Color newColor) {
        if (!this.color.equals(newColor)) {
            this.color = newColor;
            dirty = true;
        }
    }

    /**
     * Set the Line start position
     *
     * @param newPosition the new start position
     */
    public void setStartPosition(Vector2f newPosition) {
        if (!this.startPosition.equals(newPosition)) {
            this.startPosition = newPosition;
            dirty = true;
        }
    }

    /**
     * Set the Line end position
     *
     * @param newPosition the new end position
     */
    public void setEndPosition(Vector2f newPosition) {
        if (!this.endPosition.equals(newPosition)) {
            this.endPosition = newPosition;
            dirty = true;
        }
    }

    /**
     * Set the Line thickness
     *
     * @param newThickness the new thickness value
     */
    public void setThickness(float newThickness) {
        if (this.thickness != newThickness) {
            this.thickness = newThickness;
            dirty = true;
        }
    }

    /**
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
}
