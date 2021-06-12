/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.*;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;

import static org.lwjgl.opengl.GL20.*;

public class Shader {

    private final int programID;
    private boolean isInUse = false;

    /**
     * Create a new Shader
     *
     * @param programID the program ID of the shader
     */
    public Shader(int programID) {
        this.programID = programID;
    }

    /**
     * Bind the shader to use it
     */
    public void bind() {
        if (!isInUse) {
            glUseProgram(programID);
            isInUse = true;
        }
    }

    /**
     * Unbind the shader
     */
    public void unbind() {
        if (isInUse) {
            glUseProgram(0);
            isInUse = false;
        }
    }

    /**
     * Delete the Shader
     */
    public void delete() {
        glDeleteProgram(programID);
    }

    /**
     * @return is the shader is in use
     */
    public boolean isInUse() {
        return isInUse;
    }

    /**
     * Upload a Matrix4f to the shader
     *
     * @param varName the variable name to upload to
     * @param mat4 the Matrix4f to upload
     */
    public void uploadMat4f(String varName, Matrix4f mat4) {
        // First here is to transfrom our Matrix4f into a 1D matrix
        // [[0, 0, 0, 0],
        //  [0, 0, 0, 0],     to      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        //  [0, 0, 0, 0],
        //  [0, 0, 0, 0]]
        FloatBuffer matBuffer = BufferUtils.createFloatBuffer(16);
        mat4.get(matBuffer);
        bind();
        glUniformMatrix4fv(glGetUniformLocation(programID, varName), false, matBuffer);
    }

    /**
     * Upload a Matrix3f to the shader
     *
     * @param varName the variable name to upload to
     * @param mat3 the Matrix3f to upload
     */
    public void uploadMat3f(String varName, Matrix3f mat3) {
        // First here is to transfrom our Matrix3f into a 1D matrix
        // [[0, 0, 0, 0],
        //  [0, 0, 0, 0],     to      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        //  [0, 0, 0, 0],
        //  [0, 0, 0, 0]]
        FloatBuffer matBuffer = BufferUtils.createFloatBuffer(9);
        mat3.get(matBuffer);
        bind();
        glUniformMatrix3fv(glGetUniformLocation(programID, varName), false, matBuffer);
    }

    /**
     * Upload a boolean to the shader
     *
     * @param varName the variable name to upload to
     * @param bool the boolean to upload
     */
    public void uploadBoolean(String varName, boolean bool) {
        int val = (bool) ? 1 : 0;
        bind();
        glUniform1i(glGetUniformLocation(programID, varName), val);
    }

    /**
     * Upload an integer to the shader
     *
     * @param varName the variable name to upload to
     * @param val the integer to upload
     */
    public void uploadInt(String varName, int val) {
        bind();
        glUniform1i(glGetUniformLocation(programID, varName), val);
    }

    /**
     * Upload a float to the shader
     *
     * @param varName the variable name to upload to
     * @param val the float to upload
     */
    public void uploadFloat(String varName, float val) {
        bind();
        glUniform1f(glGetUniformLocation(programID, varName), val);
    }

    /**
     * Upload a Vector4f to the shader
     *
     * @param varName the variable name to upload to
     * @param vec4f the Vector4f to upload
     */
    public void uploadVec4f(String varName, Vector4f vec4f) {
        bind();
        glUniform4f(glGetUniformLocation(programID, varName), vec4f.x, vec4f.y, vec4f.z, vec4f.w);
    }

    /**
     * Upload a Vector3f to the shader
     *
     * @param varName the variable name to upload to
     * @param vec3f the Vector3f to upload
     */
    public void uploadVec3f(String varName, Vector3f vec3f) {
        bind();
        glUniform3f(glGetUniformLocation(programID, varName), vec3f.x, vec3f.y, vec3f.z);
    }

    /**
     * Upload a Vector2f to the shader
     *
     * @param varName the variable name to upload to
     * @param vec2f the Vector2f to upload
     */
    public void uploadVec2f(String varName, Vector2f vec2f) {
        bind();
        glUniform2f(glGetUniformLocation(programID, varName), vec2f.x, vec2f.y);
    }

    /**
     * Upload an integer array to the shader
     *
     * @param varName tha variable name to upload to
     * @param array the integer array to upload
     */
    public void uploadIntArray(String varName, int[] array) {
        bind();
        glUniform1iv(glGetUniformLocation(programID, varName), array);
    }

    /**
     * @return the shader program ID
     */
    public int getProgramID() {
        return programID;
    }
}
