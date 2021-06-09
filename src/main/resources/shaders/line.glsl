#type vertex
#version 130

attribute vec3 vPos;
attribute vec4 vColor;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;

out vec4 fColor;

void main() {
    fColor = vColor;
    gl_Position = uProjectionMatrix * uViewMatrix * vec4(vPos, 1.0);
}

#type fragment
#version 130

in vec4 fColor;

out vec4 color;

void main() {
    color = fColor;
}
