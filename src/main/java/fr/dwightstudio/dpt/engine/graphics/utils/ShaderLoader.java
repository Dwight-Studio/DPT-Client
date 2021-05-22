package fr.dwightstudio.dpt.engine.graphics.utils;

public class ShaderLoader {
    private String vertexShader = "#version 330 core\n" +
            "\n" +
            "layout (location=0) in vec3 vPos;\n" +
            "layout (location=1) in vec4 vColor;\n" +
            "\n" +
            "out vec4 fColor;\n" +
            "\n" +
            "void main() {\n" +
            "    fColor = vColor;\n" +
            "    gl_Position = vec4(vPos, 1.0);\n" +
            "}";

    private String fragmentShader = "#version 330 core\n" +
            "\n" +
            "in vec4 fColor;\n" +
            "\n" +
            "out vec4 color;\n" +
            "\n" +
            "void main() {\n" +
            "    color = fColor;\n" +
            "}";

    private int vertexID;
    private int fragmentID;
    private int shaderProgramID;
}
