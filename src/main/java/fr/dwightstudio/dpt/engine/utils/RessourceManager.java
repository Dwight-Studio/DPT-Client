package fr.dwightstudio.dpt.engine.utils;

import fr.dwightstudio.dpt.engine.graphics.render.Shader;
import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;

import java.util.HashMap;
import java.util.Map;

public class RessourceManager {

    public static Map<String, Texture> textures = new HashMap<>();
    public static Map<String, Shader> shaders = new HashMap<>();
    public static Map<String, Spritesheet> spritesheets = new HashMap<>();

    public static Texture getTexture(String filepath) {
        if (!textures.containsKey(filepath)) {
            textures.put(filepath, TextureLoader.loadTexture(filepath));
        }
        return textures.get(filepath);
    }

    public static Shader getShader(String filepath) {
        if (!shaders.containsKey(filepath)) {
            shaders.put(filepath, ShaderLoader.loadShaderFile(filepath));
        }
        return shaders.get(filepath);
    }

    public static Spritesheet getSpritsheet(String filepath, int numberOfSprite, int spriteWidth, int spriteHeight, int widthSpacing, int heightSpacing) {
        if (!spritesheets.containsKey(filepath)) {
            spritesheets.put(filepath, SpritesheetLoader.loadSpritesheet(filepath, numberOfSprite, spriteWidth, spriteHeight, widthSpacing, heightSpacing));
        }
        return spritesheets.get(filepath);
    }
}
