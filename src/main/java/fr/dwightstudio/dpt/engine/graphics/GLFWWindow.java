/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics;

import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.graphics.utils.FramebufferManager;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import static fr.dwightstudio.dpt.engine.DSEngine.FULLSCREEN;
import static fr.dwightstudio.dpt.engine.DSEngine.WINDOWED;
import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryUtil.NULL;

public class GLFWWindow {

    private static long window;
    private static int WIDTH;
    private static int HEIGHT;
    private final long windowMode;
    private Thread eventThread;

    /**
     * Create a new GLFWWIndow
     *
     * @param WIDTH the width of the Window
     * @param HEIGHT the height of the Window
     * @param windowMode the window mode of the Window either Engine.FULLSCREEN or Engine.WINDOWED
     */
    public GLFWWindow(int WIDTH, int HEIGHT, long windowMode) {
        GLFWWindow.WIDTH = WIDTH;
        GLFWWindow.HEIGHT = HEIGHT;
        this.windowMode = windowMode;
        Thread.currentThread().setName("Main Render Thread");
    }

    /**
     * @return the window width
     */
    public static int getWidth(){
        return GLFWWindow.WIDTH;
    }

    /**
     * @return the window height
     */
    public static int getHeight(){
        return GLFWWindow.HEIGHT;
    }

    /**
     * @return the Window object
     */
    public static long getWindow() {
        return GLFWWindow.window;
    }

    /**
     * Init the window.
     * This is called automatically, it create the default OpenGL context
     */
    public void init(){

        GameLogger.init();

        GLFWErrorCallback.createPrint(System.err).set(); // Create an Error Callback which print the errors in System.err

        // Initialize GLFW. Throw an IllegalStateException if failed
        if ( !glfwInit() ) {
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        // Configure GLFW
        glfwDefaultWindowHints(); // optional, the current window hints are already the default
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE); // the window will stay hidden after creation
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE); // the window will be resizable

        // Create the window. Throw a RuntimeException if
        if (windowMode == FULLSCREEN) {
            window = glfwCreateWindow(GLFWWindow.WIDTH, GLFWWindow.HEIGHT, "Don't Play Together 2.0", glfwGetPrimaryMonitor(), NULL);
        } else if (windowMode == WINDOWED) {
            window = glfwCreateWindow(GLFWWindow.WIDTH, GLFWWindow.HEIGHT, "Don't Play Together 2.0", NULL, NULL);
        } else {
            window = NULL;
        }
        if ( window == NULL ) {
            throw new RuntimeException("Failed to create the GLFW window");
        }

        // Setting up callbacks
        this.eventThread = new Thread(new EventSystem(window));
        this.eventThread.setName("Event System Thread");
        this.eventThread.start();

        // Setting up the render
        glfwMakeContextCurrent(window); // Make the OpenGL context current
        glfwSwapInterval(1); // Enable v-sync
        // NOTE: If you have an NVIDIA graphics card and you are using a linux system, make sure the
        //      screen is in sync by enabling nvidia-drm with modprobe on linux
        glfwShowWindow(window); // Make the window visible
        GL.createCapabilities(); // Called before any OpenGL function
        glEnable(GL_TEXTURE_2D); // Enable the GL_TEXTURE_2D feature
        glEnable(GL_BLEND);
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA);
        glLoadIdentity(); // Resets any previous projection matrix
        GameLogger.getLogger("GLFWWindow").info("Window initialized");
    }

    /**
     * Start the window loop
     */
    public void startLoop() {
        double beginTime = glfwGetTime();
        double endTime;
        double dt = 0.0f;
        GameLogger.getLogger("GLFWWindow").info("Started the game loop");
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents(); // The key callback will be invoked only during this call

            render(dt);

            // Calculate the deltaTime
            endTime = glfwGetTime();
            dt = endTime - beginTime;
            beginTime = endTime;
        }

        // End of loop
        GameLogger.getLogger("GLFWWindow").info("Cleaning...");
        try {
            this.eventThread.join(); // Interrupt the eventThread
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        glfwFreeCallbacks(window); // Freeing all the callbacks
        glfwDestroyWindow(window); // Destroy the GLFWWindow
        glfwTerminate(); // Terminate GLFW
        GameLogger.getLogger("GLFWWindow").info("Terminated");
    }

    private void render(double dt) {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear the current framebuffer

        // Render the current scene
        if (SceneManager.getCurrentScene() != null) {
            SceneManager.getCurrentScene().update(dt);
        }

        FramebufferManager.renderAll();
        glfwSwapBuffers(window); // Swap the buffers
    }
}
