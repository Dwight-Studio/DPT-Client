package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import static fr.dwightstudio.dpt.engine.Engine.ENGINE_WINDOWED;

public class DPT {

    public GLFWWindow window = new GLFWWindow(1280, 720, ENGINE_WINDOWED);

    public void run(){
        Thread.currentThread().setName("Main Render Thread");
        GameLogger.init();
        window.init();
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
