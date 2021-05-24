package fr.dwightstudio.dpt.engine.graphics.render;

import java.util.List;

public class Spritesheet {

    private final Texture texture;
    private final List<Sprite> sprites;

    public Spritesheet(Texture texture, List<Sprite> sprites) {
        this.texture = texture;
        this.sprites = sprites;
    }

    public Sprite getSprite(int index) {
        return sprites.get(index);
    }

    public Texture getTexture() {
        return texture;
    }

}
