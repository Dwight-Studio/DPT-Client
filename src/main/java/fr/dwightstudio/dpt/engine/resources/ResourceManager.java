package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;

import java.util.HashMap;
import java.util.Map;

public class ResourceManager {

    private static final Map<String, TypeHandler<?>> HANDLERS = new HashMap<>();
    private static final Map<String, String> RESOURCES = new HashMap<>();

    static {
        addHandler("texture", new TextureHandler());
        addHandler("shader", new ShaderHandler());
        addHandler("spritesheet", new SpritesheetHandler());
    }

    /**
     * Gets a resource
     *
     * @param filepath the filepath of the resource
     * @param <T> the type of the resource
     * @return the resource if found, otherwise null
     */
    public static <T> T get(String filepath) {
        if (RESOURCES.containsKey(filepath)) {
            try {
                return (T) HANDLERS.get(RESOURCES.get(filepath)).get(filepath);
            } catch (ClassCastException ignored) {
                return null;
            }
        }
        return null;
    }

    /**
     * Adds a type handler to handle specified resources
     *
     * @param type the identifier of the type
     * @param typeHandler the handler
     */
    public static void addHandler(String type, TypeHandler<?> typeHandler) {
        HANDLERS.put(type.toUpperCase(), typeHandler);
    }
}
