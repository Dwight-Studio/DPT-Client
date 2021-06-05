package fr.dwightstudio.dpt.engine.graphics.objects;

import org.joml.*;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;

import static org.lwjgl.opengl.GL20.*;

public class Shader {

    private final int programID;
    private boolean isInUse = false;

    public Shader(int programID) {
        this.programID = programID;
    }

    public void bind() {
        if (!isInUse) {
            glUseProgram(programID);
            isInUse = true;
        }
    }

    public void unbind() {
        if (isInUse) {
            glUseProgram(0);
            isInUse = false;
        }
    }

    public void delete() {
        glDeleteProgram(programID);
    }

    public boolean isInUse() {
        return isInUse;
    }

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


    public void uploadBoolean(String varName, boolean bool) {
        int val = (bool) ? 1 : 0;
        bind();
        glUniform1i(glGetUniformLocation(programID, varName), val);
    }

    public void uploadInt(String varName, int val) {
        bind();
        glUniform1i(glGetUniformLocation(programID, varName), val);
    }

    public void uploadFloat(String varName, float val) {
        bind();
        glUniform1f(glGetUniformLocation(programID, varName), val);
    }

    public void uploadVec4f(String varName, Vector4f vec4f) {
        bind();
        glUniform4f(glGetUniformLocation(programID, varName), vec4f.x, vec4f.y, vec4f.z, vec4f.w);
    }

    public void uploadVec3f(String varName, Vector3f vec3f) {
        bind();
        glUniform3f(glGetUniformLocation(programID, varName), vec3f.x, vec3f.y, vec3f.z);
    }

    public void uploadVec2f(String varName, Vector2f vec2f) {
        bind();
        glUniform2f(glGetUniformLocation(programID, varName), vec2f.x, vec2f.y);
    }

    public void uploadIntArray(String varname, int[] array) {
        bind();
        glUniform1iv(glGetUniformLocation(programID, varname), array);
    }
}
