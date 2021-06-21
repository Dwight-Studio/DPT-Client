/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dsengine.graphics.objects;

import fr.dwightstudio.dsengine.graphics.GLFWWindow;
import fr.dwightstudio.dsengine.graphics.utils.FramebufferManager;
import fr.dwightstudio.dsengine.logging.GameLogger;
import fr.dwightstudio.dsengine.resources.ResourceManager;
import fr.dwightstudio.dsengine.scripting.Component;
import org.joml.Vector2f;

import java.text.MessageFormat;

import static org.lwjgl.opengl.GL11.GL_NEAREST;
import static org.lwjgl.opengl.GL30.*;

public class Framebuffer extends Component {

    private final int baseWidth;
    private final int baseHeight;
    private final float scaleX;
    private final float scaleY;
    private final float x;
    private final float y;

    private int frameBufferObjectID;
    private int textureID;
    private int renderBufferID;

    private int frambufferVertexArrayObjectID;
    private final Shader shader;

    /**
     * Create a new Frambuffer object
     *
     * @param x the X position
     * @param y the Y position
     * @param baseWidth the base width
     * @param baseHeight the base height
     */
    public Framebuffer(int x, int y, int baseWidth, int baseHeight) {
        this.x = x;
        this.y = y;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        this.scaleX = baseWidth;
        this.scaleY = baseHeight;
        ResourceManager.load("./src/main/resources/shaders/framebuffer.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/framebuffer.glsl");
        initFramebuffer();
    }

    /**
     * Create a new Framebuffer object
     *
     * @param x the X position
     * @param y the Y position
     * @param baseWidth the base width
     * @param baseHeight the base height
     * @param scaleX the X scaling
     * @param scaleY the Y scaling
     */
    public Framebuffer(float x, float y, int baseWidth, int baseHeight, float scaleX, float scaleY) {
        this.x = x;
        this.y = y;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        this.scaleX = scaleX;
        this.scaleY = scaleY;
        ResourceManager.load("./src/main/resources/shaders/framebuffer.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/framebuffer.glsl");
        initFramebuffer();
    }

    /**
     * Initialize the Framebuffer
     */
    private void initFramebuffer() {
        frameBufferObjectID = glGenFramebuffers();
        glBindFramebuffer(GL_FRAMEBUFFER, frameBufferObjectID);

        textureID = glGenTextures();
        glBindTexture(GL_TEXTURE_2D, textureID);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, baseWidth, baseHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, 0);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, textureID, 0);

        renderBufferID = glGenRenderbuffers();
        glBindRenderbuffer(GL_RENDERBUFFER, renderBufferID);
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT32, baseWidth, baseHeight);
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderBufferID);

        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
            GameLogger.getLogger("FrameBuffer").fatal(MessageFormat.format("FrameBuffer with id: {0} is incomplete.", frameBufferObjectID));
        }

        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        genVBO();
    }

    /**
     * Generate a Vertex Buffer Object for the Framebuffer to display the Texture
     */
    // TODO: The Framebuffer default size should be the window size
    private void genVBO() {
        float renderX = x / GLFWWindow.getWidth() - 1.0f;
        float renderY = y / GLFWWindow.getHeight() - 1.0f;
        float renderWidth = scaleX / GLFWWindow.getWidth() + renderX;
        float renderHeight = scaleY / GLFWWindow.getHeight() + renderY;
        float[] vertices = {
                renderX, renderHeight, 0.0f, 1.0f,
                renderX, renderY, 0.0f, 0.0f,
                renderWidth, renderY, 1.0f, 0.0f,

                renderX, renderHeight, 0.0f, 1.0f,
                renderWidth, renderY, 1.0f, 0.0f,
                renderWidth,  renderHeight, 1.0f, 1.0f
        };
        frambufferVertexArrayObjectID = glGenVertexArrays();
        glBindVertexArray(frambufferVertexArrayObjectID);

        int vertexBufferObjectID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObjectID);
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW);

        glVertexAttribPointer(0, 2, GL_FLOAT, false, 4 * Float.BYTES, 0);
        glEnableVertexAttribArray(0);

        glVertexAttribPointer(1, 2, GL_FLOAT, false, 4 * Float.BYTES, 2 * Float.BYTES);
        glEnableVertexAttribArray(1);

        shader.bind();
        shader.uploadInt("screenTexture", 9); // We are using the GL_TEXTURE9 because it is unused
        FramebufferManager.add(this);
    }

    /**
     * Render the Framebuffer Texture on the screen
     */
    public void render() {
        shader.bind();
        glBindVertexArray(frambufferVertexArrayObjectID);
        glActiveTexture(GL_TEXTURE9);
        glBindTexture(GL_TEXTURE_2D, textureID);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glBindVertexArray(0);
        shader.unbind();
    }

    /**
     * @return the base width
     */
    public int getBaseWidth() {
        return baseWidth;
    }

    /**
     * @return the base height
     */
    public int getHeight() {
        return baseHeight;
    }

    public Vector2f getPosition() {
        return new Vector2f(x, y);
    }

    /**
     * Bind the Framebuffer object
     */
    public void bind() {
        glBindTexture(GL_TEXTURE_2D, 0);
        glBindFramebuffer(GL_FRAMEBUFFER, frameBufferObjectID);
        glViewport(0, 0, baseWidth, baseHeight);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    }

    /**
     * Unbind the Framebuffer object
     */
    public void unbind() {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        glViewport(0, 0, GLFWWindow.getWidth(), GLFWWindow.getHeight());
    }

    /**
     * Delete the Framebuffer object and it's associated Texture and Render buffer
     */
    public void delete() {
        glDeleteFramebuffers(frameBufferObjectID);
        glDeleteTextures(textureID);
        glDeleteRenderbuffers(renderBufferID);
    }

    /**
     * @return the Framebuffer object ID
     */
    public int getFrameBufferObjectID() {
        return frameBufferObjectID;
    }

    /**
     * @return the Framebuffer Texture ID
     */
    public int getTextureID() {
        return textureID;
    }

    /**
     * @return the Framebuffer Render Buffer ID
     */
    public int getRenderBufferID() {
        return renderBufferID;
    }
}
