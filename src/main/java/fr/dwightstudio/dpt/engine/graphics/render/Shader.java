package fr.dwightstudio.dpt.engine.graphics.render;

import org.joml.Matrix4f;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;

import static org.lwjgl.opengl.GL20.*;

public class Shader {

    private final int programID;

    public Shader(int programID) {
        this.programID = programID;
    }

    public void bind() {
        glUseProgram(programID);
    }

    public void unbind() {
        glUseProgram(0);
    }

    public void delete() {
        glDeleteProgram(programID);
    }

    public void uploadMat4f(String varName, Matrix4f mat4) {
        FloatBuffer matBuffer = BufferUtils.createFloatBuffer(16);
        mat4.get(matBuffer);
        glUniformMatrix4fv(glGetUniformLocation(programID, varName), false, matBuffer);
    }
}
