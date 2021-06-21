/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.utils;

import fr.dwightstudio.dsengine.graphics.objects.SpriteTexture;
import fr.dwightstudio.dsengine.graphics.objects.Spritesheet;
import fr.dwightstudio.dsengine.graphics.objects.Texture;
import fr.dwightstudio.dsengine.logging.GameLogger;
import fr.dwightstudio.dsengine.resources.ResourceManager;
import org.joml.Vector2f;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileReader;
import java.io.IOException;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class SpritesheetLoader {

    /**
     * Load a Spritesheet image file and create a Spritesheet object with it
     *
     * @param filepath the spritesheet filepath
     * @return a Spritesheet
     */
    public static Spritesheet loadSpritesheet(String filepath) {
        List<SpriteTexture> spritesTextures = new ArrayList<>();
        ResourceManager.load(filepath, Texture.class);
        Texture texture = ResourceManager.get(filepath);

        long numberOfSprite;
        long spriteWidth;
        long spriteHeight;
        long widthSpacing;
        long heightSpacing;
        try {
            JSONObject jsonObject = (JSONObject) new JSONParser().parse(new FileReader(filepath + ".meta"));
            numberOfSprite = (long) jsonObject.get("numberOfSprite");
            spriteWidth = (long) jsonObject.get("spriteWidth");
            spriteHeight = (long) jsonObject.get("spriteHeight");
            widthSpacing = (long) jsonObject.get("widthSpacing");
            heightSpacing = (long) jsonObject.get("heightSpacing");

        } catch (IOException | ParseException e) {
            e.printStackTrace();
            return null;
        }

        int currentX = 0;
        int currentY = Objects.requireNonNull(texture).getHeight() - (int) spriteHeight;
        for (int i = 0; i < numberOfSprite; i++) {
            // These variables are all normalized values
            // So we are selecting a sprite like this :
            //    left/top ->******<- right/top
            //               ******
            //               ******
            // left/bottom ->******<- right/bottom
            float top = (currentY + spriteHeight) / (float) texture.getHeight();
            float right = (currentX + spriteWidth) / (float) texture.getWidth();
            float left = currentX / (float) texture.getWidth();
            float bottom = currentY / (float) texture.getHeight();

            Vector2f[] textureCoords = {
                    new Vector2f(right, bottom),
                    new Vector2f(right, top),
                    new Vector2f(left, top),
                    new Vector2f(left, bottom),
            };
            SpriteTexture spriteTexture = new SpriteTexture(texture, textureCoords);
            spritesTextures.add(spriteTexture);

            currentX += spriteWidth + widthSpacing;
            if (currentX >= texture.getWidth()) {
                currentX = 0;
                currentY -= spriteHeight + heightSpacing;
            }
        }
        GameLogger.getLogger("SpritesheetLoader").debug(MessageFormat.format("Created Spritessheet : {0}", filepath));
        return new Spritesheet(texture, spritesTextures);
    }
}
