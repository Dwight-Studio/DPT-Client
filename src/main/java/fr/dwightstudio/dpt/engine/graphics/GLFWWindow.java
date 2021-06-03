package fr.dwightstudio.dpt.engine.graphics;

import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.inputs.KeyboardListener;
import fr.dwightstudio.dpt.engine.inputs.MouseListener;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.Time;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;

import static fr.dwightstudio.dpt.engine.Engine.ENGINE_FULLSCREEN;
import static fr.dwightstudio.dpt.engine.Engine.ENGINE_WINDOWED;
import static org.lwjgl.glfw.Callbacks.glfwFreeCallbacks;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryUtil.NULL;

public class GLFWWindow {

    private long window;
    private static int WIDTH;
    private static int HEIGHT;
    private final long windowMode;

    public GLFWWindow(int WIDTH, int HEIGHT, long windowMode) {
        GLFWWindow.WIDTH = WIDTH;
        GLFWWindow.HEIGHT = HEIGHT;
        this.windowMode = windowMode;
    }

    public static int getWidth(){
        return GLFWWindow.WIDTH;
    }

    public static int getHeight(){
        return GLFWWindow.HEIGHT;
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

        // Create the window. Throw a RuntimeException if
        if (windowMode == ENGINE_FULLSCREEN) {
            window = glfwCreateWindow(GLFWWindow.WIDTH, GLFWWindow.HEIGHT, "Don't Play Together 2.0", glfwGetPrimaryMonitor(), NULL);
        } else if (windowMode == ENGINE_WINDOWED) {
            window = glfwCreateWindow(GLFWWindow.WIDTH, GLFWWindow.HEIGHT, "Don't Play Together 2.0", NULL, NULL);
        } else {
            window = NULL;
        }
        if ( window == NULL ) {
            throw new RuntimeException("Failed to create the GLFW window");
        }

        // Setting up callbacks
        glfwSetKeyCallback(window, KeyboardListener.keyCallback); // Setup a key callback
        glfwSetMouseButtonCallback(window, MouseListener.mouseButtonCallback); // Setup a mouse buttons callback
        glfwSetCursorPosCallback(window, MouseListener.cursorPosCallback); // Setup a mouse cursor callback
        glfwSetScrollCallback(window, MouseListener.mouseScrollCallback); // Setup a mouse scroll wheel callback

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

    private void loop() {

        SceneManager.changeScene(0); // By default the scene with index 0 is instantiated

        float beginTime = Time.getDeltaTime();
        float endTime;
        float dt = -1.0f;

        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents(); // The key callback will be invoked only during this call

            glClear(GL_COLOR_BUFFER_BIT); // Clear the framebuffer

            if (dt >= 0) {
                SceneManager.getCurrentScene().update(dt);
            }

            glfwSwapBuffers(window); // Swap the color buffers

            endTime = Time.getDeltaTime();
            dt = endTime - beginTime;
            Time.setDTime(dt);
            // System.out.println(Math.round(1.0f / dt) + " FPS");
            beginTime = endTime;
        }

        // End of loop
        GameLogger.getLogger("GLFWWindow").info("Cleaning...");
        glfwFreeCallbacks(window); // Freeing all the callbacks
        glfwDestroyWindow(window); // Destroy the GLFWWindow
        glfwTerminate(); // Terminate GLFW
        GameLogger.getLogger("GLFWWindow").info("Terminated");
    }
}
