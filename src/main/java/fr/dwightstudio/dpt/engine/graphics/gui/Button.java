package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.events.EventHandler;
import fr.dwightstudio.dpt.engine.events.EventSystemI;
import fr.dwightstudio.dpt.engine.events.GUIButtonEvent;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import org.joml.Vector2f;

import java.util.ArrayList;
import java.util.List;

public class Button extends Surface implements EventSystemI {

    private static int currentID = 0;
    private long ID;
    private boolean clicked = false;
    private Vector2f position;
    private Vector2f scale;
    private Color color;

    private final EventHandler buttonEventHandler = new EventHandler(this);
    private List<GUIButtonEvent> buttonEvents = new ArrayList<>();

    public Button(Vector2f position, Vector2f scale, Color color) {
        super(position, scale, color);
        this.position = position;
        this.scale = scale;
        this.color = color;
    }

    @Override
    public void init() {
        this.ID = currentID;
        currentID++;
    }

    public long getID() {
        return this.ID;
    }

    public void addEventListener(GUIButtonEvent guiButtonEvent) {
        buttonEvents.add(guiButtonEvent);
    }

    private void setClicked(boolean clicked) {
        this.clicked = clicked;
        if (this.clicked) {
            for (GUIButtonEvent guiButtonEvent : buttonEvents) {
                guiButtonEvent.onClick(this.ID);
            }
        }
    }

    @Override
    public void eventUpdate() {
        if (MouseListener.isButtonPressed(0)) {
            if (MouseListener.getCursorPos().x >= this.position.x && MouseListener.getCursorPos().x <= this.position.x + this.scale.x) {
                if (MouseListener.getCursorPos().y >= this.position.y && MouseListener.getCursorPos().y <= this.position.y + this.scale.y) {
                    setClicked(true);
                }
            }
        }
        setClicked(false);
    }
}
