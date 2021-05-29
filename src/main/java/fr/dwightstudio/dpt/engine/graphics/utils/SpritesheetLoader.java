package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.render.SpriteTexture;
import fr.dwightstudio.dpt.engine.graphics.render.Spritesheet;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.RessourceManager;
import org.joml.Vector2f;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;

public class SpritesheetLoader {

    public static Spritesheet loadSpritesheet(String filepath, int numberOfSprite, int spriteWidth, int spriteHeight, int widthSpacing, int heightSpacing) {
        List<SpriteTexture> spritesTextures = new ArrayList<>();
        Texture texture = RessourceManager.getTexture(filepath);

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
