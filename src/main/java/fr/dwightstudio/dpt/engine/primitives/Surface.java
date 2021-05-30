package fr.dwightstudio.dpt.engine.primitives;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.Transform;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

public class Surface extends Component {

    private Color color;
    private Transform transform = new Transform();
    private Texture texture;

    public Surface(float x, float y, float xScale, float yScale, Color color) {
        this.color = color;
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(xScale, yScale);
        this.texture = null;
    }

    public Surface(float x, float y, float xScale, float yScale, Texture texture) {
        this.color = new Color(1, 1, 1, 1);
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(xScale, yScale);
        this.texture = texture;
    }

    public Surface(float x, float y, float scale, Color color) {
        this.color = color;
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(scale, scale);
        this.texture = null;
    }

    public Surface(float x, float y, float scale, Texture texture) {
        this.color = new Color(1, 1, 1, 1);
        this.transform.position = new Vector2f(x, y);
        this.transform.scale = new Vector2f(scale, scale);
        this.texture = texture;
    }

    @Override
    public void init() {

    }

    @Override
    public void update(float dt) {

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


    public void setColor(Color newColor) {
        this.color = newColor;
    }

    public void setTransform(Transform transform) {
        this.transform = transform;
    }

    public void setPosition(Vector2f position) {
        this.transform.position = position;
    }

    public void setScale(Vector2f scale) {
        this.transform.scale = scale;
    }

    public void setTexture(Texture texture) {
        this.texture = texture;
    }
}
