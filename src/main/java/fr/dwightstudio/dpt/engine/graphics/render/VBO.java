package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.Time;
import org.joml.Vector2f;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;
import java.nio.IntBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

// VBO = Vertex Buffer Object
public class VBO {

    public static List<Integer> vboList = new ArrayList<>();

    private final Shader shader = ShaderLoader.loadShaderFile("./src/ressources/shaders/default.glsl");
    private final Camera camera = new Camera(new Vector2f());

    private final int vertexArrayObjectID;
    private final int[] elementArray;

    public VBO(float[] vertexArray, int[] elementArray) {
        this.elementArray = elementArray;

        vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        FloatBuffer vertexArrayBuffer = BufferUtils.createFloatBuffer(vertexArray.length);
        vertexArrayBuffer.put(vertexArray).flip();

        int vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, vertexArrayBuffer, GL_STATIC_DRAW);

        IntBuffer elementBuffer = BufferUtils.createIntBuffer(elementArray.length);
        elementBuffer.put(elementArray).flip();

        int elementBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBufferObjectID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elementBuffer, GL_STATIC_DRAW);

        vboList.add(vertexBufferObjectID);
        vboList.add(elementBufferObjectID);

        int positionSize = 3;
        int colorSize = 4;
        int vertexSizeBytes = (positionSize + colorSize) * Float.BYTES;

        glVertexAttribPointer(0, positionSize, GL_FLOAT, false, vertexSizeBytes, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, colorSize, GL_FLOAT, false, vertexSizeBytes, positionSize * Float.BYTES);
        glEnableVertexAttribArray(1);

        GameLogger.logger.log(Level.FINE, "Created a Textured VBO with id : {0}, {1}", new Object[] {vertexBufferObjectID, elementBufferObjectID});
    }

    public void render() {
        camera.position.x -= Time.getDTime() * 50.0f;
        Objects.requireNonNull(shader).bind();
        shader.uploadMat4f("uProjectionMatrix", camera.getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", camera.getViewMatrix());
        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(0);
        glEnableVertexAttribArray(1);
        glDrawElements(GL_TRIANGLES, elementArray.length, GL_UNSIGNED_INT, 0);

        glDisableVertexAttribArray(0);
        glDisableVertexAttribArray(1);
        glBindVertexArray(0);
        shader.unbind();
    }
}
