package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;

import java.util.HashMap;
import java.util.Map;

public class FontAtlasHandler implements TypeHandler<FontAtlas> {

    private static final Map<String, FontAtlas> FONT_ATLAS = new HashMap<>();

    @Override
    public FontAtlas get(String filepath) {
        if (!FONT_ATLAS.containsKey(filepath)) {
            FontAtlas fontAtlas = null;
            if (fontAtlas != null) {
                FONT_ATLAS.put(filepath, fontAtlas);
            } else {
                return null;
            }
        }
        return FONT_ATLAS.get(filepath);
    }
}
