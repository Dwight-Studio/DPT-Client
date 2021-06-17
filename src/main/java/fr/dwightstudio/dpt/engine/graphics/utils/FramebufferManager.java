/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.objects.Framebuffer;

import java.util.ArrayList;
import java.util.List;

public class FramebufferManager {
    private static final List<Framebuffer> framebuffers = new ArrayList<>();

    public static void add(Framebuffer framebuffer) {
        if (!framebuffers.contains(framebuffer)) {
            framebuffers.add(framebuffer);
        }
    }

    public static void remove(Framebuffer framebuffer) {
        framebuffers.remove(framebuffer);
    }

    public static List<Framebuffer> getFramebuffers() {
        return framebuffers;
    }

    public static void render(Framebuffer framebuffer) {
        framebuffer.render();
    }

    public static void renderAll() {
        for (Framebuffer framebuffer : framebuffers) {
            framebuffer.render();
        }
    }
}
