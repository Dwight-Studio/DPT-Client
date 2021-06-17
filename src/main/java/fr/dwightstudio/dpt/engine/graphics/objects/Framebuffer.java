/*
 * Copyright (c) 2020-2021 Dwight Studio's Team <support@dwight-studio.fr>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package fr.dwightstudio.dpt.engine.graphics.objects;

import fr.dwightstudio.dpt.engine.graphics.GLFWWindow;
import fr.dwightstudio.dpt.engine.graphics.utils.FramebufferManager;
import fr.dwightstudio.dpt.engine.logging.GameLogger;
import fr.dwightstudio.dpt.engine.resources.ResourceManager;

import java.text.MessageFormat;

import static org.lwjgl.opengl.GL11.GL_NEAREST;
import static org.lwjgl.opengl.GL30.*;

public class Framebuffer {

    private final int baseWidth;
    private final int baseHeight;
    private final int scaleX;
    private final int scaleY;
    private final int x;
    private final int y;

    private int frameBufferObjectID;
    private int textureID;
    private int renderBufferID;

    private int frambufferVertexArrayObjectID;
    private final Shader shader;

    public Framebuffer(int x, int y, int baseWidth, int baseHeight) {
        this.x = x;
        this.y = y;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        this.scaleX = baseWidth;
        this.scaleY = baseHeight;
        ResourceManager.load("./src/main/resources/shaders/framebuffer.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/framebuffer.glsl");
        init();
    }

    public Framebuffer(int x, int y, int baseWidth, int baseHeight, int scaleX, int scaleY) {
        this.x = x;
        this.y = y;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        this.scaleX = scaleX;
        this.scaleY = scaleY;
        ResourceManager.load("./src/main/resources/shaders/framebuffer.glsl", Shader.class);
        this.shader = ResourceManager.get("./src/main/resources/shaders/framebuffer.glsl");
        init();
    }

    private void init() {
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

    private void genVBO() {
        float renderX = x / GLFWWindow.getWidth() - 1.0f;
        float renderY = y / GLFWWindow.getHeight() - 1.0f;
        float renderWidth = scaleX / GLFWWindow.getWidth();
        float renderHeight = scaleY / GLFWWindow.getHeight();
        float[] vertices = {
                renderX,  renderHeight, 0.0f, 1.0f,
                renderX, renderY, 0.0f, 0.0f,
                renderWidth, renderY, 1.0f, 0.0f,

                renderX,  renderHeight, 0.0f, 1.0f,
                renderWidth, renderY, 1.0f, 0.0f,
                renderWidth,  renderHeight, 1.0f, 1.0f
        };
        /*float vertices[] = {
                -1.0f,  0.5f,  0.0f, 1.0f,
                -1.0f, -1.0f,  0.0f, 0.0f,
                0.5f, -1.0f,  1.0f, 0.0f,

                -1.0f,  0.5f,  0.0f, 1.0f,
                0.5f, -1.0f,  1.0f, 0.0f,
                0.5f,  0.5f,  1.0f, 1.0f
        };*/
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

    public void render() {
        shader.bind();
        glBindVertexArray(frambufferVertexArrayObjectID);
        glActiveTexture(GL_TEXTURE9);
        glBindTexture(GL_TEXTURE_2D, textureID);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glBindVertexArray(0);
        shader.unbind();
    }

    public int getBaseWidth() {
        return baseWidth;
    }

    public int getHeight() {
        return baseHeight;
    }

    public void bind() {
        glBindTexture(GL_TEXTURE_2D, 0);
        glBindFramebuffer(GL_FRAMEBUFFER, frameBufferObjectID);
        //glViewport(0, 0, width, height);
    }

    public void unbind() {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        //glViewport(0, 0, GLFWWindow.getWidth(), GLFWWindow.getHeight());
    }

    public void delete() {
        glDeleteFramebuffers(frameBufferObjectID);
        glDeleteTextures(textureID);
        glDeleteRenderbuffers(renderBufferID);
    }

    public int getFrameBufferObjectID() {
        return frameBufferObjectID;
    }

    public int getTextureID() {
        return textureID;
    }

    public int getRenderBufferID() {
        return renderBufferID;
    }
}
