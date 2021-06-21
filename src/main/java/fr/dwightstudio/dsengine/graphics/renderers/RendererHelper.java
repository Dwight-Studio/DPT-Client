/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.renderers;

import fr.dwightstudio.dsengine.graphics.gui.Label;
import fr.dwightstudio.dsengine.graphics.primitives.Surface;
import fr.dwightstudio.dsengine.scripting.GameObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RendererHelper {
    private int maxBatchSize = 1000;
    private final List<Renderers> renderers;

    /**
     * Create a new RendererHelper
     *
     * This is main renderer, you should use it in every Scenes you make or at least on every scene where you need to
     * renderer Surfaces, Lines etc...
     */
    public RendererHelper() {
        this.renderers = new ArrayList<>();
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
        List<Label> labels = gameObject.getComponents(Label.class);
        for (Label label : labels) {
            if (label.getTextRenderer() != null) {
                this.renderers.add(label.getTextRenderer());
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
        for (Renderers renderer : renderers) {
            if (renderer instanceof SurfaceRenderer) {
                SurfaceRenderer surfaceRenderer = (SurfaceRenderer) renderer;
                if (surfaceRenderer.hasRoom() && surfaceRenderer.getzIndex() == gameObject.getzIndex()) {
                    surfaceRenderer.addSurface(surface);
                    added = true;
                }
            }
        }

        if (!added) {
            SurfaceRenderer surfaceRenderer = new SurfaceRenderer(maxBatchSize, gameObject.getzIndex());
            surfaceRenderer.start();
            renderers.add(surfaceRenderer);
            surfaceRenderer.addSurface(surface);
        }
    }

    /**
     * This is called every frame to render all objects contained into every Renderers
     */
    public void render() {
        Collections.sort(renderers);
        for (Renderers renderer : renderers) {
            renderer.render();
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
