package fr.dwightstudio.dpt.engine.graphics;

import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.glfw.GLFWVidMode;
import org.lwjgl.opengl.GL;
import org.lwjgl.system.MemoryStack;

import java.nio.IntBuffer;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.system.MemoryStack.stackPush;
import static org.lwjgl.system.MemoryUtil.NULL;
import static org.lwjgl.opengl.GL11.*;

public class GLFWWindow {

    private long window;
    int v_WIDTH;
    int v_HEIGHT;

    public GLFWWindow(int WIDTH, int HEIGHT) {
        v_WIDTH = WIDTH;
        v_HEIGHT = HEIGHT;
    }

    public int getWidth(){
        return v_WIDTH;
    }

    public int getHeight(){
        return v_HEIGHT;
    }

    public void init(){
        // Create an Error Callback which print the errors in System.err
        GLFWErrorCallback.createPrint(System.err).set();

        // Initialize GLFW. Throw an IllegalStateException if failed
        if ( !glfwInit() )
            throw new IllegalStateException("Unable to initialize GLFW");

        // Configure GLFW
        glfwDefaultWindowHints(); // optional, the current window hints are already the default
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE); // the window will stay hidden after creation
        glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE); // the window will be resizable

        // Create the window. Throw a RuntimeException if failed
        window = glfwCreateWindow(v_WIDTH, v_HEIGHT, "Don't Play Together Java Edition", NULL, NULL);
        if ( window == NULL )
            throw new RuntimeException("Failed to create the GLFW window");

        // Create a key callback. It will be called every time a key is pressed, repeated or released.
        glfwSetKeyCallback(window, (window, key, scancode, action, mods) -> {
            if ( key == GLFW_KEY_ESCAPE && action == GLFW_RELEASE )
                glfwSetWindowShouldClose(window, true); // We will detect this in the rendering loop
        });

        // Make the OpenGL context current
        glfwMakeContextCurrent(window);
        // Enable v-sync
        glfwSwapInterval(1);

        // Make the window visible
        glfwShowWindow(window);
        loop();
    }

    private void loop(){
        // Called before any OpenGL function
        GL.createCapabilities();

        // Set the default background color of the window
        glClearColor(1.0f, 0.0f, 0.0f, 0.0f);

        while (!glfwWindowShouldClose(window)){

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // clear the framebuffer

            glfwSwapBuffers(window); // swap the color buffers

            // The key callback will be invoked only during this call
            glfwPollEvents();

        }
    }

}
