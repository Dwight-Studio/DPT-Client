/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.audio;

import fr.dwightstudio.dsengine.logging.GameLogger;
import org.lwjgl.openal.AL;
import org.lwjgl.openal.ALC;
import org.lwjgl.openal.ALCCapabilities;
import org.lwjgl.openal.ALCapabilities;

import java.text.MessageFormat;

import static org.lwjgl.openal.ALC10.*;

public class AudioEngine {
    private long audioContext;
    private long audioDevice;

    public AudioEngine() { }

    public void init() {
        GameLogger.getLogger("Audio").debug(MessageFormat.format("{0}", alcGetString(0, ALC_DEFAULT_DEVICE_SPECIFIER)));
        audioDevice = alcOpenDevice(alcGetString(0, ALC_DEFAULT_DEVICE_SPECIFIER));

        audioContext = alcCreateContext(audioDevice, new int[1]);
        alcMakeContextCurrent(audioContext);

        ALCCapabilities alcCapabilities = ALC.createCapabilities(audioDevice);
        ALCapabilities alCapabilities = AL.createCapabilities(alcCapabilities);

        if (!alCapabilities.OpenAL10) {
            GameLogger.getLogger("Audio").fatal("Audio library not supported");
        }
    }

    public void destroy() {
        alcDestroyContext(audioContext);
        alcCloseDevice(audioDevice);
    }
}
