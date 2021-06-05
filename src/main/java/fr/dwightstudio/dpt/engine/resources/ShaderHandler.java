package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;

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
