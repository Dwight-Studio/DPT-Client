/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.DSEngine;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.objects.Transform;
import fr.dwightstudio.dpt.engine.graphics.renderers.TextRenderer;
import fr.dwightstudio.dpt.engine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

import java.awt.*;
import java.text.MessageFormat;

public class Label extends Component {

    private boolean antiAliasing;
    private String string;
    private Font font;
    private final FontAtlas fontAtlas;
    private Color color;
    private TextRenderer textRenderer = null;
    private Transform transform;
    private Transform lastTransform;
    private int zindex;

    private final int maxNumberOfChars;

    private boolean dirty = true;

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param color the Label's color
     * @param antiAliasing if the font antialiasing should be enabled
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, Font font, Color color, boolean antiAliasing, int maxNumberOfChars) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = antiAliasing;
        this.maxNumberOfChars = maxNumberOfChars;
        this.fontAtlas = FontUtils.createFontAtlas(font, this.antiAliasing);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param color the Label's color
     * @param antiAliasing if the font antialiasing should be enabled
     */
    public Label(String string, Font font, Color color, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = antiAliasing;
        this.maxNumberOfChars = 1000;
        this.fontAtlas = FontUtils.createFontAtlas(font, this.antiAliasing);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param color the Label's color
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, Font font, Color color, int maxNumberOfChars) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = false;
        this.fontAtlas = FontUtils.createFontAtlas(font, false);
        this.maxNumberOfChars = maxNumberOfChars;
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param antiAliasing if the font antialiasing should be enabled
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, Font font, boolean antiAliasing, int maxNumberOfChars) {
        this.string = string;
        this.font = font;
        this.color = DSEngine.COLORS.BLACK;
        this.antiAliasing = antiAliasing;
        this.maxNumberOfChars = maxNumberOfChars;
        this.fontAtlas = FontUtils.createFontAtlas(font, antiAliasing);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param fontAtlas the Label's FontAtlas
     * @param color the Label's color
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, FontAtlas fontAtlas, Color color, int maxNumberOfChars) {
        this.string = string;
        this.color = color;
        this.fontAtlas = fontAtlas;
        this.antiAliasing = fontAtlas.isAntiAliasing();
        this.font = fontAtlas.getFont();
        this.maxNumberOfChars = maxNumberOfChars;
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param color the Label's color
     */
    public Label(String string, Font font, Color color) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = false;
        this.maxNumberOfChars = 1000;
        this.fontAtlas = FontUtils.createFontAtlas(font, false);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     * @param antiAliasing if the font antialiasing should be enabled
     */
    public Label(String string, Font font, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = DSEngine.COLORS.BLACK;
        this.antiAliasing = antiAliasing;
        this.maxNumberOfChars = 1000;
        this.fontAtlas = FontUtils.createFontAtlas(font, antiAliasing);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param fontAtlas the Label's FontAtlas
     * @param color the Label's color
     */
    public Label(String string, FontAtlas fontAtlas, Color color) {
        this.string = string;
        this.color = color;
        this.fontAtlas = fontAtlas;
        this.antiAliasing = fontAtlas.isAntiAliasing();
        this.font = fontAtlas.getFont();
        this.maxNumberOfChars = 1000;
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param fontAtlas the Label's FontAltas
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, FontAtlas fontAtlas, int maxNumberOfChars) {
        this.string = string;
        this.color = DSEngine.COLORS.BLACK;
        this.fontAtlas = fontAtlas;
        this.antiAliasing = fontAtlas.isAntiAliasing();
        this.font = fontAtlas.getFont();
        this.maxNumberOfChars = maxNumberOfChars;
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's FontAltlas
     * @param maxNumberOfChars the max number of chars of this Label
     */
    public Label(String string, Font font, int maxNumberOfChars) {
        this.string = string;
        this.font = font;
        this.color = DSEngine.COLORS.BLACK;
        this.antiAliasing = false;
        this.maxNumberOfChars = maxNumberOfChars;
        this.fontAtlas = FontUtils.createFontAtlas(this.font, false);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param fontAtlas the Label's FontAtlas
     */
    public Label(String string, FontAtlas fontAtlas) {
        this.string = string;
        this.color = DSEngine.COLORS.BLACK;
        this.fontAtlas = fontAtlas;
        this.antiAliasing = fontAtlas.isAntiAliasing();
        this.font = fontAtlas.getFont();
        this.maxNumberOfChars = 1000;
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * Create a new Label
     *
     * @param string the Label's text
     * @param font the Label's font
     */
    public Label(String string, Font font) {
        this.string = string;
        this.font = font;
        this.color = DSEngine.COLORS.BLACK;
        this.antiAliasing = false;
        this.maxNumberOfChars = 1000;
        this.fontAtlas = FontUtils.createFontAtlas(this.font, false);
        GameLogger.getLogger("Label").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    /**
     * @return the current text
     */
    public String getText() {
        return this.string;
    }

    /**
     * @return the current font
     */
    public Font getFont() {
        return this.font;
    }

    /**
     * @return the current FontAtlas
     */
    public FontAtlas getFontAtlas() {
        return this.fontAtlas;
    }

    /**
     * @return the current color
     */
    public Color getColor() {
        return this.color;
    }

    /**
     * @return the Transform object
     */
    public Transform getTransform() {
        return this.transform;
    }

    /**
     * @return the max number of chars allowed
     */
    public int getMaxNumberOfChars() {
        return maxNumberOfChars;
    }

    /**
     * @return if the font is using antialiasing
     */
    public boolean isUsingAntialiasing() {
        return this.antiAliasing;
    }

    /**
     * When this tag is set, the renderer will update this Label
     *
     * @return set this Label to be dirty
     */
    public boolean isDirty() {
        return this.dirty;
    }

    /**
     * @return the TextRenderer assiocated with the Label, null if not drawn on screen.
     */
    public TextRenderer getTextRenderer() {
        if (this.textRenderer != null) {
            return this.textRenderer;
        } else {
            return null;
        }
    }

    /**
     * Set the new font of this label
     *
     * @param newFont a font
     */
    public void setFont(Font newFont) {
        if (!newFont.equals(this.font)) {
            this.font = newFont;
        }
    }

    /**
     * Set a new text for this label
     *
     * @param string a text
     */
    public void setText(String string) {
        if (!string.equals(this.string)) {
            this.string = string;
            this.dirty = true;
        }
    }

    /**
     * Set the new color of this Label
     *
     * @param newColor the new color
     */
    public void setColor(Color newColor) {
        if (!newColor.equals(this.color)) {
            this.color = newColor;
            this.dirty = true;
        }
    }

    /**
     * Set the antialiasing value
     *
     * @param antiAliasing the antialiasing value
     */
    public void setAntiAliasing(boolean antiAliasing) {
        this.antiAliasing = antiAliasing;
    }

    /**
     * Set the dirty flag to false
     */
    public void markClean() {
        this.dirty = false;
    }

    /**
     * Draw this Label on the screen
     *
     * NOTE: You must call this only one time.
     *
     * @param position the position of the Label
     * @param scale the scale of the Label
     */
    public void draw(Vector2f position, Vector2f scale) {
        this.transform = new Transform();
        this.lastTransform = new Transform();
        this.transform.position = position;
        this.transform.scale = scale;
        this.textRenderer = new TextRenderer(this, 0);
        this.textRenderer.init();
    }

    /**
     * Draw this Label on the screen
     *
     * NOTE: You must call this only one time.
     *
     * @param position the position of the Label
     * @param scale the scale of the Label
     * @param zindex the z level of the TextRenderer
     */
    public void draw(Vector2f position, Vector2f scale, int zindex) {
        this.transform = new Transform();
        this.lastTransform = new Transform();
        this.transform.position = position;
        this.transform.scale = scale;
        this.textRenderer = new TextRenderer(this, zindex);
        this.textRenderer.init();
    }

    @Override
    public void update(double dt) {
        if (this.textRenderer != null) {
            this.textRenderer.render();
        }
        if (!this.lastTransform.equals(this.transform)) {
            this.lastTransform = this.transform.copy();
            dirty = true;
        }
    }
}
