package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.primitives.Surface;
import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.List;

public class Renderer {
    private int maxBatchSize = 1000;
    private List<BatchRenderer> batchRenderers;

    public Renderer() {
        this.batchRenderers = new ArrayList<>();
    }

    public void addGameObject(GameObject gameObject) {
        List<Surface> surfaces = gameObject.getComponents(Surface.class);
        for (Surface surface : surfaces) {
            if (surface != null) {
                add(surface);
            }
        }
    }

    private void add(Surface surface) {
        boolean added = false;
        for (BatchRenderer batch : batchRenderers) {
            if (batch.hasRoom()) {
                batch.addSurface(surface);
                added = true;
            }
        }

        if (!added) {
            BatchRenderer batchRenderer = new BatchRenderer(maxBatchSize);
            batchRenderer.start();
            batchRenderers.add(batchRenderer);
            batchRenderer.addSurface(surface);
        }
    }

    public void render() {
        for (BatchRenderer batchRenderer : batchRenderers) {
            batchRenderer.render();
        }
    }

    public void setMaxBatchSize(int batchSize) {
        maxBatchSize = batchSize;
    }
}
