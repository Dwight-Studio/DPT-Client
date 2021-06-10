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
