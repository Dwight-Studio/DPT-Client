package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;
import fr.dwightstudio.dpt.engine.graphics.gui.Label;
import fr.dwightstudio.dpt.engine.graphics.gui.events.GUIButtonEvent;
import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.render.*;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import org.joml.Vector2f;

import java.awt.*;
import java.io.File;
import java.io.IOException;

public class MainScene extends Scene implements GUIButtonEvent {

    private final Surface surface = new Surface(new Vector2f(0, 0), 64, 64, new Color(1, 1, 1, 1));
    private final Surface surface2 = new Surface(new Vector2f(100, 100), 64, 64, new Color(0, 1, 0, 0.5f));
    private Spritesheet spritesheet;
    private Label label;
    private Surface textSurface;
    private int count = 0;
    private Button button = new Button(new Vector2f(400, 400), new Vector2f(50, 32), new Color(0.0f, 0.0f, 1.0f));

    public MainScene() {

    }

    @Override
    public void init() {
        camera = new Camera(new Vector2f());
        GameObject tiles = new GameObject("tiles", 0);
        ResourceManager.load("./src/main/resources/textures/test.png", Texture.class);
        ResourceManager.load("./src/main/resources/textures/sheet.png", Spritesheet.class);

        Font font = null;
        try {
            GraphicsEnvironment graphicsEnvironment = GraphicsEnvironment.getLocalGraphicsEnvironment();
            graphicsEnvironment.registerFont(Font.createFont(Font.TRUETYPE_FONT, new File("./src/main/resources/fonts/Ubuntu-Medium.ttf")));
            font = new Font("Ubuntu", Font.PLAIN, 28);
        } catch (FontFormatException | IOException e) {
            e.printStackTrace();
        }

        button.addEventListener(this);
        this.label = new Label("FPS", font, true);
        textSurface = label.createSurface(0, GLFWWindow.getHeight() - this.label.getScale().y);
        this.spritesheet = ResourceManager.get("./src/main/resources/textures/sheet.png");
        tiles.addComponent(surface);
        tiles.addComponent(surface2);
        surface.setTexture(spritesheet.getSprite(0).getTexture());
        surface.setTextureCoords(spritesheet.getSprite(0).getTextureCoords());
        tiles.addComponent(textSurface);
        tiles.addComponent(new Line(new Vector2f(0, 300), new Vector2f(300, 300), new Color(0.0f, 1.0f, 0.0f), 4.0f));
        tiles.addComponent(new Surface(new Vector2f(200, 200), 64, 64, ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        tiles.addComponent(button);
        setBackgroundColor(new Color(1.0f, 1.0f, 1.0f, 0.0f));
        this.addGameObject(tiles);
    }

    @Override
    public void update(float dt) {
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }

        if (surface2.getTransform().getRotation(Transform.DEGREE) < 90) {
            surface2.getTransform().setRotation(surface2.getTransform().getRotation(Transform.DEGREE) + 1, Transform.DEGREE);
        }

        if (count == 60) {
            this.label.setText(Math.round(1.0f / dt) + " FPS");
            textSurface.getTransform().scale = this.label.getScale();
            textSurface.setTexture(this.label.getTexture());
            count = 0;
        } else {
            count++;
        }

        renderer.render();
    }

    @Override
    public void onClick(int buttonID) {

    }

    @Override
    public void onHover(int buttonID) {

    }
}
