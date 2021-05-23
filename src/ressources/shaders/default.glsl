#type vertex
#version 330 core

layout (location=0) in vec3 vPos;
layout (location=1) in vec4 vColor;
layout (location=2) in vec2 vTextureCoords;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;

out vec4 fColor;
out vec2 fTextureCoords;

void main() {
    fColor = vColor;
    fTextureCoords = vTextureCoords;
    gl_Position = uProjectionMatrix * uViewMatrix * vec4(vPos, 1.0);
}

#type fragment
#version 330 core

uniform float uTime;
uniform sampler2D textureSampler;
uniform bool usingTexture;

in vec4 fColor;
in vec2 fTextureCoords;

out vec4 color;

void main() {
    if (usingTexture) {
        color = texture(textureSampler, fTextureCoords);
    } else {
        color = fColor;
    }
}
