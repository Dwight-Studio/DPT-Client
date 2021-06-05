package fr.dwightstudio.dpt.engine.graphics.objects;

public class Sprite {

    private Texture texture;
    private SpriteTexture spriteTexture;

    public Sprite(Texture texture) {
        this.texture = texture;
    }

    public Sprite(SpriteTexture spriteTexture) {
        this.spriteTexture = spriteTexture;
    }
}
