package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.objects.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;

import java.util.HashMap;
import java.util.Map;

public class SpritesheetHandler implements TypeHandler<Spritesheet> {

    private static final Map<String, Spritesheet> SPRITESHEETS = new HashMap<>();

    @Override
    public Spritesheet get(String filepath) {
        if (!SPRITESHEETS.containsKey(filepath)) {
            Spritesheet spritesheet = SpritesheetLoader.loadSpritesheet(filepath);
            if (spritesheet != null) {
                SPRITESHEETS.put(filepath, spritesheet);
            } else {
                return null;
            }
        }
        return SPRITESHEETS.get(filepath);
    }
}
