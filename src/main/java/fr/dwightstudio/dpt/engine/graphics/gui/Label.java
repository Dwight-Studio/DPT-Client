package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.Engine;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
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
    private FontAtlas fontAtlas;
    private Color color;
    private TextRenderer textRenderer = null;
    private float xPosition;
    private float yPosition;

    private boolean dirty = true;

    public Label(String string, Font font, Color color, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = antiAliasing;
        this.fontAtlas = FontUtils.createFontAtlas(font, this.antiAliasing);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font, Color color) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = false;
        this.fontAtlas = FontUtils.createFontAtlas(font, false);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = Engine.COLORS.BLACK;
        this.antiAliasing = antiAliasing;
        this.fontAtlas = FontUtils.createFontAtlas(font, antiAliasing);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, FontAtlas fontAtlas, boolean antiAliasing) {
        this.string = string;
        this.color = Engine.COLORS.BLACK;
        this.antiAliasing = antiAliasing;
        this.fontAtlas = fontAtlas;
        this.font = fontAtlas.getFont();
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, Font font) {
        this.string = string;
        this.font = font;
        this.color = Engine.COLORS.BLACK;
        this.antiAliasing = false;
        this.fontAtlas = FontUtils.createFontAtlas(this.font, false);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public String getText() {
        return this.string;
    }

    public Font getFont() {
        return this.font;
    }

    public FontAtlas getFontAtlas() {
        return this.fontAtlas;
    }

    public Texture getTexture() {
        return this.fontAtlas.getTexture();
    }

    public Color getColor() {
        return this.color;
    }

    public Vector2f getPosition() {
        return new Vector2f(xPosition, yPosition);
    }

    public boolean isUsingAntialiasing() {
        return this.antiAliasing;
    }

    public boolean isDirty() {
        return this.dirty;
    }

    public void setFont(Font newFont) {
        this.font = newFont;
    }

    public void setText(String string) {
        this.string = string;
        this.dirty = true;
    }

    public void setPosition(Vector2f position) {
        this.xPosition = position.x;
        this.yPosition = position.y;
        this.dirty = true;
    }

    public void setColor(Color newColor) {
        this.color = newColor;
        this.dirty = true;
    }

    public void setAntiAliasing(boolean antiAliasing) {
        this.antiAliasing = antiAliasing;
    }

    public void markClean() {
        this.dirty = false;
    }

    public void draw(float x, float y) {
        this.xPosition = x;
        this.yPosition = y;
        this.textRenderer = new TextRenderer(this, new Vector2f(x, y));
        this.textRenderer.init();
    }

    @Override
    public void update(float dt) {
        if (this.textRenderer != null) {
            this.textRenderer.render();
        }
    }
}
