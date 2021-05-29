package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

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
