package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;

public class dpt {

    public GLFWWindow window = new GLFWWindow(1280, 720);

    public void run(){

        window.init();

    }

    public static void main(String[] args){
        new dpt().run();
    }

}
