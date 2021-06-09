package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Renderer {
    private int maxBatchSize = 1000;
    private List<SurfaceRenderer> surfaceRenderers;
    private List<LineRenderer> lineRenderers;

    public Renderer() {
        this.surfaceRenderers = new ArrayList<>();
        this.lineRenderers = new ArrayList<>();
    }

    public void addGameObject(GameObject gameObject) {
        List<Surface> surfaces = gameObject.getComponents(Surface.class);
        for (Surface surface : surfaces) {
            if (surface != null) {
                add(surface, gameObject);
            }
        }
        List<Line> lines = gameObject.getComponents(Line.class);
        for (Line line : lines) {
            if (line != null) {
                add(line);
            }
        }
    }

    private void add(Surface surface, GameObject gameObject) {
        boolean added = false;
        for (SurfaceRenderer batch : surfaceRenderers) {
            if (batch.hasRoom() && batch.getzIndex() == gameObject.getzIndex()) {
                batch.addSurface(surface);
                added = true;
            }
        }

        if (!added) {
            SurfaceRenderer surfaceRenderer = new SurfaceRenderer(maxBatchSize, gameObject.getzIndex());
            surfaceRenderer.start();
            surfaceRenderers.add(surfaceRenderer);
            surfaceRenderer.addSurface(surface);
            Collections.sort(surfaceRenderers);
        }
    }

    private void add(Line line) {
        boolean added = false;
        for (LineRenderer batch : lineRenderers) {
            if (batch.hasRoom()) {
                batch.addLine(line);
                added = true;
            }
        }

        if (!added) {
            LineRenderer lineRenderer = new LineRenderer(maxBatchSize);
            lineRenderer.start();
            lineRenderers.add(lineRenderer);
            lineRenderer.addLine(line);
        }
    }

    public void render() {
        for (SurfaceRenderer surfaceRenderer : surfaceRenderers) {
            surfaceRenderer.render();
        }
        for (LineRenderer lineRenderer : lineRenderers) {
            lineRenderer.render();
        }
    }

    public void setMaxBatchSize(int batchSize) {
        maxBatchSize = batchSize;
    }
}
