/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonClickEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonHoverEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonReleaseEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonUnhoverEvent;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import org.joml.Vector2f;

import java.util.HashSet;

import static org.lwjgl.glfw.GLFW.glfwGetTime;

public class Button extends Surface {

    protected boolean clicked = false;
    protected boolean hover = false;
    private double clickMillis;
    private Spritesheet buttonSpritesheet;

    private static final HashSet<Button> buttonsList = new HashSet<>();

    /**
     * Create a new Button
     *
     * @param position the on-screen position
     * @param scale the scale of the Button
     * @param color the color of the Button
     */
    public Button(Vector2f position, Vector2f scale, Color color) {
        super(position, scale, color);
        buttonsList.add(this);
    }

    /**
     * Create a Button
     *
     * NOTE: All the Textures will be scaled according to the scale parameters
     * The Spritesheet must contain at least 1 picture
     * The Spritesheet must respect the following structure :
     *
     * First sprite     (index 0) :     defaultButtonTexture
     * Second sprite    (index 1) :     clickedButtonTexture (optional)
     * Third sprite     (index 2) :     hoverButtonTexture (optional)
     *
     * @param position the on-screen position
     * @param scale the scale of the Button
     * @param buttonSpritesheet a Spritesheet containg Buttons Textures
     */
    public Button(Vector2f position, Vector2f scale, Spritesheet buttonSpritesheet) {
        super(position, scale, buttonSpritesheet.getTexture(), buttonSpritesheet.getSprite(0).getTextureCoords());
        if (buttonSpritesheet.getNumberOfSprite() < 1) {
            throw new IllegalArgumentException("The Spritesheet must contain at least 1 sprite!");
        }
        this.buttonSpritesheet = buttonSpritesheet;
        buttonsList.add(this);
    }

    /**
     * Set the clicked parameter, change textures and fire the appropriate events
     *
     * @param clicked the clicked value
     */
    protected void setClicked(boolean clicked) {
        if (!this.clicked && clicked) {
            this.clickMillis = glfwGetTime();
            EventSystem.fire(new ButtonClickEvent(this));
            changeTexture(true, hover);
        } else if (this.clicked && !clicked) {
            EventSystem.fire(new ButtonReleaseEvent(this, this.clickMillis));
            changeTexture(false, hover);
        }
        this.clicked = clicked;
    }

    /**
     * Set the hover parameter, change textures and fire the appropriate events
     *
     * @param hover the hover value
     */
    protected void setHover(boolean hover) {
        if (!this.hover && hover) {
            EventSystem.fire(new ButtonHoverEvent(this));
            changeTexture(clicked, true);
        } else if (this.hover && !hover) {
            EventSystem.fire(new ButtonUnhoverEvent(this));
            changeTexture(clicked, false);
        }
        this.hover = hover;
    }

    /**
     * Check if the user click on this button
     */
    private void checkButtonClick() {
        if (MouseListener.isButtonPressed(0)) {
            if (MouseListener.getCursorPos().x >= this.getTransform().position.x + this.gameObject.getTransform().position.x && MouseListener.getCursorPos().x <= this.getTransform().position.x + this.gameObject.getTransform().position.x + this.getTransform().scale.x + this.gameObject.getTransform().scale.x) {
                if (MouseListener.getCursorPos().y >= this.getTransform().position.y + this.gameObject.getTransform().position.y && MouseListener.getCursorPos().y <= this.getTransform().position.y + this.gameObject.getTransform().position.y + this.getTransform().scale.y + this.gameObject.getTransform().scale.y) {
                    this.setClicked(true);
                    return;
                }
            }
        }
        this.setClicked(false);
    }

    /**
     * Check if the user hover this button
     */
    private void checkButtonHover() {
        if (MouseListener.getCursorPos().x >= this.getTransform().position.x + this.gameObject.getTransform().position.x && MouseListener.getCursorPos().x <= this.getTransform().position.x + this.gameObject.getTransform().position.x + this.getTransform().scale.x + this.gameObject.getTransform().scale.x) {
            if (MouseListener.getCursorPos().y >= this.getTransform().position.y + this.gameObject.getTransform().position.y && MouseListener.getCursorPos().y <= this.getTransform().position.y + this.gameObject.getTransform().position.y + this.getTransform().scale.y + this.gameObject.getTransform().scale.y) {
                this.setHover(true);
                return;
            }
        }
        this.setHover(false);
    }

    public static void checkClickAll() {
        for (Button button : buttonsList) {
            button.checkButtonClick();
        }
    }

    public static void checkHoverAll() {
        for (Button button : buttonsList) {
            button.checkButtonHover();
        }
    }

    /**
     * Change the button texture
     *
     * @param clicked the clicked value
     * @param hover the hover value
     */
    protected void changeTexture(boolean clicked, boolean hover) {
        // The Spritesheet should respect the following structure :
        // First sprite     (index 0) :     defaultButtonTexture
        // Second sprite    (index 1) :     clickedButtonTexture
        // Third sprite     (index 2) :     hoverButtonTexture
        if (clicked) {
            if (buttonSpritesheet.getNumberOfSprite() >= 2) {
                setTextureCoords(buttonSpritesheet.getSprite(1).getTextureCoords());
            }
        } else {
            if (hover) {
                if (buttonSpritesheet.getNumberOfSprite() >= 3) {
                    setTextureCoords(buttonSpritesheet.getSprite(2).getTextureCoords());
                }
            } else {
                setTextureCoords(buttonSpritesheet.getSprite(0).getTextureCoords());
            }
            }
    }

    /**
     * Remove this button
     */
    public void remove() {
        buttonsList.remove(this);
    }
}