package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.render.Shader;
import fr.dwightstudio.dpt.engine.graphics.render.Texture;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.primitives.Surface;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import org.joml.Vector2f;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class BatchRenderer {
    // This is what the array should looks like:
    //
    // Position                Color                    TextureCoords   TextureID
    // float, float,    float, float, float, float,     float, float    float
    //
    // NOTE: Here I put only x and y for position bacause we are working with 2d only in this BatchRender
    private final int POSITION_SIZE = 2;
    private final int COLOR_SIZE = 4;
    private final int TEXTURE_COORDS_SIZE = 2;
    private final int TEXTURE_ID_SIZE = 1;
    private final int VERTEX_SIZE = POSITION_SIZE + COLOR_SIZE + TEXTURE_COORDS_SIZE + TEXTURE_ID_SIZE;

    // Here are the 'offsets' in the array for each differents data
    private final int POSITION_OFFSET = 0;
    private final int COLOR_OFFSET = POSITION_OFFSET + POSITION_SIZE * Float.BYTES;
    private final int TEXTURE_COORDS_OFFSET = COLOR_OFFSET + COLOR_SIZE * Float.BYTES;
    private final int TEXTURE_ID_OFFSET = TEXTURE_COORDS_OFFSET + TEXTURE_COORDS_SIZE * Float.BYTES;

    private Surface[] surfaces;
    private List<Texture> textures;

    private int batchSize;
    private Shader shader;
    private float[] vertices;
    private int[] textureSlots = {0, 1, 2, 3, 4, 5, 6, 7};
    private int numberOfSurfaces;
    private boolean hasRoom;

    private int vertexBufferObjectID;
    private int vertexArrayObjectID;

    public BatchRenderer(int batchSize) {
        this.surfaces = new Surface[batchSize];
        this.textures = new ArrayList<>();

        this.batchSize = batchSize;
        ResourceManager.load("./src/main/resources/shaders/default.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/default.glsl");
        this.vertices = new float[batchSize * 4 * VERTEX_SIZE]; // The 4 is the number of vertices per quads
        this.numberOfSurfaces = 0;
        this.hasRoom = true;
    }

    public void start() {
        vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, (long) vertices.length * Float.BYTES, GL_DYNAMIC_DRAW);

        int elementBufferObjectID = glGenBuffers();
        int[] indices = generateIndices();
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBufferObjectID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, POSITION_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, POSITION_OFFSET);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, COLOR_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, COLOR_OFFSET);
        glEnableVertexAttribArray(1);

        glVertexAttribPointer(2, TEXTURE_COORDS_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, TEXTURE_COORDS_OFFSET);
        glEnableVertexAttribArray(2);

        glVertexAttribPointer(3, TEXTURE_ID_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, TEXTURE_ID_OFFSET);
        glEnableVertexAttribArray(3);
    }

    public void addSurface(Surface surface) {
        surfaces[numberOfSurfaces] = surface;

        loadVertexProperties(numberOfSurfaces);

        numberOfSurfaces++;
        if (numberOfSurfaces >= batchSize) {
            hasRoom = false;
        }
    }

    public void render() {
        boolean rebufferData = false;
        for (int i = 0; i < numberOfSurfaces; i++) {
            if (surfaces[i].isDirty()) {
                loadVertexProperties(i);
                surfaces[i].markClean();
                rebufferData = true;
            }
        }

        if (rebufferData) {
            glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices);
        }

        shader.bind();
        shader.uploadMat4f("uProjectionMatrix", SceneManager.getCurrentScene().getCamera().getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", SceneManager.getCurrentScene().getCamera().getViewMatrix());
        for (int i = 0; i < textures.size(); i++) {
            glActiveTexture(GL_TEXTURE0 + i + 1);
            textures.get(i).bind();
        }
        shader.uploadIntArray("uTextures", textureSlots);

        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(0);
        glEnableVertexAttribArray(1);

        glDrawElements(GL_TRIANGLES, numberOfSurfaces * 6, GL_UNSIGNED_INT, 0);

        glDisableVertexAttribArray(0);
        glDisableVertexAttribArray(1);
        glBindVertexArray(0);

        for (Texture texture : textures) {
            texture.unbind();
        }

        shader.unbind();
    }

    private int[] generateIndices() {
        // The indices array will look like this :
        //
        // int, int, int, int, int, int, <- 1 quad
        // int, int, int, int, int, int  <- 1 quad
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

    private void loadVertexProperties(int index) {
        Surface surface = this.surfaces[index];
        int offset = index * 4 * VERTEX_SIZE;

        if (surface.getTexture() != null) {
            if (!textures.contains(surface.getTexture())) {
                textures.add(surface.getTexture());
            }
        }

        int textureID = 0; // The texture ID 0 will never be used
        if (surface.getTexture() != null) {
            for (int i = 0; i < textures.size(); i++) {
                if (textures.get(i) == surface.getTexture()) {
                    textureID = i + 1;
                    break;
                }
            }
        }

        float x = (surface.getPosition().x - surface.getCenterPoint().x) + surface.getScale().x;
        float y = (surface.getPosition().y - surface.getCenterPoint().y) + surface.getScale().y;
        // This will loop 4 times for the 4 vertices.
        for (int i = 0; i < 4; i++) {
            if (i == 1) {
                y = surface.getPosition().y - surface.getCenterPoint().y;
            } else if (i == 2) {
                x = surface.getPosition().x - surface.getCenterPoint().x;
            } else if (i == 3) {
                y = (surface.getPosition().y - surface.getCenterPoint().y) + surface.getScale().y;
            }

            // Load the position
            vertices[offset] = (x * (float) Math.cos(surface.getRotation()) - y * (float) Math.sin(surface.getRotation())) + surface.getCenterPoint().x;
            vertices[offset + 1] = (x * (float) Math.sin(surface.getRotation()) + y * (float) Math.cos(surface.getRotation())) + surface.getCenterPoint().y;

            // Load the color
            vertices[offset + 2] = surface.getColor().getRed();
            vertices[offset + 3] = surface.getColor().getGreen();
            vertices[offset + 4] = surface.getColor().getBlue();
            vertices[offset + 5] = surface.getColor().getAlpha();


            // Load the texture coordinates
            vertices[offset + 6] = surface.getTextureCoords()[i].x;
            vertices[offset + 7] = surface.getTextureCoords()[i].y;

            // Load texture ID
            vertices[offset + 8] = textureID;


            offset += VERTEX_SIZE;
        }
    }

    public boolean hasRoom() {
        return hasRoom;
    }

}
