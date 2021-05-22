package fr.dwightstudio.dpt.engine.graphics.render;

import fr.dwightstudio.dpt.engine.logging.GameLogger;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;

import static org.lwjgl.opengl.GL15.*;

// VBO = Vertex Buffer Object
public class TexturedVBO {

    public static List<Integer> vboList = new ArrayList<>();

    private final int verticesID;
    private final int textureID;
    private final int indicesID;
    private final int[] indices;

    public TexturedVBO(float[] vertices, float[] textureCoords, int[] indices) {
        this.indices = indices;

        verticesID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, verticesID);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        textureID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, textureID);
        glBufferData(GL_ARRAY_BUFFER, textureCoords, GL_STATIC_DRAW);

        indicesID = glGenBuffers();
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indicesID);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW);

        vboList.add(verticesID);
        vboList.add(textureID);
        vboList.add(indicesID);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0); // Unbinding any array buffer at the end to make sure it is not modified after
        glBindBuffer(GL_ARRAY_BUFFER, 0); // Unbinding any array buffer at the end to make sure it is not modified after
        GameLogger.logger.log(Level.FINE, "Created a Textured VBO with id : {0}, {1}, {2}", new Object[] {verticesID, textureID, indicesID});
    }

    public void render() {
        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);

        glBindBuffer(GL_ARRAY_BUFFER, verticesID);
        glVertexPointer(2, GL_FLOAT, 0, 0);

        glBindBuffer(GL_ARRAY_BUFFER, textureID);
        glTexCoordPointer(2, GL_FLOAT, 0, 0);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indicesID);
        glDrawElements(GL_TRIANGLES, indices.length, GL_UNSIGNED_INT, 0);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
        glBindBuffer(GL_ARRAY_BUFFER, 0);

        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    }
}
