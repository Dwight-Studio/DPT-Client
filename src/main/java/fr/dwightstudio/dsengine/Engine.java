/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine;

import fr.dwightstudio.dsengine.graphics.objects.Color;

public class Engine {
    public static final long FULLSCREEN = 0;
    public static final long WINDOWED = 1;

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
