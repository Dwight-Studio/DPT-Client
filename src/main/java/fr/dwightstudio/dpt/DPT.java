/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt;

import fr.dwightstudio.dsengine.audio.AudioEngine;
import fr.dwightstudio.dsengine.graphics.GLFWWindow;
import fr.dwightstudio.dsengine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.game.levels.MainScene;

import static fr.dwightstudio.dsengine.Engine.WINDOWED;

public class DPT {

    public GLFWWindow window = new GLFWWindow(1280, 720, WINDOWED);
    public AudioEngine audioEngine = new AudioEngine();

    public void run(){
        audioEngine.init();
        window.init();
        SceneManager.changeScene(new MainScene());
        window.startLoop();
        audioEngine.destroy();
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
