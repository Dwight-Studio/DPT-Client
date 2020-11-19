package fr.dwightstudio.dpt;

import org.lwjgl.glfw.GLFWErrorCallback;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.system.MemoryUtil.*;

public class main {

    private long window;
    private int WIDTH = 300;
    private int HEIGHT = 300;

    public int getWindowWidth() {
        return WIDTH;
    }

    public int getWindowHeight(){
        return HEIGHT;
    }

    private void init(){

        // Initialize the error callback and print the errors in System.err
        GLFWErrorCallback.createPrint(System.err).set();

        // Initialize GLFW, will throw an IllegalStateException if errors
        if ( !glfwInit() ){
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        // Make the window resizable
        glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE);

        // Create the window
        window = glfwCreateWindow(WIDTH, HEIGHT, "Don't Play Together : Java Edition", NULL, NULL);

        // Throw a RuntimeException if errors when creating the window
        if ( window == NULL ){
            throw new RuntimeException("Failed to create the GLFW window");
        }

        // Initialize a key callback that will be called every time a key is pressed, repeated or released
        glfwSetKeyCallback(window, (window, key, scancode, action, mods) -> {
            glfwSetWindowShouldClose(window, true);
        });
    }

}
