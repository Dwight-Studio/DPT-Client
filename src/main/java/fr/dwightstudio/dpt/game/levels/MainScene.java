package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.graphics.gui.Text;
import fr.dwightstudio.dpt.engine.graphics.render.*;
import fr.dwightstudio.dpt.engine.graphics.render.Color;
import fr.dwightstudio.dpt.engine.inputs.GameInputs;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.primitives.Surface;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import org.joml.Vector2f;

import java.awt.*;
import java.io.File;
import java.io.IOException;

public class MainScene extends Scene {

    private GameObject tiles;
    private final Surface surface = new Surface(0, 0, 64, 64, new Color(1, 0, 0, 1));
    private final Surface surface2 = new Surface(100, 100, 64, 64, new Color(0, 1, 0, 1));
    private Spritesheet spritesheet;
    private Font font;
    private Surface textSurface;
    private int count = 0;

    public MainScene() {

    }

    @Override
    public void init() {
        camera = new Camera(new Vector2f());
        tiles = new GameObject("tiles", 0);
        ResourceManager.load("./src/main/resources/textures/test.png", Texture.class);
        ResourceManager.load("./src/main/resources/textures/sheet.png", Spritesheet.class);

        try {
            GraphicsEnvironment graphicsEnvironment = GraphicsEnvironment.getLocalGraphicsEnvironment();
            graphicsEnvironment.registerFont(Font.createFont(Font.TRUETYPE_FONT, new File("./src/main/resources/fonts/Ubuntu-Medium.ttf")));
            this.font = new Font("Ubuntu", Font.PLAIN, 50);
        } catch (FontFormatException | IOException e) {
            e.printStackTrace();
        }
        this.textSurface = Text.createSurface(0, 300, "Bonjour", font, java.awt.Color.BLACK);
        this.spritesheet = ResourceManager.get("./src/main/resources/textures/sheet.png");
        tiles.addComponent(surface);
        tiles.addComponent(surface2);
        tiles.addComponent(textSurface);
        tiles.addComponent(new Surface(200, 200, 64, 64, ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        setBackgroundColor(new Color(1.0f, 1.0f, 1.0f, 0.0f));
        this.addGameObject(tiles);
    }

    @Override
    public void update(float dt) {
        for (GameObject gameObject : this.gameObjects) {
            gameObject.update(dt);
        }

        surface.setTexture(spritesheet.getSprite(0).getTexture());
        surface.setTextureCoords(spritesheet.getSprite(0).getTextureCoords());

        surface.getTransform().rotation += 0.1f;

        renderer.render();
    }
}
