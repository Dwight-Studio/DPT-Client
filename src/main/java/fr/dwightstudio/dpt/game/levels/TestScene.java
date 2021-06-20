/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.DSEngine.Engine;
import fr.dwightstudio.dpt.DSEngine.graphics.objects.Camera;
import fr.dwightstudio.dpt.DSEngine.graphics.objects.Transform;
import fr.dwightstudio.dpt.DSEngine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.DSEngine.scripting.GameObject;
import fr.dwightstudio.dpt.DSEngine.scripting.Scene;
import org.joml.Vector2f;

public class TestScene extends Scene {

    Surface surface = new Surface(new Vector2f(100, 0), new Vector2f(64, 64), Engine.COLORS.MAGENTA);

    @Override
    public void init() {
        camera = new Camera(new Vector2f(0, 0));
        GameObject gameObject = new GameObject("test");

        gameObject.addComponent(surface);
        gameObject.addComponent(new Surface(new Vector2f(0, 0), new Vector2f(64, 64), Engine.COLORS.CYAN));
        addGameObject(gameObject);
    }

    @Override
    public void update(double dt) {
        surface.getTransform().setRotation(surface.getTransform().getRotation(Transform.DEGREE) + 1, Transform.DEGREE);
        super.update(dt);
    }
}
