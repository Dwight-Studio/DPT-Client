package fr.dwightstudio.dpt;

import fr.dwightstudio.dpt.engine.graphics.VideoInit;

public class dpt {

    public VideoInit video = new VideoInit(300, 300);

    public void run(){

        video.init();

    }

    public static void main(String[] args){
        new dpt().run();
    }

}
