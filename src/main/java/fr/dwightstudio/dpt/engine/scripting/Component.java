/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.scripting;

public abstract class Component {

    public GameObject gameObject = null;
    private boolean gameObjectDirty = false;

    public void update(double dt) {}
    protected void setGameobjectDirty() {
        gameObjectDirty = true;
    }
    public void markGameObjectClean() {
        gameObjectDirty = false;
    }
    public boolean isGameObjectDirty() {
        return gameObjectDirty;
    }
    public void remove() {}

    public void init() {}
}
