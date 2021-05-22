package fr.dwightstudio.dpt.engine.graphics;

import com.google.common.primitives.Ints;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.render.TexturedVBO;
import fr.dwightstudio.dpt.engine.graphics.utils.TextureLoader;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.Time;
import fr.dwightstudio.dpt.game.graphics.Tile;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

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

        GLFWErrorCallback.createPrint(System.err).set(); // Create an Error Callback which print the errors in System.err

        // Initialize GLFW. Throw an IllegalStateException if failed
        if ( !glfwInit() ) {
            throw new IllegalStateException("Unable to initialize GLFW");
        }

        // Configure GLFW
        glfwDefaultWindowHints(); // optional, the current window hints are already the default
        glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE); // the window will stay hidden after creation
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE); // the window will be resizable

        // Create the window. Throw a RuntimeException if failed
        window = glfwCreateWindow(WIDTH, HEIGHT, "Don't Play Together 2.0", NULL, NULL);
        if ( window == NULL ) {
            throw new RuntimeException("Failed to create the GLFW window");
        }

        // Setting up callbacks
        glfwSetKeyCallback(window, KeyboardListener.keyCallback); // Setup a key callback
        glfwSetMouseButtonCallback(window, MouseListener.mouseButtonCallback); // Setup a mouse buttons callback
        glfwSetCursorPosCallback(window, MouseListener.cursorPosCallback); // Setup a mouse cursor callback
        glfwSetScrollCallback(window, MouseListener.mouseScrollCallback); // Setup a mouse scroll whell callback

        // Setting up the render
        glfwMakeContextCurrent(window); // Make the OpenGL context current
        glfwSwapInterval(1); // Enable v-sync (no max fps)
        glfwShowWindow(window); // Make the window visible
        GL.createCapabilities(); // Called before any OpenGL function
        glEnable(GL_TEXTURE_2D); // Enable the GL_TEXTURE_2D feature
        glMatrixMode(GL_PROJECTION); // Setting up a projection matrix
        glLoadIdentity(); // Resets any previous projection matriced
        // NOTE: (0, 0) is the upper-left corner and (WIDTH, HEIGHT) the bottom-right corner
        glOrtho(0, WIDTH, HEIGHT, 0, 1, -1); // Create the orthographic projection
        glMatrixMode(GL_MODELVIEW);
        GameLogger.logger.log(Level.INFO, "Window initialized");
        loop(); // Start the loop
    }

    private void loop() {
        Texture texture = TextureLoader.loadTexture("./src/ressources/test.png");
        Tile tile = new Tile(400, 300, 100, texture);
        Tile tile2 = new Tile(200, 150, 100, texture);

        float beginTime = Time.getDeltaTime();
        float endTime;

        while (!glfwWindowShouldClose(window)) {

            glfwPollEvents(); // The key callback will be invoked only during this call

            glClear(GL_COLOR_BUFFER_BIT); // Clear the framebuffer

            tile.render();
            tile2.render();

            glfwSwapBuffers(window); // Swap the color buffers

            endTime = Time.getDeltaTime();
            float dt = endTime - beginTime;
            //System.out.println(Math.round(1.0f / dt) + " FPS");
            beginTime = endTime;
        }

        // End of loop
        GameLogger.logger.log(Level.INFO, "Cleaning...");
        glfwFreeCallbacks(window); // Freeing all the callbacks
        glfwDestroyWindow(window); // Destroy the GLFWWindow
        glfwTerminate(); // Terminate GLFW
        glDeleteTextures(Ints.toArray(TextureLoader.texturesList)); // Delete all the textures
        glDeleteBuffers(Ints.toArray(TexturedVBO.vboList)); // Delete all the buffers
        GameLogger.logger.log(Level.INFO, "Terminated");
    }
}
