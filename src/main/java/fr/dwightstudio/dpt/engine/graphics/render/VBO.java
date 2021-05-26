package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.graphics.utils.ShaderLoader;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.utils.Time;
import org.joml.Vector2f;
import org.lwjgl.BufferUtils;

import java.nio.FloatBuffer;
import java.nio.IntBuffer;
import java.text.MessageFormat;
import java.util.Objects;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

// VBO = Vertex Buffer Object
public class VBO {

    private final static Shader shader = ShaderLoader.loadShaderFile("./src/main/resources/shaders/default.glsl");
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

        int positionSize = 3;
        int colorSize = 4;
        int textureCoordsSize = 2;
        int vertexSizeBytes = (positionSize + colorSize + textureCoordsSize) * Float.BYTES;

        glVertexAttribPointer(0, positionSize, GL_FLOAT, false, vertexSizeBytes, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, colorSize, GL_FLOAT, false, vertexSizeBytes, positionSize * Float.BYTES);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, textureCoordsSize, GL_FLOAT, false, vertexSizeBytes, (positionSize + colorSize) * Float.BYTES);
        glEnableVertexAttribArray(2);

        GameLogger.getLogger().debug(MessageFormat.format("Created a VBO with id : {0}, {1}, {2}", vertexArrayObjectID, vertexBufferObjectID, elementBufferObjectID));
    }

    public void render(boolean usingTexture, boolean moving) {
        if (moving) {
            camera.position.x -= Time.getDTime() * 50.0f;
            camera.position.y -= Time.getDTime() * 25.0f;
        }
        Objects.requireNonNull(shader).bind();
        shader.uploadBoolean("usingTexture", usingTexture);
        shader.uploadInt("textureSampler", 0);
        glActiveTexture(GL_TEXTURE0);
        shader.uploadMat4f("uProjectionMatrix", camera.getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", camera.getViewMatrix());
        shader.uploadFloat("uTime", Time.getDeltaTime());
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
