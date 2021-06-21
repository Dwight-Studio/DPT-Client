/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.objects;

public class Color {

    private final float red;
    private final float green;
    private final float blue;
    private final float alpha;

    /**
     * Create a new Color
     *
     * All the values should be between 0 and 1
     *
     * The alpha value will be 1.0f
     *
     * @param r the red value
     * @param g the green value
     * @param b the blue value
     */
    public Color(float r, float g, float b) {
        this.red = r;
        this.green = g;
        this.blue = b;
        this.alpha = 1;
    }

    /**
     * Create a new Color
     *
     * All the values should be between 0 and 1
     *
     * @param r the red value
     * @param g the green value
     * @param b the blue value
     * @param a the alpha value
     */
    public Color(float r, float g, float b, float a) {
        this.red = r;
        this.green = g;
        this.blue = b;
        this.alpha = a;
    }

    /**
     * @return the red value
     */
    public float getRed() {
        return red;
    }

    /**
     * @return the green value
     */
    public float getGreen() {
        return green;
    }

    /**
     * @return the blue value
     */
    public float getBlue() {
        return blue;
    }

    /**
     * @return the alpha value
     */
    public float getAlpha() {
        return alpha;
    }

    /**
     * Check equality between two Color objects
     *
     * @param object another Color
     * @return true or false
     */
    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Color)) return false;

        Color color = (Color) object;

        return color.getRed() == this.red && color.getGreen() == this.green && color.getBlue() == this.blue && color.getAlpha() == this.alpha;
    }
}
