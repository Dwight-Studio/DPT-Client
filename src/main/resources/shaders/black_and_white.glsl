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

uniform float uTime;
uniform sampler2D textureSampler;
uniform bool usingTexture;

in vec4 fColor;
in vec2 fTextureCoords;

out vec4 color;

void main() {
    if (usingTexture) {
        vec4 Color = texture2D(textureSampler, fTextureCoords);
        color = vec4(vec3(Color.r + Color.g + Color.b) / 3, Color.a);
    } else {
        color = vec4(vec3(fColor.r + fColor.g + fColor.b) / 3, 1);
    }
}
