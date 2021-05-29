package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.scripting.Component;
import fr.dwightstudio.dpt.engine.utils.RessourceManager;

import java.util.Objects;

import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class BatchRenderer {
    // This is what the array should looks like:
    //
    // Position         Color                           TextureCoords
    // float, float,    float, float, float, float,     float, float
    //
    // NOTE: Here I put only x and y for position bacause we are working with 2d only in this BatchRender
    private final int POSITION_SIZE = 2;
    private final int COLOR_SIZE = 4;
    private final int TEXTURE_COORDS_SIZE = 2;
    private final int VERTEX_SIZE = POSITION_SIZE + COLOR_SIZE + TEXTURE_COORDS_SIZE;

    // Here are the 'offsets' in the array for each differents data
    private final int POSITION_OFFSET = 0;
    private final int COLOR_OFFSET = POSITION_OFFSET + POSITION_SIZE * Float.BYTES;
    private final int TEXTURE_COORDS_OFFSET = COLOR_OFFSET + COLOR_SIZE * Float.BYTES;

    private int batchSize;
    private Component[] components;
    private Shader shader;
    private float[] vertices;
    private int numberOfGameObjects;
    private boolean hasRoom;
    private int vertexBufferObjectID;
    private int vertexArrayObjectID;

    public BatchRenderer(int batchSize) {
        this.batchSize = batchSize;
        this.components = new Component[batchSize];
        shader = RessourceManager.getShader("./src/main/resources/shaders/default.glsl");

        this.vertices = new float[batchSize * 4 * VERTEX_SIZE]; // The 4 is the number of vertices per quads
        this.numberOfGameObjects = 0;
        this.hasRoom = true;
    }

    public void start() {
        int vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, (long) vertices.length * Float.BYTES, GL_DYNAMIC_DRAW);

        int elementBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBufferObjectID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, generateIndices(), GL_STATIC_DRAW);

        glVertexAttribPointer(0, POSITION_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, POSITION_OFFSET);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, COLOR_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, COLOR_OFFSET);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, TEXTURE_COORDS_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, TEXTURE_COORDS_OFFSET);
        glEnableVertexAttribArray(2);
    }

    public void addGameObject(Component component) {
        components[this.numberOfGameObjects] = component;
        numberOfGameObjects++;

        if (numberOfGameObjects >= batchSize) {
            hasRoom = false;
        }
    }

    public void render() {
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices);
        Objects.requireNonNull(shader).bind();
        shader.uploadMat4f("uProjectionMatrix", SceneManager.getCurrentScene().getCamera().getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", SceneManager.getCurrentScene().getCamera().getViewMatrix());
        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(0);
        glEnableVertexAttribArray(1);;
        glDrawElements(GL_TRIANGLES, numberOfGameObjects * 6, GL_UNSIGNED_INT, 0);

        glDisableVertexAttribArray(0);
        glDisableVertexAttribArray(1);
        glBindVertexArray(0);
        shader.unbind();
    }

    private int[] generateIndices() {
        // The indices array will look like this :
        //
        // int, int, int, int, int, int,
        // int, int, int, int, int, int
        //
        // NOTE: We have 2 triangles with 3 indices each to form a quad so 3*2=6
        int[] elements = new int[6 * batchSize];
        for (int i = 0; i < batchSize; i++) {
            int offsetArrayIndex = 6 * i;

            // First Triangle
            elements[offsetArrayIndex] = 4 * i + 3;
            elements[offsetArrayIndex + 1] = 4 * i + 2;
            elements[offsetArrayIndex + 2] = 4 * i;

            // Second Triangle
            elements[offsetArrayIndex + 3] = 4 * i;
            elements[offsetArrayIndex + 4] = 4 * i + 2;
            elements[offsetArrayIndex + 5] = 4 * i + 1;
        }

        return elements;
    }

}
