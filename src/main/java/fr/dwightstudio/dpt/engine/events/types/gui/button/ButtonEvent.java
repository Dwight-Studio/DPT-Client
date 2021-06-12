/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.events.types.gui.GUIEvent;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;

/**
 * Parent event for ButtonClickEvent or ButtonReleaseEvent etc...
 */
public class ButtonEvent extends GUIEvent {

    private final Button button;

    public ButtonEvent(Button button) {
        this.button = button;
    }

    /**
     * @return a Button object
     */
    public Button getObject() {
        return button;
    }
}
