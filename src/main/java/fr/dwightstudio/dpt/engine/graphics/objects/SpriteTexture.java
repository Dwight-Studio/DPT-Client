package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

public class SpriteTexture {
    private final Vector2f[] textureCoords;
    private final Texture texture;

    public SpriteTexture(Texture texture, Vector2f[] textureCoords){
        this.texture = texture;
        this.textureCoords = textureCoords;
    }

    public Vector2f[] getTextureCoords() {
        return textureCoords;
    }

    public Texture getTexture() {
        return texture;
    }
}
