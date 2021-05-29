package fr.dwightstudio.dpt.engine.graphics.render;

import java.util.List;

public class Spritesheet {

    private final Texture texture;
    private final List<SpriteTexture> sprites;

    public Spritesheet(Texture texture, List<SpriteTexture> sprites) {
        this.texture = texture;
        this.sprites = sprites;
    }

    public SpriteTexture getSprite(int index) {
        return sprites.get(index);
    }

    public Texture getTexture() {
        return texture;
    }

}
