package fr.dwightstudio.dpt.engine.graphics.gui;

import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.scripting.Component;
import org.joml.Vector2f;

import java.awt.*;
import java.text.MessageFormat;

public class Label extends Component {

    private int width;
    private int height;
    private boolean antiAliasing;
    private CharSequence string;
    private Font font;
    private FontAtlas fontAtlas;
    private Color color;

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

    public Label(CharSequence string, Font font, boolean antiAliasing) {
        this.string = string;
        this.font = font;
        this.color = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        this.antiAliasing = antiAliasing;
        this.fontAtlas = FontUtils.createFontAtlas(font, antiAliasing);
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

    public Vector2f getScale() {
        return new Vector2f(width, height);
    }

    public CharSequence getText() {
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

    public void setText(CharSequence string) {
        this.string = string;
        //ByteBuffer image = createImageFromString(string, this.font, this.color, this.antiAliasing);
        //this.texture = TextureLoader.reloadTexture(image, this.texture, width, height);
    }

    public void setFont(Font newFont) {
        this.font = newFont;
    }

    public void setColor(Color newColor) {
        this.color = newColor;
    }

    public void setAntiAliasing(boolean antiAliasing) {
        this.antiAliasing = antiAliasing;
    }

    public Surface[] createSurface(float x, float y) {
        float xPos = x;
        Surface[] surfaces = new Surface[string.length()];
        for (int i = 0; i < string.length(); i++) {
            surfaces[i] = (
                    new Surface(new Vector2f(xPos, y),
                    new Vector2f(this.fontAtlas.getGlyph(string.charAt(i)).getWidth(),  this.fontAtlas.getGlyph(string.charAt(i)).getHeight()),
                    this.fontAtlas.getTexture(), this.fontAtlas.getGlyph(string.charAt(i)).getTextureCoords(this.fontAtlas)));
            xPos += this.fontAtlas.getGlyph(string.charAt(i)).getWidth();
        }
        return surfaces;
    }
}
