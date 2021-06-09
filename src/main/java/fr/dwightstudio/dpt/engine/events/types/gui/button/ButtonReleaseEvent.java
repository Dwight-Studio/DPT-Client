package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.graphics.gui.Button;

public class ButtonReleaseEvent extends ButtonEvent {

    private final double clickMillis;

    public ButtonReleaseEvent(Button button, double clickMillis) {
        super(button);
        this.clickMillis = clickMillis;
    }

    public double getClickMillis() {
        return clickMillis;
    }
}
