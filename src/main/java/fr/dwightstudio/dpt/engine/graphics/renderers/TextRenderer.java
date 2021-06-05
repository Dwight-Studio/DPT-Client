package fr.dwightstudio.dpt.engine.graphics.renderers;

import fr.dwightstudio.dpt.engine.graphics.objects.FontAtlas;
import fr.dwightstudio.dpt.engine.graphics.objects.Shader;
import fr.dwightstudio.dpt.engine.graphics.objects.Texture;
import fr.dwightstudio.dpt.engine.graphics.objects.Transform;
import fr.dwightstudio.dpt.engine.graphics.primitives.Surface;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;
import org.joml.Vector2f;

import static org.lwjgl.opengl.GL11.GL_FLOAT;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL15.GL_STATIC_DRAW;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL20.glDisableVertexAttribArray;
import static org.lwjgl.opengl.GL30.glBindVertexArray;
import static org.lwjgl.opengl.GL30.glGenVertexArrays;

public class TextRenderer {
    // This TextRenderer will take an Array of char and create vertices to render it
    // The vertices array will look like this :
    // Position         Color                   TextureCoords
    // float, float,    float, float, float,    float, float
    private final int POSITION_SIZE = 2;
    private final int COLOR_SIZE = 3;
    private final int TEXTURE_COORDS_SIZE = 2;
    private final int VERTEX_SIZE = POSITION_SIZE + COLOR_SIZE + TEXTURE_COORDS_SIZE;

    private final int POSITION_OFFSET = 0;
    private final int COLOR_OFFSET = POSITION_OFFSET + POSITION_SIZE * Float.BYTES;
    private final int TEXTURE_COORDS_OFFSET = COLOR_OFFSET + COLOR_SIZE * Float.BYTES;

    private final FontAtlas fontAtlas;
    private final char[] characters;
    private final Shader shader;
    private final float[] vertices;
    private final Vector2f position;

    private int vertexArrayObjectID;
    private int vertexBufferObjectID;

    public TextRenderer(FontAtlas fontAtlas, char[] characters, Vector2f position) {
        this.fontAtlas = fontAtlas;
        this.characters = characters;
        ResourceManager.load("./src/main/resources/shaders/default.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/default.glsl");
        this.vertices = new float[this.characters.length * 4 * VERTEX_SIZE];
        this.position = position;
    }

    public void init() {
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

        for (int i = 0; i < this.characters.length; i++) {
            loadVertexProperties(i);
        }
    }

    public void render() {
        GameLogger.getLogger("TextRender").debug("LOOP");
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices);

        shader.bind();

        glBindVertexArray(vertexArrayObjectID);
        glEnableVertexAttribArray(0);
        glEnableVertexAttribArray(1);

        glDrawElements(GL_TRIANGLES, this.characters.length * 6, GL_UNSIGNED_INT, 0);

        glDisableVertexAttribArray(0);
        glDisableVertexAttribArray(1);
        glBindVertexArray(0);

        shader.unbind();
    }

    private void loadVertexProperties(int index) {
        char character = this.characters[index];
        int offset = index * 4 * VERTEX_SIZE;

        float x = this.position.x + this.fontAtlas.getGlyph(character).getWidth();
        float y = this.position.y +  this.fontAtlas.getGlyph(character).getHeight();
        // This will loop 4 times for the 4 vertices.
        for (int i = 0; i < 4; i++) {
            if (i == 1) {
                y = this.position.y;
            } else if (i == 2) {
                x = this.position.x;
            } else if (i == 3) {
                y = this.position.y+ this.fontAtlas.getGlyph(character).getHeight();
            }

            // Load the position
            vertices[offset] = x;
            vertices[offset + 1] = y;

            // Load the color
            vertices[offset + 2] = 1.0f;
            vertices[offset + 3] = 1.0f;
            vertices[offset + 4] = 1.0f;
            vertices[offset + 5] = 1.0f;


            // Load the texture coordinates
            vertices[offset + 6] = this.fontAtlas.getGlyph(character).getTextureCoords(this.fontAtlas)[i].x;
            vertices[offset + 7] = this.fontAtlas.getGlyph(character).getTextureCoords(this.fontAtlas)[i].y;


            offset += VERTEX_SIZE;
        }
    }

    private int[] generateIndices() {
        // The indices array will look like this :
        //
        // int, int, int, int, int, int, <- 1 quad
        // int, int, int, int, int, int  <- 1 quad
        //
        // NOTE: We have 2 triangles with 3 indices each to form a quad so 3*2=6
        int[] elements = new int[6 * this.characters.length];
        for (int i = 0; i < this.characters.length; i++) {
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