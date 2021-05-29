package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

public class ResourceManager {

    private static final Map<String, TypeHandler<?>> HANDLERS = new HashMap<>();
    private static final Map<String, Supplier<?>> RESOURCES = new HashMap<>();

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
                return (T) RESOURCES.get(filepath).get();
            } catch (ClassCastException ignored) {
                GameLogger.getLogger("ResourceManager").error(MessageFormat.format("Trying to get unloaded resource '{0}'", filepath));
                return null;
            }
        }
        return null;
    }

    public static boolean load(String filepath, String type) {
        if (HANDLERS.containsKey(type.toLowerCase())) {
            TypeHandler<?> handler = HANDLERS.get(type.toLowerCase());
            if (handler.get(filepath) != null) {
                RESOURCES.put(filepath, () -> handler.get(filepath));
                return true;
            } else {
                GameLogger.getLogger("ResourceManager").warn(MessageFormat.format("Handler '{0}' has returned Null for '{1}'", type.toLowerCase(), filepath));
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
    public static void addHandler(String type, TypeHandler<?> typeHandler) {
        HANDLERS.put(type.toLowerCase(), typeHandler);
    }
}
