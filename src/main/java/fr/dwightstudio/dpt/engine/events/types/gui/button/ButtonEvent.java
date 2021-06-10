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
