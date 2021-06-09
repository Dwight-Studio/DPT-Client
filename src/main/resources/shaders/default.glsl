#type vertex
#version 130

attribute vec3 vPos;
attribute vec4 vColor;
attribute vec2 vTextureCoords;
attribute float vTextureID;

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
#version 130

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
