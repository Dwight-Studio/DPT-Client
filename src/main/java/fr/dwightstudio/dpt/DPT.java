package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;

public class DPT {

    public GLFWWindow window = new GLFWWindow(640, 360);

    public void run(){
        window.init();
    }

    public static void main(String[] args){
        new DPT().run();
    }

}
