package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import static fr.dwightstudio.dpt.engine.Engine.WINDOWED;

public class DPT {

    public GLFWWindow window = new GLFWWindow(1280, 720, WINDOWED);

    public void run(){
        GameLogger.init();
        window.init();
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
