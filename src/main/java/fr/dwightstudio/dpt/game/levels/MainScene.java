/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.engine.Engine;
import fr.dwightstudio.dpt.engine.events.EventHandler;
import fr.dwightstudio.dpt.engine.events.EventListener;
import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonClickEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonHoverEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonReleaseEvent;
import fr.dwightstudio.dpt.engine.events.types.gui.button.ButtonUnhoverEvent;
import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.graphics.gui.Button;
import fr.dwightstudio.dpt.engine.graphics.gui.Checkbox;
import fr.dwightstudio.dpt.engine.graphics.gui.Label;
import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.objects.*;
import fr.dwightstudio.dpt.engine.graphics.objects.Color;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.engine.graphics.utils.SpritesheetLoader;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import fr.dwightstudio.dpt.engine.scripting.GameObject;
import fr.dwightstudio.dpt.engine.scripting.Scene;
import org.joml.Vector2f;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Objects;

public class MainScene extends Scene implements EventListener {

    GameObject tiles = new GameObject("tiles", 2);

    private final Surface surface = new Surface(new Vector2f(0, 0), new Vector2f(64, 64), Engine.COLORS.WHITE);
    private final Surface surface2 = new Surface(new Vector2f(100, 100), new Vector2f(64, 64), new Color(0, 1, 0, 0.5f));
    private final Surface surface3 = new Surface(new Vector2f(132, 100), new Vector2f(64, 64), new Color(1, 0, 0, 0.5f));
    private Spritesheet spritesheet;

    private Label cursorPosX;
    private Label cursorPosY;
    private Label fpsCounter;
    FontAtlas fontAtlas;

    private int count = 0;

    public MainScene() {

    }

    @Override
    public void init() {
        camera = new Camera(new Vector2f());
        GameObject otherOne = new GameObject("otherOne", 1);
        ResourceManager.load("./src/main/resources/textures/test.png", Texture.class);
        ResourceManager.load("./src/main/resources/textures/sheet.png", Spritesheet.class);
        ResourceManager.load("./src/main/resources/textures/buttonSheet.png", Spritesheet.class);
        ResourceManager.load("./src/main/resources/textures/checkboxSheet.png", Spritesheet.class);

        Font font = null;
        try {
            GraphicsEnvironment graphicsEnvironment = GraphicsEnvironment.getLocalGraphicsEnvironment();
            graphicsEnvironment.registerFont(Font.createFont(Font.TRUETYPE_FONT, new File("./src/main/resources/fonts/Ubuntu-Medium.ttf")));
            font = new Font("Ubuntu", Font.PLAIN, 28);
        } catch (FontFormatException | IOException e) {
            e.printStackTrace();
        }

        this.fontAtlas = FontUtils.createFontAtlas(font, true);

        Button button = new Button(new Vector2f(450, 300), new Vector2f(64, 64), Objects.requireNonNull(ResourceManager.<Spritesheet>get("./src/main/resources/textures/buttonSheet.png")));
        Checkbox checkbox = new Checkbox(new Vector2f(600, 300), new Vector2f(64, 64), ResourceManager.<Spritesheet>get("./src/main/resources/textures/checkboxSheet.png"));
        Checkbox checkbox2 = new Checkbox(new Vector2f(800, 300), new Vector2f(64, 64), ResourceManager.<Spritesheet>get("./src/main/resources/textures/checkboxSheet.png"));


        this.fpsCounter = new Label("FPS", fontAtlas, Engine.COLORS.PURPLE);
        this.cursorPosX = new Label("X", fontAtlas);
        this.cursorPosY = new Label("Y", fontAtlas);
        this.fpsCounter.draw(0, GLFWWindow.getHeight() - this.fpsCounter.getFontAtlas().getTexture().getHeight());
        this.cursorPosX.draw(0, GLFWWindow.getHeight() - this.cursorPosX.getFontAtlas().getTexture().getHeight() * 2);
        this.cursorPosY.draw(0, GLFWWindow.getHeight() - this.cursorPosY.getFontAtlas().getTexture().getHeight() * 3);

        this.spritesheet = ResourceManager.get("./src/main/resources/textures/sheet.png");
        tiles.addComponent(cursorPosX);
        tiles.addComponent(fpsCounter);
        tiles.addComponent(cursorPosY);
        tiles.addComponent(surface);
        tiles.addComponent(surface2);
        surface.setTexture(spritesheet.getSprite(0).getTexture());
        surface.setTextureCoords(spritesheet.getSprite(0).getTextureCoords());
        tiles.addComponent(new Line(new Vector2f(0, 300), new Vector2f(300, 300), Engine.COLORS.GREEN, 4.0f));
        tiles.addComponent(new Surface(new Vector2f(200, 200), new Vector2f(64, 64), ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        tiles.addComponent(button);
        tiles.addComponent(checkbox);
        tiles.addComponent(checkbox2);
        otherOne.addComponent(surface3);
        setBackgroundColor(Engine.COLORS.WHITE);
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
            fpsCounter.setText(Math.round(1.0f / dt) + " FPS");
            tiles.getTransform().position.x += 1;
            count = 0;
        } else {
            count++;
        }

        cursorPosX.setText(String.valueOf(MouseListener.getCursorPos().x));
        cursorPosY.setText(String.valueOf(MouseListener.getCursorPos().y));

        rendererHelper.render();
    }
}
