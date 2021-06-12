/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.graphics.gui.Button;

/**
 * Event fired when the mouse hover a Button object
 */
public class ButtonHoverEvent extends ButtonEvent{

    public ButtonHoverEvent(Button button) {
        super(button);
    }
}
