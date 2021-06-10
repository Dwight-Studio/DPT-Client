package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.graphics.gui.Button;

/**
 * Event fired when a Button is released
 */
public class ButtonReleaseEvent extends ButtonEvent {

    private final double clickMillis;

    public ButtonReleaseEvent(Button button, double clickMillis) {
        super(button);
        this.clickMillis = clickMillis;
    }

    /**
     * @return the time when the Button was released
     */
    public double getClickMillis() {
        return clickMillis;
    }
}
