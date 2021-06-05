package fr.dwightstudio.dpt.engine.graphics.objects;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;

import java.text.MessageFormat;

public class Camera {
    private final Matrix4f projectionMatrix;
    private final Matrix4f viewMatrix;
    public final Vector2f position;

    public Camera(Vector2f position) {
        this.position = position; // Since we are in a 2D view we don't need a Vector3
        this.projectionMatrix = new Matrix4f();
        this.viewMatrix = new Matrix4f();
        adjustProjection();
        GameLogger.getLogger("Camera").debug(MessageFormat.format("Created a Camera object at : {0}, {1}", position.x, position.y));
    }

    public void adjustProjection() {
        projectionMatrix.identity(); // Reset the projection matrix (put 0 everywhere)
        projectionMatrix.ortho(0.0f, GLFWWindow.getWidth(), 0.0f, GLFWWindow.getHeight(), 0.0f, 100.0f);
    }

    public Matrix4f getViewMatrix() {
        Vector3f cameraFront = new Vector3f(0.0f, 0.0f, -1.0f); // Set the front position of the camera
        Vector3f cameraUp = new Vector3f(0.0f, 1.0f, 0.0f); // Set the up position of the camera (for the camera to go up we need to add +1 unit to the y axis)
        this.viewMatrix.identity(); // Reset the wiew Matrix
        viewMatrix.lookAt(new Vector3f(position.x, position.y, 0.0f), // We are forced to use Vector3 here even if the z is unused
                          cameraFront.add(position.x, position.y, 0.0f), // The point were the camera look at. By default : 0, 0, -1
                          cameraUp);
        return this.viewMatrix;
    }

    public Matrix4f getProjectionMatrix() {
        return this.projectionMatrix;
    }

}
