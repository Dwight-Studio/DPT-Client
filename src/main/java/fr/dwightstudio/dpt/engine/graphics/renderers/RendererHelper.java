/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.scripting.GameObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RendererHelper {
    private int maxBatchSize = 1000;
    private List<SurfaceRenderer> surfaceRenderers;

    /**
     * Create a new RendererHelper
     *
     * This is main renderer, you should use it in every Scenes you make or at least on every scene where you need to
     * renderer Surfaces, Lines etc...
     */
    public RendererHelper() {
        this.surfaceRenderers = new ArrayList<>();
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
     * This is called every frame to render all objects contained into every Renderers
     */
    public void render() {
        for (SurfaceRenderer surfaceRenderer : surfaceRenderers) {
            surfaceRenderer.render();
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
