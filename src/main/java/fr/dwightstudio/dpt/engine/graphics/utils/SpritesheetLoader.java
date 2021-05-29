package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.render.SpriteTexture;
import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import org.joml.Vector2f;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;

public class SpritesheetLoader {

    private static int numberOfSprite;
    private static int spriteWidth;
    private static int spriteHeight;
    private static int widthSpacing;
    private static int heightSpacing;

    public static Spritesheet loadSpritesheet(String filepath) {
        List<SpriteTexture> spritesTextures = new ArrayList<>();
        Texture texture = ResourceManager.get(filepath);

        try {
            JSONObject jsonObject = (JSONObject) new JSONParser().parse(new FileReader(filepath + ".meta"));
            numberOfSprite = (int) jsonObject.get("numberOfSprite");
            spriteWidth = (int) jsonObject.get("spriteWidth");
            spriteHeight = (int) jsonObject.get("spriteHeight");
            widthSpacing = (int) jsonObject.get("widthSpacing");
            heightSpacing = (int) jsonObject.get("heightSpacing");

        } catch (IOException | ParseException e) {
            e.printStackTrace();
            return null;
        }

        int currentX = 0;
        int currentY = texture.getHeight() - spriteHeight;
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
                    new Vector2f(right, top),
                    new Vector2f(right, bottom),
                    new Vector2f(left, bottom),
                    new Vector2f(left, top)
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
