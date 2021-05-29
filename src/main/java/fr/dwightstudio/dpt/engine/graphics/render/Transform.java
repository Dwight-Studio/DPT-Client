package fr.dwightstudio.dpt.engine.graphics.render;

import org.joml.Vector2f;

public class Transform {
    public Vector2f position;
    public Vector2f scale;

    public Transform() {
        this.position = new Vector2f();
        this.scale = new Vector2f();
    }

    public Transform(Vector2f position) {
        this.position = position;
        this.scale = new Vector2f();
    }

    public Transform(Vector2f position, Vector2f scale) {
        this.position = position;
        this.scale = scale;
    }
}
