/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

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
    private Vector3f cameraFront;
    private Vector3f cameraUp;

    /**
     * Create a new Camera
     *
     * @param position the position of the camera
     */
    public Camera(Vector2f position) {
        this.position = position; // Since we are in a 2D view we don't need a Vector3
        this.projectionMatrix = new Matrix4f();
        this.viewMatrix = new Matrix4f();
        init();
        GameLogger.getLogger("Camera").debug(MessageFormat.format("Created a Camera object at : {0}, {1}", position.x, position.y));
    }

    private void init() {
        adjustProjection();
        this.cameraFront = new Vector3f(0.0f, 0.0f, -1.0f); // Set the front position of the camera
        this.cameraUp = new Vector3f(0.0f, 1.0f, 0.0f); // Set the up position of the camera (for the camera to go up we need to add +1 unit to the y axis)
    }

    /**
     * Reset the projection matrix
     */
    public void adjustProjection() {
        projectionMatrix.identity(); // Reset the projection matrix (put 0 everywhere)
        projectionMatrix.ortho(0.0f, GLFWWindow.getWidth(), 0.0f, GLFWWindow.getHeight(), 0.0f, 100.0f);
    }

    /**
     * @return the view matrix
     */
    public Matrix4f getViewMatrix() {
        this.viewMatrix.identity(); // Reset the wiew Matrix
        viewMatrix.lookAt(new Vector3f(position.x, position.y, 0.0f), // We are forced to use Vector3 here even if the z is unused
                          this.cameraFront.add(position.x, position.y, 0.0f), // The point were the camera look at. By default : 0, 0, -1
                          this.cameraUp);
        return this.viewMatrix;
    }

    /**
     * @return the projection matrix
     */
    public Matrix4f getProjectionMatrix() {
        return this.projectionMatrix;
    }

}
