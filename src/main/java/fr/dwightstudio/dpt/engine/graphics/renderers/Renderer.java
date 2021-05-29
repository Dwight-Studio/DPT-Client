package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.List;

public class Renderer {
    private List<BatchRenderer> batchRenderers;

    public Renderer() {
        this.batchRenderers = new ArrayList<>();
    }

    public void addGameObject(GameObject gameObject) {

    }
}
