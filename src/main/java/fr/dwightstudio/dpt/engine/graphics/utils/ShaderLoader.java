/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.utils;

import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.MessageFormat;

import static org.lwjgl.opengl.GL20.*;

public class ShaderLoader {

    private static StringBuilder vertexShader;
    private static StringBuilder fragmentShader;
    private static String file;

    /**
     * Load a GLSL shader file and create a Shader object with it
     *
     * @param filepath the shader filepath
     * @return the loaded Shader
     */
    public static Shader loadShaderFile(String filepath) {
        file = filepath;
        vertexShader = new StringBuilder();
        fragmentShader = new StringBuilder();

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
                        GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Unexpected token in line : {0}", line));
                    }
                } else if (readingVertexShader) {
                    vertexShader.append(line).append("\n");
                } else if (readingFragmentShader) {
                    fragmentShader.append(line).append("\n");
                } else {
                    GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Error while loading file : {0}", filepath));
                }
            }
            return compileShader();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Compile a GLSL shader
     *
     * @return a Shader
     */
    private static Shader compileShader() {
        int vertexID = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexID, vertexShader.toString());
        glCompileShader(vertexID);

        if (glGetShaderi(vertexID, GL_COMPILE_STATUS) == GL_FALSE) {
            GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Error compiling vertex shader : {0}", file));
            GameLogger.getLogger("ShaderLoader").fatal(glGetShaderInfoLog(vertexID, glGetShaderi(vertexID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        int fragmentID = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentID, fragmentShader.toString());
        glCompileShader(fragmentID);

        if (glGetShaderi(fragmentID, GL_COMPILE_STATUS) == GL_FALSE) {
            GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Error compiling fragment shader : {0}", file));
            GameLogger.getLogger("ShaderLoader").fatal(glGetShaderInfoLog(fragmentID, glGetShaderi(fragmentID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        int shaderProgramID = glCreateProgram();
        glAttachShader(shaderProgramID, vertexID);
        glAttachShader(shaderProgramID, fragmentID);

        glBindAttribLocation(shaderProgramID, 0, "vertices");

        glLinkProgram(shaderProgramID);

        if (glGetProgrami(shaderProgramID, GL_LINK_STATUS) == GL_FALSE) {
            GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Error linking shader : {0}", file));
            GameLogger.getLogger("ShaderLoader").fatal(glGetProgramInfoLog(fragmentID, glGetProgrami(shaderProgramID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        glValidateProgram(shaderProgramID);

        if (glGetProgrami(shaderProgramID, GL_VALIDATE_STATUS) != 1) {
            GameLogger.getLogger("ShaderLoader").fatal(MessageFormat.format("Error validating shader : {0}", file));
            GameLogger.getLogger("ShaderLoader").fatal(glGetProgramInfoLog(fragmentID, glGetProgrami(shaderProgramID, GL_INFO_LOG_LENGTH)));
            return null;
        }

        glDeleteShader(vertexID);
        glDeleteShader(fragmentID);
        GameLogger.getLogger("ShaderLoader").debug(MessageFormat.format("Successfully loaded and compiled shader : {0}", file));
        return new Shader(shaderProgramID);
    }
}
