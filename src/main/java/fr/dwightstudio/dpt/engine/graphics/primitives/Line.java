package fr.dwightstudio.dpt.engine.graphics.primitives;

import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

public class Line extends Component {

    private Vector2f startPosition;
    private Vector2f endPosition;
    private float thickness;
    private Color color;
    private boolean dirty = true;

    public Line(Vector2f startPosition, Vector2f endPosition, Color color, float thickness) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = color;
        this.thickness = thickness;
    }

    public Line(Vector2f startPosition, Vector2f endPosition, Color color) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = color;
        this.thickness = 1.0f;
    }

    public Line(Vector2f startPosition, Vector2f endPosition, float thickness) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.thickness = thickness;
    }

    public Line(Vector2f startPosition, Vector2f endPosition) {
        this.startPosition = startPosition;
        this.endPosition = endPosition;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.thickness = 1.0f;
    }

    public Vector2f getStartPosition() {
        return startPosition;
    }

    public Vector2f getEndPosition() {
        return endPosition;
    }

    public Color getColor() {
        return color;
    }

    public float getThickness() {
        return thickness;
    }

    public void setColor(Color newColor) {
        if (!this.color.equals(newColor)) {
            this.color = newColor;
            dirty = true;
        }
    }

    public void setStartPosition(Vector2f newPosition) {
        if (!this.startPosition.equals(newPosition)) {
            this.startPosition = newPosition;
            dirty = true;
        }
    }

    public void setEndPosition(Vector2f newPosition) {
        if (!this.endPosition.equals(newPosition)) {
            this.endPosition = newPosition;
            dirty = true;
        }
    }

    public void setThickness(float newThickness) {
        if (this.thickness != newThickness) {
            this.thickness = newThickness;
            dirty = true;
        }
    }

    public boolean isDirty() {
        return dirty;
    }

    public void markClean() {
        dirty = false;
    }

    @Override
    public void update(float dt) {

    }
}
