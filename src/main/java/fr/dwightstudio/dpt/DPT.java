package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import static fr.dwightstudio.dpt.engine.Engine.ENGINE_FULLSCREEN;

public class DPT {

    public GLFWWindow window = new GLFWWindow(1920, 1080, ENGINE_FULLSCREEN);

    public void run(){
        if (GameLogger.init()) {
            window.init();
        }
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
