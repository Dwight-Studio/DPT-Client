package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

public class DPT {

    public GLFWWindow window = new GLFWWindow(960, 540);

    public void run(){
        if (GameLogger.init()) {
            window.init();
        }
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
