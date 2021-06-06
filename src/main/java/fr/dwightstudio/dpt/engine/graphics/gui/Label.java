package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
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

    /*public Label(CharSequence string, Font font, Color color, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = antiAliasing;
        *//*ByteBuffer image = createImageFromString(string, font, color, this.antiAliasing);
        this.texture = TextureLoader.createTexture(image, width, height);*//*
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(CharSequence string, Font font, Color color) {
        this.string = string;
        this.font = font;
        this.color = color;
        this.antiAliasing = false;
        *//*ByteBuffer image = createImageFromString(string, font, color, false);
        this.texture = TextureLoader.createTexture(image, width, height);*//*
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }*/
    public Label(String string, Font font, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = antiAliasing;
        this.fontAtlas = FontUtils.createFontAtlas(font, antiAliasing);
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }

    public Label(String string, FontAtlas fontAtlas, boolean antiAliasing) {
        this.string = string;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = antiAliasing;
        this.fontAtlas = fontAtlas;
        this.font = fontAtlas.getFont();
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }


    /*public Label(CharSequence string, Font font) {
        this.string = string;
        this.font = font;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = false;
        *//*ByteBuffer image = createImageFromString(string, font, this.color, false);
        this.texture = TextureLoader.createTexture(image, width, height);*//*
        GameLogger.getLogger("Text").debug(MessageFormat.format("Created a text: \"{0}\" with anti-aliasing : {1}", string, antiAliasing));
    }*/
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

    public boolean isUsingAntialiasing() {
        return this.antiAliasing;
    }

    public void setFont(Font newFont) {
        this.font = newFont;
    }

    public void setText(String string) {
        this.string = string;
    }

    public void setPosition(Vector2f position) {
        this.xPosition = position.x;
        this.yPosition = position.y;
    }

    public void setColor(Color newColor) {
        this.color = newColor;
    }

    public void setAntiAliasing(boolean antiAliasing) {
        this.antiAliasing = antiAliasing;
    }

    public void draw(float x, float y) {
        this.xPosition = x;
        this.yPosition = y;
        this.textRenderer = new TextRenderer(this.fontAtlas, this.string.toCharArray(), new Vector2f(x, y));
        this.textRenderer.init();
    }

    @Override
    public void update(float dt) {
        if (this.textRenderer != null) {
            this.textRenderer.render();
        }
    }
}
