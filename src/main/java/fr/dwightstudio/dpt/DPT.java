/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.DSEngine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.DSEngine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.game.levels.MainScene;

import static fr.dwightstudio.dpt.DSEngine.Engine.WINDOWED;

public class DPT {

    public GLFWWindow window = new GLFWWindow(1280, 720, WINDOWED);

    public void run(){
        window.init();
        SceneManager.changeScene(new MainScene());
        window.startLoop();
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
