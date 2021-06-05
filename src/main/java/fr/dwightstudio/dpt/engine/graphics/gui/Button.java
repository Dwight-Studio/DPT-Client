package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.events.types.ButtonClickEvent;
import fr.dwightstudio.dpt.engine.events.types.ButtonReleaseEvent;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import org.joml.Vector2f;

import java.util.HashSet;

import static org.lwjgl.glfw.GLFW.glfwGetTime;

public class Button extends Surface {

    private boolean clicked = false;
    private Vector2f position;
    private Vector2f scale;
    private Color color;
    private double clickMillis;

    private static final HashSet<Button> buttonsList = new HashSet<>();

    public Button(Vector2f position, Vector2f scale, Color color) {
        super(position, scale, color);
        this.position = position;
        this.scale = scale;
        this.color = color;
        buttonsList.add(this);
    }

    private void setClicked(boolean clicked) {
        if (!this.clicked && clicked) {
            this.clickMillis = glfwGetTime();
            EventSystem.fire(new ButtonClickEvent(this));
        } else if (this.clicked && !clicked) {
            EventSystem.fire(new ButtonReleaseEvent(this, this.clickMillis));
        }
        this.clicked = clicked;
    }

    private void checkClick() {
        if (MouseListener.isButtonPressed(0)) {
            if (MouseListener.getCursorPos().x >= this.position.x && MouseListener.getCursorPos().x <= this.position.x + this.scale.x) {
                if (MouseListener.getCursorPos().y >= this.position.y && MouseListener.getCursorPos().y <= this.position.y + this.scale.y) {
                    setClicked(true);
                    return;
                }
            }
        }
        setClicked(false);
    }

    public static void checkClickAll() {
        for (Button button : buttonsList) {
            button.checkClick();
        }
    }

    public void remove() {
        buttonsList.remove(this);
    }
}