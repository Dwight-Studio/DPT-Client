package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.primitives.Line;
import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.utils.SceneManager;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;

import static org.lwjgl.opengl.GL11.GL_FLOAT;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class LineBatchRenderer {
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

    private Line[] lines;

    private int batchSize;
    private Shader shader;
    private float[] vertices;
    private int numberOfLines;
    private boolean hasRoom;
    private int[] textureSlots = {0, 1, 2, 3, 4, 5, 6, 7};

    private int vertexBufferObjectID;
    private int vertexArrayObjectID;

    public LineBatchRenderer(int batchSize) {
        this.lines = new Line[batchSize];

        this.batchSize = batchSize;
        ResourceManager.load("./src/main/resources/shaders/line.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/line.glsl");
        this.vertices = new float[batchSize * VERTEX_SIZE * 2]; // The 2 is the number of vertices per lines
        this.numberOfLines = 0;
        this.hasRoom = true;
    }

    public void start() {
        shader.uploadMat4f("uProjectionMatrix", SceneManager.getCurrentScene().getCamera().getProjectionMatrix());
        shader.uploadMat4f("uViewMatrix", SceneManager.getCurrentScene().getCamera().getViewMatrix());

        vertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(vertexArrayObjectID);

        vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, (long) vertices.length * Float.BYTES, GL_DYNAMIC_DRAW);

        glVertexAttribPointer(0, POSITION_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, POSITION_OFFSET);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, COLOR_SIZE, GL_FLOAT, false, VERTEX_SIZE * Float.BYTES, COLOR_OFFSET);
        glEnableVertexAttribArray(1);
    }

    public void addLine(Line line) {
        lines[numberOfLines] = line;

        loadVertexProperties(numberOfLines);

        numberOfLines++;
        if (numberOfLines >= batchSize) {
            hasRoom = false;
        }
    }

    public void render() {
        boolean rebufferData = false;
        for (int i = 0; i < numberOfLines; i++) {
            if (lines[i].isDirty()) {
                loadVertexProperties(i);
                lines[i].markClean();
                rebufferData = true;
            }
        }

        if (rebufferData) {
            glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices);
        }


        shader.bind();

        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(0);
        glEnableVertexAttribArray(1);

        glDrawArrays(GL_LINES, 0, lines.length * 6 * 2);

        glDisableVertexAttribArray(0);
        glDisableVertexAttribArray(1);
        glBindVertexArray(0);

        shader.unbind();
    }

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
            vertices[offset] = x;
            vertices[offset + 1] = y;

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

    public boolean hasRoom() {
        return hasRoom;
    }
}
