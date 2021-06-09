package fr.dwightstudio.dpt.engine;

import fr.dwightstudio.dpt.engine.graphics.objects.Color;

public class Engine {
    public static final long ENGINE_FULLSCREEN = 0;
    public static final long ENGINE_WINDOWED = 1;


    public static class COLORS {
        public static final Color RED = new Color(1.0f, 0.0f, 0.0f, 1.0f);
        public static final Color GREEN = new Color(0.0f, 1.0f, 0.0f, 1.0f);
        public static final Color BLUE = new Color(0.0f, 0.0f, 1.0f, 1.0f);
        public static final Color YELLOW = new Color(1.0f, 1.0f, 0.0f, 1.0f);
        public static final Color ORANGE = new Color(1.0f, 0.5f, 0.0f, 1.0f);
        public static final Color MAGENTA = new Color(1.0f, 0.0f, 1.0f, 1.0f);
        public static final Color PURPLE = new Color(0.5f, 0.0f, 1.0f, 1.0f);
        public static final Color CYAN = new Color(0.0f, 1.0f, 1.0f, 1.0f);
        public static final Color BLACK = new Color(0.0f, 0.0f, 0.0f, 1.0f);
        public static final Color WHITE = new Color(1.0f, 1.0f, 1.0f, 1.0f);
    }
}
