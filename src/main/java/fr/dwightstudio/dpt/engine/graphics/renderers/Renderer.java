package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.List;

public class Renderer {
    private int maxBatchSize = 1000;
    private List<SurfaceBatchRenderer> surfaceBatchRenderers;
    private List<LineBatchRenderer> lineBatchRenderers;

    public Renderer() {
        this.surfaceBatchRenderers = new ArrayList<>();
        this.lineBatchRenderers = new ArrayList<>();
    }

    public void addGameObject(GameObject gameObject) {
        List<Surface> surfaces = gameObject.getComponents(Surface.class);
        for (Surface surface : surfaces) {
            if (surface != null) {
                add(surface);
            }
        }
        List<Line> lines = gameObject.getComponents(Line.class);
        for (Line line : lines) {
            if (line != null) {
                add(line);
            }
        }
    }

    private void add(Surface surface) {
        boolean added = false;
        for (SurfaceBatchRenderer batch : surfaceBatchRenderers) {
            if (batch.hasRoom()) {
                batch.addSurface(surface);
                added = true;
            }
        }

        if (!added) {
            SurfaceBatchRenderer surfaceBatchRenderer = new SurfaceBatchRenderer(maxBatchSize);
            surfaceBatchRenderer.start();
            surfaceBatchRenderers.add(surfaceBatchRenderer);
            surfaceBatchRenderer.addSurface(surface);
        }
    }

    private void add(Line line) {
        boolean added = false;
        for (LineBatchRenderer batch : lineBatchRenderers) {
            if (batch.hasRoom()) {
                batch.addLine(line);
                added = true;
            }
        }

        if (!added) {
            LineBatchRenderer lineBatchRenderer = new LineBatchRenderer(maxBatchSize);
            lineBatchRenderer.start();
            lineBatchRenderers.add(lineBatchRenderer);
            lineBatchRenderer.addLine(line);
        }
    }

    public void render() {
        for (SurfaceBatchRenderer surfaceBatchRenderer : surfaceBatchRenderers) {
            surfaceBatchRenderer.render();
        }
        for (LineBatchRenderer lineBatchRenderer : lineBatchRenderers) {
            lineBatchRenderer.render();
        }
    }

    public void setMaxBatchSize(int batchSize) {
        maxBatchSize = batchSize;
    }
}
