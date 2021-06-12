/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

public class Transform {

    public static int RADIAN = 0;
    public static int DEGREE = 1;

    public Vector2f position;
    public Vector2f scale;
    private float rotation;

    /**
     * Create a new Transform with default values (all zero)
     */
    public Transform() {
        this.position = new Vector2f();
        this.scale = new Vector2f();
        this.rotation = 0.0f;
    }

    /**
     * Create a new Transform
     *
     * @param position the position
     */
    public Transform(Vector2f position) {
        this.position = position;
        this.scale = new Vector2f();
        this.rotation = 0.0f;
    }

    /**
     * Create a new Transform
     *
     * @param rotation the rotation
     */
    public Transform(float rotation) {
        this.position = new Vector2f();
        this.scale = new Vector2f();
        this.rotation = rotation;
    }

    /**
     * Create a new Tranform
     *
     * @param position the position
     * @param scale the scale
     */
    public Transform(Vector2f position, Vector2f scale) {
        this.position = position;
        this.scale = scale;
        this.rotation = 0.0f;
    }

    /**
     * Create a new Transform
     *
     * @param position the position
     * @param rotation the rotation
     */
    public Transform(Vector2f position, float rotation) {
        this.position = position;
        this.scale = new Vector2f();
        this.rotation = rotation;
    }

    /**
     * Create a new Transform
     *
     * @param position the position
     * @param scale the scale
     * @param rotation the rotation
     */
    public Transform(Vector2f position, Vector2f scale, float rotation) {
        this.position = position;
        this.scale = scale;
        this.rotation = rotation;
    }

    /**
     * Create a copy of an instance of the Transform object
     *
     * @return a new instance of the Transform object
     */
    public Transform copy() {
        return new Transform(new Vector2f(this.position), new Vector2f(this.scale), this.rotation);
    }

    /**
     * Set the rotation value
     *
     * @param rotation the new value of the rotation
     * @param rotationType can be Transform.DEGREE or Transform.RADIAN
     */
    public void setRotation(float rotation, int rotationType) {
        if (rotationType == Transform.RADIAN) {
            this.rotation = rotation;
        } else if (rotationType == Transform.DEGREE) {
            this.rotation = (float) (rotation * (Math.PI / 180));
        }
    }

    /**
     * Set the rotation value in radian
     *
     * @param rotation the new value of the rotation in radian
     */
    public void setRotation(float rotation) {
        this.rotation = rotation;
    }

    /**
     * Get the rotation value
     *
     * @param rotationType can be Transform.DEGREE or Transform.RADIAN
     * @return a float value which correspond to the rotation value
     */
    public float getRotation(int rotationType) {
        if (rotationType == Transform.RADIAN) {
            return this.rotation;
        } else if (rotationType == Transform.DEGREE) {
            return (float) (this.rotation * (180 / Math.PI));
        }
        return this.rotation;
    }

    /**
     * Get the rotation value in radian
     *
     * @return a float value which correspond to the rotation value in radian
     */
    public float getRotation() {
        return this.rotation;
    }

    /**
     * Check if two instance of the Transform object are equals
     *
     * @param object another Transform instance
     * @return true if the two instance are equal, otherwise, false
     */
    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Transform)) return false;

        Transform transform = (Transform) object;

        return transform.position.equals(this.position) && transform.scale.equals(this.scale) && transform.rotation == this.rotation;
    }
}
