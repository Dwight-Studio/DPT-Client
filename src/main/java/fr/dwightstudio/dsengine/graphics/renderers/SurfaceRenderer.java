/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.renderers;

import fr.dwightstudio.dsengine.graphics.objects.Shader;
import fr.dwightstudio.dsengine.graphics.objects.Texture;
import fr.dwightstudio.dsengine.graphics.objects.Transform;
import fr.dwightstudio.dsengine.graphics.primitives.Surface;
import fr.dwightstudio.dsengine.graphics.utils.SceneManager;
import fr.dwightstudio.dsengine.resources.ResourceManager;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class SurfaceRenderer extends Renderers {
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

    private final Surface[] surfaces;
    private final List<Texture> textures;

    private final int batchSize;
    private final Shader shader;
    private final float[] vertices;
    private final int[] textureSlots = {0, 1, 2, 3, 4, 5, 6, 7};
    private int numberOfSurfaces;
    private boolean hasRoom;
    private final int zIndex;

    private int vertexBufferObjectID;
    private int vertexArrayObjectID;

    /**
     * Create a new SurfaceRenderer
     * This renderer is going to be automatically created when adding Surface to your GameObjects
     *
     * @param batchSize the max number of Line the renderer can buffer
     * @param zIndex the Z level of the SurfaceRenderer
     */
    public SurfaceRenderer(int batchSize, int zIndex) {
        this.surfaces = new Surface[batchSize];
        this.textures = new ArrayList<>();

        this.batchSize = batchSize;
        this.zIndex = zIndex;
        m_zIndex = zIndex;
        ResourceManager.load("./src/main/resources/shaders/default.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/default.glsl");
        this.vertices = new float[batchSize * 4 * VERTEX_SIZE]; // The 4 is the number of vertices per quads
        this.numberOfSurfaces = 0;
        this.hasRoom = true;
    }

    /**
     * This method will allocate the new buffers for this renderer and upload the necessary values into the shader
     */
    public void start() {
        shader.bind();
        shader.uploadIntArray("uTextures", textureSlots);
        shader.uploadMat4f("uProjectionMatrix", SceneManager.getCurrentScene().getCamera().getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", SceneManager.getCurrentScene().getCamera().getViewMatrix());

        vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, (long) vertices.length * Float.BYTES, GL_STREAM_DRAW);

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

    /**
     * Add a Surface to the SurfaceRenderer
     *
     * @param surface a Surface
     */
    public void addSurface(Surface surface) {
        surfaces[numberOfSurfaces] = surface;

        loadVertexProperties(numberOfSurfaces);

        numberOfSurfaces++;
        if (numberOfSurfaces >= batchSize) {
            hasRoom = false;
        }
    }

    /**
     * This method is called every frame to update the Surfaces however the data new data will be buffered only if
     * a Surface is set to dirty
     */
    public void render() {
        boolean rebufferData = false;
        for (int i = 0; i < numberOfSurfaces; i++) {
            if (surfaces[i].isDirty() || surfaces[i].isGameObjectDirty()) {
                loadVertexProperties(i);
                surfaces[i].markClean();
                surfaces[i].markGameObjectClean();
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

        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vPos"));
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vColor"));

        glDrawElements(GL_TRIANGLES, numberOfSurfaces * 6, GL_UNSIGNED_INT, 0);

        glDisableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vPos"));
        glDisableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vColor"));
        glBindVertexArray(0);

        for (Texture texture : textures) {
            texture.unbind();
        }
        shader.unbind();
    }

    /**
     * Generate and fill the elements buffer to draw Quads correctly with two triangles
     *
     * @return the elements array
     */
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

    /**
     * This method will automatically generate the necessary vertices for the Surface at index
     *
     * @param index the index of the Surface
     */
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
                if (textures.get(i).equals(surface.getTexture())) {
                    textureID = i + 1;
                    break;
                }
            }
        }

        float x = -surface.getCenterPoint().x + surface.getTransform().scale.x + surface.gameObject.getTransform().scale.x;
        float y = -surface.getCenterPoint().y + surface.getTransform().scale.y + surface.gameObject.getTransform().scale.y;
        // This will loop 4 times for the 4 vertices.
        for (int i = 0; i < 4; i++) {
            if (i == 1) {
                y = -surface.getCenterPoint().y;
            } else if (i == 2) {
                x = -surface.getCenterPoint().x;
            } else if (i == 3) {
                y = -surface.getCenterPoint().y + surface.getTransform().scale.y + surface.gameObject.getTransform().scale.y;
            }

            // Load the position
            vertices[offset] = (x * (float) Math.cos(surface.getTransform().getRotation(Transform.RADIAN)) - y * (float) Math.sin(surface.getTransform().getRotation(Transform.RADIAN))) + surface.getCenterPoint().x + surface.getTransform().position.x + surface.gameObject.getTransform().position.x;
            vertices[offset + 1] = (x * (float) Math.sin(surface.getTransform().getRotation(Transform.RADIAN)) + y * (float) Math.cos(surface.getTransform().getRotation(Transform.RADIAN))) + surface.getCenterPoint().y + surface.getTransform().position.y + surface.gameObject.getTransform().position.y;

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

    /**
     * This method check if the renderer have room to put more Line
     *
     * @return if there is space remaining in this renderer
     */
    public boolean hasRoom() {
        return hasRoom;
    }

    /**
     * Get the current Z level of the SurfaceRenderer
     *
     * @return the current Z level of the SurfaceRenderer
     */
    public int getzIndex() {
        return zIndex;
    }

    @Override
    public int compareTo(@NotNull Renderers renderer) {
        return Integer.compare(this.zIndex, renderer.m_zIndex);
    }
}
