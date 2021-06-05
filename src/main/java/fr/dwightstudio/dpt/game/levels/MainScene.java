package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.events.EventHandler;
import fr.dwightstudio.dpt.engine.events.EventListener;
import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.events.types.ButtonClickEvent;
import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;
import fr.dwightstudio.dpt.engine.graphics.gui.Label;
import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.objects.*;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import org.joml.Vector2f;

import java.awt.*;
import java.io.File;
import java.io.IOException;

public class MainScene extends Scene implements EventListener {

    private final Surface surface = new Surface(new Vector2f(0, 0), new Vector2f(64, 64), new Color(1, 1, 1, 1));
    private final Surface surface2 = new Surface(new Vector2f(100, 100), new Vector2f(64, 64), new Color(0, 1, 0, 0.5f));
    private final Surface surface3 = new Surface(new Vector2f(132, 100), new Vector2f(64, 64), new Color(1, 0, 0, 0.5f));
    private Spritesheet spritesheet;

    private Label cursorPosX;
    private Label label;
    private Label cursorPosY;

    private int count = 0;
    private Button button = new Button(new Vector2f(400, 400), new Vector2f(50, 32), new Color(0.0f, 0.0f, 1.0f));

    public MainScene() {

    }

    @Override
    public void init() {
        camera = new Camera(new Vector2f());
        GameObject tiles = new GameObject("tiles", 2);
        GameObject otherOne = new GameObject("otherOne", 1);
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

        FontAtlas fontAtlas = FontUtils.createFontAtlas(font, true);

        EventSystem.registerListener(this);

        this.label = new Label("FPS", fontAtlas, true);
        this.label.draw(0, GLFWWindow.getHeight() - this.label.getFontAtlas().getTexture().getHeight());
        this.cursorPosX = new Label("X", fontAtlas, true);
        this.cursorPosX.draw(0, GLFWWindow.getHeight() - this.cursorPosX.getFontAtlas().getTexture().getHeight() * 2);
        //this.cursorPosY = new Label("Y", fontAtlas, true);
        //this.cursorPosY.draw(0, GLFWWindow.getHeight() - this.label.getFontAtlas().getTexture().getHeight() * 3);

        this.spritesheet = ResourceManager.get("./src/main/resources/textures/sheet.png");
        tiles.addComponent(label);
        tiles.addComponent(cursorPosX);
        //tiles.addComponent(cursorPosY);
        tiles.addComponent(surface);
        tiles.addComponent(surface2);
        surface.setTexture(spritesheet.getSprite(0).getTexture());
        surface.setTextureCoords(spritesheet.getSprite(0).getTextureCoords());
        tiles.addComponent(new Line(new Vector2f(0, 300), new Vector2f(300, 300), new Color(0.0f, 1.0f, 0.0f), 4.0f));
        tiles.addComponent(new Surface(new Vector2f(200, 200), new Vector2f(64, 64), ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        tiles.addComponent(button);
        otherOne.addComponent(surface3);
        setBackgroundColor(new Color(1.0f, 1.0f, 1.0f, 0.0f));
        this.addGameObject(tiles);
        this.addGameObject(otherOne);
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
            count = 0;
        } else {
            count++;
        }
        this.cursorPosX.setText(String.valueOf(MouseListener.getCursorPos().x));
        //this.cursorPosY.setText(String.valueOf(MouseListener.getCursorPos().y));

        renderer.render();
    }

    @EventHandler
    public void onClick(ButtonClickEvent event) {
        GameLogger.getLogger("MainScene").debug(event.getButton().toString());
    }
}
