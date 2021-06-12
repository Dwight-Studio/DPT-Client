/*
 * Copyright (c) 2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;

import static org.lwjgl.opengl.GL11.GL_FLOAT;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class LineRenderer {
    // This is what the array should looks like:
    //
    // Position         Color
    // float, float,    float, float, float, float
    //
    // NOTE: Here I put only x and y for position bacause we are working with 2d only in this BatchRender
    private final int POSITION_SIZE = 2;
    private final int COLOR_SIZE = 4;
    private final int VERTEX_SIZE = POSITION_SIZE + COLOR_SIZE;

    // Here are the 'offsets' in the array for each differents data
    private final int POSITION_OFFSET = 0;
    private final int COLOR_OFFSET = (POSITION_OFFSET + POSITION_SIZE) * Float.BYTES;

    private final Line[] lines;
    private final int batchSize;
    private final Shader shader;
    private final float[] vertices;

    private int numberOfLines;
    private boolean hasRoom;
    private int vertexBufferObjectID;
    private int vertexArrayObjectID;

    /**
     * Create a new LineRenderer
     * This renderer is going to be automatically created when adding Line to your GameObjects
     *
     * @param batchSize the max number of Line the renderer can buffer
     */
    public LineRenderer(int batchSize) {
        this.lines = new Line[batchSize];

        this.batchSize = batchSize;
        ResourceManager.load("./src/main/resources/shaders/line.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/line.glsl");
        this.vertices = new float[batchSize * VERTEX_SIZE * 2]; // The 2 is the number of vertices per lines
        this.numberOfLines = 0;
        this.hasRoom = true;
    }

    /**
     * This method will allocate the new buffers for this renderer and upload the necessary values into the shader
     */
    public void start() {
        shader.uploadMat4f("uProjectionMatrix", SceneManager.getCurrentScene().getCamera().getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", SceneManager.getCurrentScene().getCamera().getViewMatrix());

        vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, (long) vertices.length * Float.BYTES, GL_DYNAMIC_DRAW);

        glVertexAttribPointer(glGetAttribLocation(shader.getProgramID(), "vPos"), POSITION_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, POSITION_OFFSET);
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vPos"));

        glVertexAttribPointer(glGetAttribLocation(shader.getProgramID(), "vColor"), COLOR_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, COLOR_OFFSET);
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vColor"));
    }

    /**
     * Add a line to the renderer
     *
     * @param line a Line
     */
    public void addLine(Line line) {
        lines[numberOfLines] = line;

        loadVertexProperties(numberOfLines);

        numberOfLines++;
        if (numberOfLines >= batchSize) {
            hasRoom = false;
        }
    }

    /**
     * This method is called every frame to update the Lines however the data new data will be buffered only if
     * a Line is set to dirty
     */
    public void render() {
        boolean rebufferData = false;
        for (int i = 0; i < numberOfLines; i++) {
            if (lines[i].isDirty() || lines[i].isGameObjectDirty()) {
                loadVertexProperties(i);
                lines[i].markClean();
                lines[i].markGameObjectClean();
                rebufferData = true;
            }
        }

        if (rebufferData) {
            glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices);
        }


        shader.bind();

        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vPos"));
        glEnableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vColor"));

        glDrawArrays(GL_LINES, 0, lines.length * 6 * 2);

        glDisableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vPos"));
        glDisableVertexAttribArray(glGetAttribLocation(shader.getProgramID(), "vColor"));
        glBindVertexArray(0);

        shader.unbind();
    }

    /**
     * This method will automatically generate the necessary vertices for the Line at index
     *
     * @param index the index of the Line
     */
    private void loadVertexProperties(int index) {
        Line line = this.lines[index];
        int offset = index * VERTEX_SIZE * 2;

        float x = line.getStartPosition().x;
        float y = line.getStartPosition().y;
        // This will loop 2 times for the 2 vertices.
        for (int i = 0; i < 2; i++) {
            if (i == 1) {
                x = line.getEndPosition().x;
                y = line.getEndPosition().y;
            }

            // Load the position
            vertices[offset] = x + line.getTransform().position.x + line.gameObject.getTransform().position.x;
            vertices[offset + 1] = y + line.getTransform().position.y + line.gameObject.getTransform().position.y;

            // Load the color
            vertices[offset + 2] = line.getColor().getRed();
            vertices[offset + 3] = line.getColor().getGreen();
            vertices[offset + 4] = line.getColor().getBlue();
            vertices[offset + 5] = line.getColor().getAlpha();

            // Load the thickness
            glLineWidth(line.getThickness());

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
}
