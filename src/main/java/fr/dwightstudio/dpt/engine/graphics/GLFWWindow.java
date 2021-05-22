package fr.dwightstudio.dpt.engine.graphics;

import com.google.common.primitives.Ints;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.game.graphics.Tile;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import java.util.Objects;
import java.util.logging.Level;

import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL15.glDeleteBuffers;
import static org.lwjgl.system.MemoryUtil.NULL;
import static org.lwjgl.opengl.GL11.*;

public class GLFWWindow {

    private long window;
    final int WIDTH;
    final int HEIGHT;

    public GLFWWindow(int WIDTH, int HEIGHT) {
        this.WIDTH = WIDTH;
        this.HEIGHT = HEIGHT;
    }

    public int getWidth(){
        return WIDTH;
    }

    public int getHeight(){
        return HEIGHT;
    }

    public void init(){
        // Create an Error Callback which print the errors in System.err
        GLFWErrorCallback.createPrint(System.err).set();

        // Initialize GLFW. Throw an IllegalStateException if failed
        if ( !glfwInit() ) {
            GameLogger.logger.log(Level.SEVERE, "");
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        // Configure GLFW
        glfwDefaultWindowHints(); // optional, the current window hints are already the default
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE); // the window will stay hidden after creation
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE); // the window will be resizable

        // Create the window. Throw a RuntimeException if failed
        window = glfwCreateWindow(WIDTH, HEIGHT, "Don't Play Together 2.0", NULL, NULL);
        if ( window == NULL ) {
            GameLogger.logger.log(Level.SEVERE, "");
            throw new RuntimeException("Failed to create the GLFW window");
        }

        // Create a key callback. It will be called every time a key is pressed, repeated or released.
        KeyboardListener.getInstance();
        glfwSetKeyCallback(window, KeyboardListener.keyCallback);
        glfwSetMouseButtonCallback(window, MouseListener.mouseButtonCallback);
        glfwSetCursorPosCallback(window, MouseListener.cursorPosCallback);
        glfwSetScrollCallback(window, MouseListener.mouseScrollCallback);

        // Make the OpenGL context current
        glfwMakeContextCurrent(window);
        // Enable v-sync (no max fps)
        glfwSwapInterval(1);

        // Make the window visible
        glfwShowWindow(window);
        GameLogger.logger.log(Level.INFO, "Window initialized");
        loop();
    }

    private void loop() {
        // Called before any OpenGL function
        GL.createCapabilities();

        // Enable the GL_TEXTURE_2D feature
        glEnable(GL_TEXTURE_2D);

        // Setting up a projection matrix
        glMatrixMode(GL_PROJECTION);

        // Resets any previous projection matriced
        glLoadIdentity();

        // Create the orthographic projection
        // (0, 0) is the upper-left corner and (WIDTH, HEIGHT) the bottom-right corner
        glOrtho(0, WIDTH, HEIGHT, 0, 1, -1);
        glMatrixMode(GL_MODELVIEW);

        Texture texture = TextureLoader.loadTexture("./src/ressources/test.png");
        Tile tile = new Tile(400, 300, 100, texture);

        while (!glfwWindowShouldClose(window)) {
            // The key callback will be invoked only during this call
            glfwPollEvents();

            glClear(GL_COLOR_BUFFER_BIT); // clear the framebuffer

            tile.render();

            glfwSwapBuffers(window); // swap the color buffers
        }
        GameLogger.logger.log(Level.INFO, "Cleaning...");
        glfwFreeCallbacks(window);
        glfwDestroyWindow(window);
        glfwTerminate();
        Objects.requireNonNull(glfwSetErrorCallback(null)).free();
        int[] textures = Ints.toArray(TextureLoader.texturesList);
        int[] vbos = Ints.toArray(TexturedVBO.vboList);
        glDeleteTextures(textures);
        glDeleteBuffers(vbos);
        GameLogger.logger.log(Level.INFO, "Terminated");
    }
}
