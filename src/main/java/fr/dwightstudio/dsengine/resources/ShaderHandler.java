/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.resources;

import fr.dwightstudio.dsengine.graphics.objects.Shader;
import fr.dwightstudio.dsengine.graphics.utils.ShaderLoader;

import java.util.HashMap;
import java.util.Map;

public class ShaderHandler implements TypeHandler<Shader> {

    private static final Map<String, Shader> SHADERS = new HashMap<>();

    @Override
    public Shader get(String filepath) {
        if (!SHADERS.containsKey(filepath)) {
            Shader shader = ShaderLoader.loadShaderFile(filepath);
            if (shader != null) {
                SHADERS.put(filepath, shader);
            } else {
                return null;
            }
        }
        return SHADERS.get(filepath);
    }
}
