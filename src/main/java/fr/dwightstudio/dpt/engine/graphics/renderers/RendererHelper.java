package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RendererHelper {
    private int maxBatchSize = 1000;
    private List<SurfaceRenderer> surfaceRenderers;
    private List<LineRenderer> lineRenderers;

    /**
     * Create a new RendererHelper
     *
     * This is main renderer, you should use it in every Scenes you make or at least on every scene where you need to
     * renderer Surfaces, Lines etc...
     */
    public RendererHelper() {
        this.surfaceRenderers = new ArrayList<>();
        this.lineRenderers = new ArrayList<>();
    }

    /**
     * Add a GameObject to be rendered in the Renderer
     *
     * @param gameObject a GameObject
     */
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

    /**
     * Add a surface to the Renderer
     *
     * @param surface a Surface
     * @param gameObject a GameObject
     */
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

    /**
     * Add a Line to the renderer
     *
     * @param line a Line
     */
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

    /**
     * This is called every frame to render all objects contained into every Renderers
     */
    public void render() {
        for (SurfaceRenderer surfaceRenderer : surfaceRenderers) {
            surfaceRenderer.render();
        }
        for (LineRenderer lineRenderer : lineRenderers) {
            lineRenderer.render();
        }
    }

    /**
     * Change the number of objects that one renderer can have
     *
     * @param batchSize the new batch size
     */
    public void setMaxBatchSize(int batchSize) {
        maxBatchSize = batchSize;
    }
}
