#type vertex
#version 130

attribute vec3 vPos;
attribute vec4 vColor;
attribute vec2 vTextureCoords;

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
#version 130

uniform sampler2D textureSampler;

in vec4 fColor;
in vec2 fTextureCoords;

out vec4 color;

void main() {
    color = fColor * texture2D(textureSampler, fTextureCoords);
}
