package fr.dwightstudio.dpt.engine.graphics;

import java.util.ArrayList;
import java.util.List;

import static org.lwjgl.opengl.GL15.*;

// VBO = Vertex Buffer Object
public class TexturedVBO {

    public static List<Integer> vboList = new ArrayList<>();

    private final int vID;
    private final int tID;
    private final float[] vertices;

    public TexturedVBO(float[] vertices, float[] textureCoords) {
        this.vertices = vertices;

        vID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vID);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        tID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, tID);
        glBufferData(GL_ARRAY_BUFFER, textureCoords, GL_STATIC_DRAW);

        glBindBuffer(GL_ARRAY_BUFFER, 0); // Unbinding any array buffer at the end to make sure it is not modified after
    }

    public void render() {
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);

        glBindBuffer(GL_ARRAY_BUFFER, vID);
        glVertexPointer(2, GL_FLOAT, 0, 0);

        glBindBuffer(GL_ARRAY_BUFFER, tID);
        glTexCoordPointer(2, GL_FLOAT, 0, 0);

        glDrawArrays(GL_TRIANGLES, 0, vertices.length / 2);
        glBindBuffer(GL_ARRAY_BUFFER, 0);

        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    }
}
