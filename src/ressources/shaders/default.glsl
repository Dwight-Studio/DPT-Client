#type vertex
#version 330 core

layout (location=0) in vec3 vPos;
layout (location=1) in vec4 vColor;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;

out vec4 fColor;

void main() {
    fColor = vColor;
    gl_Position = uProjectionMatrix * uViewMatrix * vec4(vPos, 1.0);
}

#type fragment
#version 330 core

in vec4 fColor;

out vec4 color;

void main() {
    color = fColor;
}
