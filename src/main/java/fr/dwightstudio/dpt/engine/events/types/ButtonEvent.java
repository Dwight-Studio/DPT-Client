package fr.dwightstudio.dpt.engine.events.types;

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
