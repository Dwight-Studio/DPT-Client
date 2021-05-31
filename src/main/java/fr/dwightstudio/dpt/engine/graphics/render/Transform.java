package fr.dwightstudio.dpt.engine.graphics.render;

import org.joml.Vector2f;

public class Transform {
    public Vector2f position;
    public Vector2f scale;
    public float rotation;

    public Transform() {
        this.position = new Vector2f();
        this.scale = new Vector2f();
        this.rotation = 0.0f;
    }

    public Transform(Vector2f position) {
        this.position = position;
        this.scale = new Vector2f();
        this.rotation = 0.0f;
    }

    public Transform(float rotation) {
        this.position = new Vector2f();
        this.scale = new Vector2f();
        this.rotation = rotation;
    }

    public Transform(Vector2f position, Vector2f scale) {
        this.position = position;
        this.scale = scale;
        this.rotation = 0.0f;
    }

    public Transform(Vector2f position, float rotation) {
        this.position = position;
        this.scale = new Vector2f();
        this.rotation = rotation;
    }

    public Transform(Vector2f position, Vector2f scale, float rotation) {
        this.position = position;
        this.scale = scale;
        this.rotation = rotation;
    }

    public Transform copy() {
        return new Transform(new Vector2f(this.position), new Vector2f(this.scale));
    }

    @Override
    public boolean equals(Object object) {
        if (object == null) return false;
        if (!(object instanceof Transform)) return false;

        Transform transform = (Transform) object;

        return transform.position.equals(this.position) && transform.scale.equals(this.scale) && transform.rotation == this.rotation;
    }
}
