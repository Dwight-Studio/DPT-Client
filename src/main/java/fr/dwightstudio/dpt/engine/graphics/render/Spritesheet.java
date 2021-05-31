package fr.dwightstudio.dpt.engine.graphics.render;

import java.util.List;

public class Spritesheet {

    private final Texture texture;
    private final List<SpriteTexture> spriteTextures;

    public Spritesheet(Texture texture, List<SpriteTexture> sprites) {
        this.texture = texture;
        this.spriteTextures = sprites;
    }

    public SpriteTexture getSprite(int index) {
        return spriteTextures.get(index);
    }

    public Texture getTexture() {
        return texture;
    }

    public int getNumberOfSprite() {
        return spriteTextures.size();
    }
}
