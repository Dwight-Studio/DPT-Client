#type vertex
#version 330 core

layout (location=0) in vec3 vPos;
layout (location=1) in vec4 vColor;
layout (location=2) in vec2 vTextureCoords;
layout (location=3) in float vTextureID;

uniform mat4 uProjectionMatrix;
uniform mat4 uViewMatrix;

out vec4 fColor;
out vec2 fTextureCoords;
out float fTextureID;

void main() {
    fColor = vColor;
    fTextureCoords = vTextureCoords;
    fTextureID = vTextureID;
    gl_Position = uProjectionMatrix * uViewMatrix * vec4(vPos, 1.0);
}

#type fragment
#version 330 core

uniform sampler2D uTextures[8];

in vec4 fColor;
in vec2 fTextureCoords;
in float fTextureID;

out vec4 color;

void main() {
    if (fTextureID > 0) {
        int id = int(fTextureID);
        color = fColor * texture(uTextures[id], fTextureCoords);
    } else {
        color = fColor;
    }
}
