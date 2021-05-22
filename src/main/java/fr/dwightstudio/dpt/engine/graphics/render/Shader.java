package fr.dwightstudio.dpt.engine.graphics.render;

import static org.lwjgl.opengl.GL20.glDeleteProgram;
import static org.lwjgl.opengl.GL20.glUseProgram;

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
}
