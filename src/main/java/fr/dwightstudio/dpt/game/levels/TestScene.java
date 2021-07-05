/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dsengine.Engine;
import fr.dwightstudio.dsengine.graphics.objects.Camera;
import fr.dwightstudio.dsengine.graphics.objects.Transform;
import fr.dwightstudio.dsengine.graphics.primitives.Surface;
import fr.dwightstudio.dsengine.scripting.RenderGroup;
import fr.dwightstudio.dsengine.scripting.Scene;
import org.joml.Vector2f;

public class TestScene extends Scene {

    Surface surface = new Surface(new Vector2f(100, 0), new Vector2f(64, 64), Engine.COLOR.MAGENTA);

    @Override
    public void init() {
        camera = new Camera(new Vector2f(0, 0));
        RenderGroup renderGroup = new RenderGroup("test");

        renderGroup.addComponent(surface);
        renderGroup.addComponent(new Surface(new Vector2f(0, 0), new Vector2f(64, 64), Engine.COLOR.CYAN));
        addGameObject(renderGroup);
    }

    @Override
    public void update(double dt) {
        surface.getTransform().setRotation(surface.getTransform().getRotation(Transform.DEGREE) + 1, Transform.DEGREE);
        super.update(dt);
    }
}
