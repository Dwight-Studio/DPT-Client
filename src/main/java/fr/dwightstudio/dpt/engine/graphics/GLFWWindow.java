/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics;

import fr.dwightstudio.dpt.engine.events.EventSystem;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.Time;
import fr.dwightstudio.dpt.game.levels.MainScene;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import static fr.dwightstudio.dpt.engine.Engine.FULLSCREEN;
import static fr.dwightstudio.dpt.engine.Engine.WINDOWED;
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
        loop(); // Start the loop
    }

    /**
     * Start the window loop
     */
    private void loop() {

        /*int frameBufferObject;
        frameBufferObject = glGenFramebuffers();
        glBindFramebuffer(GL_FRAMEBUFFER, frameBufferObject);

        int textureBuffer;
        textureBuffer = glGenTextures();
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, GLFWWindow.getWidth(), GLFWWindow.getHeight(), 0, GL_RGBA, GL_UNSIGNED_BYTE, 0);
        glBindTexture(GL_TEXTURE_2D, 0); // Unbinding any texture at the end to make sure it is not modified after
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, textureBuffer, 0);

        int renderBufferObject;
        renderBufferObject = glGenRenderbuffers();
        glBindRenderbuffer(GL_RENDERBUFFER, renderBufferObject);
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT32, GLFWWindow.getWidth(), GLFWWindow.getHeight());
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderBufferObject);
        glBindRenderbuffer(GL_RENDERBUFFER, 0);

        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
            GameLogger.getLogger("GLFWWindow").error("The Framebuffer is not complete");
        }
        glBindFramebuffer(GL_FRAMEBUFFER, 0);*/

        SceneManager.changeScene(new MainScene()); // By default the MainScene is instanciated

        float beginTime = Time.getDeltaTime();
        float endTime;
        float dt = -1.0f;

        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents(); // The key callback will be invoked only during this call

            //glBindFramebuffer(GL_FRAMEBUFFER, frameBufferObject);
            glClear(GL_COLOR_BUFFER_BIT); // Clear the framebuffer

            if (dt >= 0) {
                SceneManager.getCurrentScene().update(dt);
            }
            //glBindFramebuffer(GL_FRAMEBUFFER, 0);

            glfwSwapBuffers(window); // Swap the color buffers

            endTime = Time.getDeltaTime();
            dt = endTime - beginTime;
            Time.setDTime(dt);
            // System.out.println(Math.round(1.0f / dt) + " FPS");
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
}
