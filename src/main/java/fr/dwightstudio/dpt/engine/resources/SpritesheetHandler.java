package fr.dwightstudio.dpt.engine.resources;

import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;

public class SpritesheetHandler implements TypeHandler<Spritesheet> {

    @Override
    public Spritesheet get(String filepath) {
        return SpritesheetLoader.loadSpritesheet(filepath);
    }
}
