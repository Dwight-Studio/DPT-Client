package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

public class Sprite extends Component {

    // TODO: Spritesheet system review. Sprite creation in it not appropriate. I don't what to do for that.

    private Texture texture;
    private Vector2f[] textureCoords;

    public Sprite(Texture texture) {
        this.texture = texture;
    }

    public Sprite(Texture texture, Vector2f[] textureCoords) {

    }

    @Override
    public void init() {

    }

    @Override
    public void update(float dt) {

    }
}
