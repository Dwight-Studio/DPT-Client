#type vertex
#version 330 core

layout (location=0) in vec2 vPos;
layout (location=1) in vec2 vTexCoords;

out vec2 fTexCoords;

void main() {
    gl_Position = vec4(vPos.x, vPos.y, 0.0, 1.0);
    fTexCoords = vTexCoords;
}

#type fragment
#version 330 core

uniform sampler2D screenTexture;

in vec2 fTexCoords;

out vec4 color;

void main() {
    color = texture(screenTexture, fTexCoords);
}
