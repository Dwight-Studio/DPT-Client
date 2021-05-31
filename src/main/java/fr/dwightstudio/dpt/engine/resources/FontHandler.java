package fr.dwightstudio.dpt.engine.resources;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class FontHandler implements TypeHandler<Font> {
    private static final Map<String, Font> FONTS = new HashMap<>();

    @Override
    public Font get(String filepath) {
        if (!FONTS.containsKey(filepath)) {
            Font font = null;
            try {
                font = Font.createFont(Font.TRUETYPE_FONT, new File(filepath));
            } catch (FontFormatException | IOException e) {
                e.printStackTrace();
            }

            if (font != null) {
                FONTS.put(filepath, font);
            } else {
                return null;
            }
        }
        return FONTS.get(filepath);
    }
}
