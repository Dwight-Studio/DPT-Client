package fr.dwightstudio.dpt.engine.primitives;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.Transform;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

public class Surface extends Component {

    private Color color;
    private Transform transform = new Transform();
    private Transform lastTransform;
    private Texture texture;
    private Vector2f[] textureCoords;

    private boolean dirty = false;

    public Surface(float x, float y, float xScale, float yScale, Texture texture, Vector2f[] textureCoords) {
        this.color = new Color(1, 1, 1, 1);
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(xScale, yScale);
        this.lastTransform = new Transform();
        this.texture = texture;
        this.textureCoords = textureCoords;
    }

    public Surface(float x, float y, float xScale, float yScale, Color color) {
        this.color = color;
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(xScale, yScale);
        this.lastTransform = new Transform();
        this.texture = null;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 1),
                new Vector2f(1, 0),
                new Vector2f(0, 0),
                new Vector2f(0, 1)
        };
    }

    public Surface(float x, float y, float xScale, float yScale, Texture texture) {
        this.color = new Color(1, 1, 1, 1);
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(xScale, yScale);
        this.lastTransform = new Transform();
        this.texture = texture;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 1),
                new Vector2f(1, 0),
                new Vector2f(0, 0),
                new Vector2f(0, 1)
        };
    }

    public Surface(float x, float y, float scale, Color color) {
        this.color = color;
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(scale, scale);
        this.lastTransform = new Transform();
        this.texture = null;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 1),
                new Vector2f(1, 0),
                new Vector2f(0, 0),
                new Vector2f(0, 1)
        };
    }

    public Surface(float x, float y, float scale, Texture texture) {
        this.color = new Color(1, 1, 1, 1);
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(scale, scale);
        this.lastTransform = new Transform();
        this.texture = texture;
        this.textureCoords = new Vector2f[]{
                new Vector2f(1, 1),
                new Vector2f(1, 0),
                new Vector2f(0, 0),
                new Vector2f(0, 1)
        };
    }

    @Override
    public void init() {

    }

    @Override
    public void update(float dt) {
        if (!this.lastTransform.equals(this.transform)) {
            this.lastTransform = this.transform.copy();
            dirty = true;
        }
    }

    public Color getColor() {
        return color;
    }

    public Transform getTransform() {
        return transform;
    }

    public Vector2f getPosition() {
        return transform.position;
    }

    public Vector2f getScale() {
        return transform.scale;
    }

    public Texture getTexture() {
        return texture;
    }

    public Vector2f[] getTextureCoords() {
        return textureCoords;
    }

    public void setColor(Color newColor) {
        if (!newColor.equals(this.color)) {
            this.color = newColor;
            this.dirty = true;
        }
    }

    public void setTransform(Transform transform) {
        this.transform = transform;
        this.dirty = true;
    }

    public void setPosition(Vector2f position) {
        this.transform.position.set(position);
        this.dirty = true;
    }

    public void setScale(Vector2f scale) {
        this.transform.scale.set(scale);
        this.dirty = true;
    }

    public void setTexture(Texture texture) {
        if (!texture.equals(this.texture)) {
            this.texture = texture;
            this.color = new Color(1, 1, 1,1);
            this.dirty = true;
        }
    }

    public void setTextureCoords(Vector2f[] textureCoords) {
        if (!textureCoords.equals(this.textureCoords)) {
            this.textureCoords = textureCoords;
            this.dirty = true;
        }
    }

    public boolean isDirty() {
        return dirty;
    }

    public void markClean() {
        dirty = false;
    }
}
