package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.render.Shader;
import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;

public class ShaderHandler implements TypeHandler<Shader> {
    @Override
    public Shader get(String filepath) {
        return ShaderLoader.loadShaderFile(filepath);
    }
}
