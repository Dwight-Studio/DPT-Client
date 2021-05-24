package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.render.Shader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL20.*;

public class ShaderLoader {

    private static final StringBuilder vertexShader = new StringBuilder();
    private static final StringBuilder fragmentShader = new StringBuilder();
    private static String file;

    public static Shader loadShaderFile(String filepath) {
        file = filepath;

        try {
            BufferedReader fileBuffer = new BufferedReader(new FileReader(filepath));
            boolean readingVertexShader = false;
            boolean readingFragmentShader = false;
            String line;
            while ((line = fileBuffer.readLine()) != null) {
                if (line.contains("#type")) {
                    if (line.contains("vertex")) {
                        readingVertexShader = true;
                        readingFragmentShader = false;
                    } else if (line.contains("fragment")) {
                        readingVertexShader = false;
                        readingFragmentShader = true;
                    } else {
                        GameLogger.log(Level.SEVERE, "Unexpected token in line : {0}", new Object[] {line});
                    }
                } else if (readingVertexShader) {
                    vertexShader.append(line).append("\n");
                } else if (readingFragmentShader) {
                    fragmentShader.append(line).append("\n");
                } else {
                    GameLogger.log(Level.SEVERE, "Error while loading file : {0}", new Object[] {filepath});
                }
            }
            return compileShader();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static Shader compileShader() {
        int vertexID = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexID, vertexShader.toString());
        glCompileShader(vertexID);

        if (glGetShaderi(vertexID, GL_COMPILE_STATUS) == GL_FALSE) {
            GameLogger.log(Level.SEVERE, "Error compiling vertex shader : {0}", new Object[] {file});
            GameLogger.log(Level.SEVERE, glGetShaderInfoLog(vertexID, glGetShaderi(vertexID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        int fragmentID = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentID, fragmentShader.toString());
        glCompileShader(fragmentID);

        if (glGetShaderi(fragmentID, GL_COMPILE_STATUS) == GL_FALSE) {
            GameLogger.log(Level.SEVERE, "Error compiling fragment shader : {0}", new Object[] {file});
            GameLogger.log(Level.SEVERE, glGetShaderInfoLog(fragmentID, glGetShaderi(fragmentID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        int shaderProgramID = glCreateProgram();
        glAttachShader(shaderProgramID, vertexID);
        glAttachShader(shaderProgramID, fragmentID);

        glBindAttribLocation(shaderProgramID, 0, "vertices");

        glLinkProgram(shaderProgramID);

        if (glGetProgrami(shaderProgramID, GL_LINK_STATUS) == GL_FALSE) {
            GameLogger.log(Level.SEVERE, "Error linking shader : {0}", new Object[] {file});
            GameLogger.log(Level.SEVERE, glGetProgramInfoLog(fragmentID, glGetProgrami(shaderProgramID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        glValidateProgram(shaderProgramID);

        if (glGetProgrami(shaderProgramID, GL_VALIDATE_STATUS) != 1) {
            GameLogger.log(Level.SEVERE, "Error validating shader : {0}", new Object[] {file});
            GameLogger.log(Level.SEVERE, glGetProgramInfoLog(fragmentID, glGetProgrami(shaderProgramID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        glDeleteShader(vertexID);
        glDeleteShader(fragmentID);
        GameLogger.log(Level.FINE, "Successfully loaded and compiled shader : {0}", new Object[] {file});
        return new Shader(shaderProgramID);
    }
}
