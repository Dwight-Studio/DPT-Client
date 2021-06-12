/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;

public class TestScene extends Scene {

    private GameObject tiles;

    public TestScene() {

    }

    @Override
    public void init() {
        this.tiles = new GameObject("tiles", 0);
        //this.tiles.addComponent(new Tile(100, 100, 32, new Color(0, 1, 1, 1)));
        this.addGameObject(tiles);
    }

    @Override
    public void update(float dt) {
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }
    }
}
