package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.gui.events.GUIButtonEvent;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

import java.util.ArrayList;
import java.util.List;

public class Button extends Component {

    private static List<GUIButtonEvent> listeners = new ArrayList<>();
    private static int currentID = 0;
    private final int ID;
    private boolean clicked = false;

    public Button(Vector2f position, Vector2f size, Color color) {
        this.ID = currentID;
        currentID++;
    }

    public int getID() {
        return this.ID;
    }

    public void addEventListener(GUIButtonEvent guiButtonEvent) {
        listeners.add(guiButtonEvent);
    }

    @Override
    public void update(float dt) {
        if (MouseListener.isButtonPressed(0)) {
            setClicked(true);
        } else {
            setClicked(false);
        }
    }

    private void setClicked(boolean clicked) {
        this.clicked = clicked;
        if (this.clicked) {
            for (GUIButtonEvent guiButtonEvent : listeners) {
                guiButtonEvent.onClick(this.ID);
            }
        }
    }
}
