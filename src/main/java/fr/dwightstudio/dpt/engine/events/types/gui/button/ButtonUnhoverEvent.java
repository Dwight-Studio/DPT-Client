package fr.dwightstudio.dpt.engine.events.types.gui.button;

import fr.dwightstudio.dpt.engine.graphics.gui.Button;

/**
 * Event fired when a Button that was hover is 'unhover'
 */
public class ButtonUnhoverEvent extends ButtonEvent {
    public ButtonUnhoverEvent(Button button) {
        super(button);
    }
}
