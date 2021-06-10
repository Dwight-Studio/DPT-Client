package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.graphics.gui.Button;

/**
 * Event fired when a Button is clicked
 */
public class ButtonClickEvent extends ButtonEvent {

    public ButtonClickEvent(Button button) {
        super(button);
    }

}
