/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import java.nio.ByteBuffer;

import static org.lwjgl.opengl.GL11.*;

public class Texture {
    private final int width;
    private final int height;
    private final int id;
    private final int nbChannel;
    private final String filepath;

    /**
     * Create a new Texture
     *
     * @param width the Texture widht
     * @param height the Texture height
     * @param id the Texture ID
     * @param nbChannel the number of available channel in this Texture
     * @param filepath the Texture filepath
     */
    public Texture(int width, int height, int id, int nbChannel, String filepath) {
        this.width = width;
        this.height = height;
        this.id = id;
        this.nbChannel = nbChannel;
        this.filepath = filepath;
    }

    /**
     * Bind the Texture to use it
     */
    public void bind() {
        glBindTexture(GL_TEXTURE_2D, id);
    }

    /**
     * Unbind the Texture
     */
    public void unbind() {
        glBindTexture(GL_TEXTURE_2D, 0);
    }

    /**
     * @return the width of the Texture
     */
    public int getWidth() {
        return this.width;
    }

    /**
     * @return the height of the Texture
     */
    public int getHeight() {
        return this.height;
    }

    /**
     * @return the number of available channel of the Texture
     */
    public int getChannelsNumber() {
        return this.nbChannel;
    }

    /**
     * @return the Texture ID
     */
    public int getID() {
        return this.id;
    }

    /**
     * @return the Texture filepath
     */
    public String getFilepath() {
        return this.filepath;
    }

    /**
     * Delete the Texture
     */
    public void delete() {
        glDeleteTextures(id);
    }

    /**
     * Check equality betwenn the two Texture objects
     *
     * @param object a Texture
     * @return equality
     */
    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Texture)) return false;

        Texture texture = (Texture) object;

        return texture.getID() == this.getID();
    }
}
