package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import org.lwjgl.stb.STBImage;

import java.util.HashMap;
import java.util.Map;

public class TextureHandler implements TypeHandler<Texture> {

    private static final Map<String, Texture> TEXTURES = new HashMap<>();

    @Override
    public Texture get(String filepath) {
        if (!TEXTURES.containsKey(filepath)) {
            Texture texture = TextureLoader.loadTexture(filepath);
            if (texture != null) {
                TEXTURES.put(filepath, texture);
            } else {
                return null;
            }
        }
        return TEXTURES.get(filepath);
    }
}
