/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureUtils;

import java.util.HashMap;
import java.util.Map;

import static org.lwjgl.opengl.GL11.GL_NEAREST;

public class TextureHandler implements TypeHandler<Texture> {

    private static final Map<String, Texture> TEXTURES = new HashMap<>();

    @Override
    public Texture get(String filepath) {
        if (!TEXTURES.containsKey(filepath)) {
            Texture texture = TextureUtils.loadTexture(filepath, GL_NEAREST);
            if (texture != null) {
                TEXTURES.put(filepath, texture);
            } else {
                return null;
            }
        }
        return TEXTURES.get(filepath);
    }
}
