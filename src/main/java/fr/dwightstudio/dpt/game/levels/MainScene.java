/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.game.levels;

import fr.dwightstudio.dpt.DSEngine.Engine;
import fr.dwightstudio.dpt.DSEngine.events.EventListener;
import fr.dwightstudio.dpt.DSEngine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.DSEngine.graphics.gui.Button;
import fr.dwightstudio.dpt.DSEngine.graphics.gui.Checkbox;
import fr.dwightstudio.dpt.DSEngine.graphics.gui.Label;
import fr.dwightstudio.dpt.DSEngine.graphics.objects.Color;
import fr.dwightstudio.dpt.DSEngine.graphics.objects.*;
import fr.dwightstudio.dpt.DSEngine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.DSEngine.graphics.utils.FontUtils;
import fr.dwightstudio.dpt.DSEngine.inputs.MouseListener;
import fr.dwightstudio.dpt.DSEngine.resources.ResourceManager;
import fr.dwightstudio.dpt.DSEngine.scripting.GameObject;
import fr.dwightstudio.dpt.DSEngine.scripting.Scene;
import org.joml.Vector2f;

import java.awt.*;
import java.util.Objects;

public class MainScene extends Scene implements EventListener {

    GameObject tiles = new GameObject("tiles", 2);
    GameObject background = new GameObject("background", -1);

    private final Surface surface = new Surface(new Vector2f(0, 0), new Vector2f(64, 64), Engine.COLORS.WHITE);
    private final Surface surface2 = new Surface(new Vector2f(100, 100), new Vector2f(64, 10), new Color(0, 1, 0, 0.5f));
    private final Surface surface3 = new Surface(new Vector2f(132, 100), new Vector2f(64, 64), new Color(1, 0, 0, 0.5f));

    private Label cursorPosX;
    private Label cursorPosY;
    private Label fpsCounter;
    FontAtlas fontAtlas;

    private int count = 0;

    public MainScene() { }

    @Override
    public void init() {
        camera = new Camera(new Vector2f(0, 0));
        Viewport viewport = new Viewport(0, 0, GLFWWindow.getWidth() / 2, GLFWWindow.getHeight() / 2);
        viewport.attachScene(new TestScene());
        GameObject otherOne = new GameObject("otherOne", 1);
        ResourceManager.load("./src/main/resources/textures/test.png", Texture.class);
        ResourceManager.load("./src/main/resources/textures/sheet.png", Spritesheet.class);
        ResourceManager.load("./src/main/resources/textures/buttonSheet.png", Spritesheet.class);
        ResourceManager.load("./src/main/resources/textures/checkboxSheet.png", Spritesheet.class);

        Font font = new Font("Ubuntu", Font.PLAIN, 28);

        this.fontAtlas = FontUtils.createFontAtlas(font, true);

        Button button = new Button(new Vector2f(450, 300), new Vector2f(64, 64), Objects.requireNonNull(ResourceManager.<Spritesheet>get("./src/main/resources/textures/buttonSheet.png")));
        Checkbox checkbox = new Checkbox(new Vector2f(600, 300), new Vector2f(64, 64), ResourceManager.<Spritesheet>get("./src/main/resources/textures/checkboxSheet.png"));
        Checkbox checkbox2 = new Checkbox(new Vector2f(800, 300), new Vector2f(64, 64), ResourceManager.<Spritesheet>get("./src/main/resources/textures/checkboxSheet.png"));


        this.fpsCounter = new Label("FPS", fontAtlas, Engine.COLORS.PURPLE);
        this.cursorPosX = new Label("X", fontAtlas);
        this.cursorPosY = new Label("Y", fontAtlas);
        this.fpsCounter.draw(new Vector2f(0, GLFWWindow.getHeight() - this.fpsCounter.getFontAtlas().getTexture().getHeight()), new Vector2f(0, 0));
        this.cursorPosX.draw(new Vector2f(0, GLFWWindow.getHeight() - this.fpsCounter.getFontAtlas().getTexture().getHeight() * 2), new Vector2f(0, 0));
        this.cursorPosY.draw(new Vector2f(0, GLFWWindow.getHeight() - this.fpsCounter.getFontAtlas().getTexture().getHeight() * 3), new Vector2f(0, 0));

        Spritesheet spritesheet = ResourceManager.get("./src/main/resources/textures/sheet.png");
        ResourceManager.load("./src/main/resources/textures/background.png", Texture.class);
        background.addComponent(new Surface(new Vector2f(0, 0), new Vector2f(GLFWWindow.getWidth(), GLFWWindow.getHeight()), ResourceManager.<Texture>get("./src/main/resources/textures/background.png")));
        tiles.addComponent(cursorPosX);
        tiles.addComponent(fpsCounter);
        tiles.addComponent(cursorPosY);
        tiles.addComponent(surface);
        tiles.addComponent(surface2);
        surface.setTexture(Objects.requireNonNull(spritesheet).getSprite(0).getTexture());
        surface.setTextureCoords(spritesheet.getSprite(0).getTextureCoords());
        tiles.addComponent(new Surface(new Vector2f(200, 200), new Vector2f(64, 64), ResourceManager.<Texture>get("./src/main/resources/textures/test.png")));
        tiles.addComponent(button);
        tiles.addComponent(checkbox);
        tiles.addComponent(checkbox2);
        otherOne.addComponent(surface3);
        tiles.addComponent(viewport);
        setBackgroundColor(Engine.COLORS.BLACK);
        this.addGameObject(tiles);
        this.addGameObject(otherOne);
        this.addGameObject(background);
    }

    @Override
    public void update(double dt) {
        tiles.getTransform().position.x += dt * 10.0f;
        background.getTransform().position.x += dt * 10.0f;
        surface2.getTransform().setRotation(surface2.getTransform().getRotation(Transform.DEGREE) + 1, Transform.DEGREE);

        if (count == 60) {
            fpsCounter.setText(Math.round(1.0f / dt) + " FPS");
            count = 0;
        } else {
            count++;
        }

        cursorPosX.setText(String.valueOf(MouseListener.getOrthoCursorPos().x));
        cursorPosY.setText(String.valueOf(MouseListener.getOrthoCursorPos().y));

        super.update(dt);
    }
}
