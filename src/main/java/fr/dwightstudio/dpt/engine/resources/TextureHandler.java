package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureUtils;

import java.util.HashMap;
import java.util.Map;

public class TextureHandler implements TypeHandler<Texture> {

    private static final Map<String, Texture> TEXTURES = new HashMap<>();

    @Override
    public Texture get(String filepath) {
        if (!TEXTURES.containsKey(filepath)) {
            Texture texture = TextureUtils.loadTexture(filepath);
            if (texture != null) {
                TEXTURES.put(filepath, texture);
            } else {
                return null;
            }
        }
        return TEXTURES.get(filepath);
    }
}
