package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.Vector2f;

public class SpriteTexture {
    private final Vector2f[] textureCoords;
    private final Texture texture;

    /**
     * Create a new SpriteTexture
     *
     * @param texture the Spritsheet Texture containing this SpriteTexture
     * @param textureCoords the Texture coordinates of this SpriteTexture
     */
    public SpriteTexture(Texture texture, Vector2f[] textureCoords){
        this.texture = texture;
        this.textureCoords = textureCoords;
    }

    /**
     * @return the Texture coordinates of this SpriteTexture
     */
    public Vector2f[] getTextureCoords() {
        return textureCoords;
    }

    /**
     * @return the Spritesheet Texture containing this SpriteTexture
     */
    public Texture getTexture() {
        return texture;
    }
}
