/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.objects.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

public class ResourceManager {

    private static final Map<Class<?>, TypeHandler<?>> HANDLERS = new HashMap<>();
    private static final Map<String, Supplier<?>> RESOURCES = new HashMap<>();

    static {
        addHandler(Texture.class, new TextureHandler());
        addHandler(Shader.class, new ShaderHandler());
        addHandler(Spritesheet.class, new SpritesheetHandler());
    }

    /**
     * Gets a resource
     *
     * You can get a resource after loading it
     *
     * @param filepath the filepath of the resource
     * @param <T> the type of the resource
     * @return the resource if found, otherwise null
     */
    public static <T> T get(String filepath) {
        if (RESOURCES.containsKey(filepath)) {
            try {
                return (T) RESOURCES.get(filepath).get();
            } catch (ClassCastException ignored) {
                GameLogger.getLogger("ResourceManager").error(MessageFormat.format("Trying to get unloaded resource \"{0}\"", filepath));
                return null;
            }
        }
        return null;
    }

    // You have to load the resource before using it
    public static boolean load(String filepath, Class<?> type) {
        if (HANDLERS.containsKey(type)) {
            TypeHandler<?> handler = HANDLERS.get(type);
            if (handler.get(filepath) != null) {
                RESOURCES.put(filepath, () -> handler.get(filepath));
                return true;
            } else {
                GameLogger.getLogger("ResourceManager").warn(MessageFormat.format("Handler '{0}' has returned Null for '{1}'", type, filepath));
                return false;
            }
        } else {
            GameLogger.getLogger("ResourceManager").warn(MessageFormat.format("Can't find handler for '{0}'", filepath));
            return false;
        }
    }

    /**
     * Adds a type handler to handle specified resources
     *
     * @param type the identifier of the type
     * @param typeHandler the handler
     */
    public static void addHandler(Class<?> type, TypeHandler<?> typeHandler) {
        HANDLERS.put(type, typeHandler);
    }
}
