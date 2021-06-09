package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.events.types.gui.GUIEvent;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;

public class ButtonEvent extends GUIEvent {

    private final Button button;

    public ButtonEvent(Button button) {
        this.button = button;
    }

    public Button getButton() {
        return button;
    }
}
