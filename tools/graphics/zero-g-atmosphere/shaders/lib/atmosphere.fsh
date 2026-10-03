#include "/lib/options.glsl"
uniform sampler2D colortex0;
uniform sampler2D depthtex0;
uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferModelViewInverse;
uniform vec3 cameraPosition;
uniform vec3 fogColor;
uniform vec3 sunPosition;
uniform float frameTimeCounter;
uniform float rainStrength;
uniform float viewWidth;
uniform float viewHeight;
uniform ivec2 eyeBrightnessSmooth;
uniform int isEyeInWater;
in vec2 texcoord;
/* RENDERTARGETS: 0 */
layout(location = 0) out vec4 fragColor;

float hash31(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
}
float zgNoise(vec3 p) {
    vec3 i = floor(p), f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(mix(hash31(i), hash31(i + vec3(1,0,0)), f.x),
                   mix(hash31(i + vec3(0,1,0)), hash31(i + vec3(1,1,0)), f.x), f.y),
               mix(mix(hash31(i + vec3(0,0,1)), hash31(i + vec3(1,0,1)), f.x),
                   mix(hash31(i + vec3(0,1,1)), hash31(i + vec3(1,1,1)), f.x), f.y), f.z);
}
float cloudDensity(vec3 p) {
    float heightMask = smoothstep(0.0, 9.0, p.y - CLOUD_HEIGHT)
                    * (1.0 - smoothstep(22.0, 36.0, p.y - CLOUD_HEIGHT));
    vec3 q = (p + vec3(frameTimeCounter * 1.6, 0.0, frameTimeCounter * 0.4)) * 0.012;
    float shape = zgNoise(q) * 0.62 + zgNoise(q * 2.03) * 0.26 + zgNoise(q * 4.07) * 0.12;
    return max(shape - (1.0 - CLOUD_COVERAGE - rainStrength * 0.14), 0.0) * heightMask;
}
vec3 addClouds(vec3 colour, vec3 ray, float maximumDistance) {
#if CLOUDS_ENABLED == 1 && ZG_ATMOSPHERE == 1
    if (abs(ray.y) < 0.015 || isEyeInWater != 0) return colour;
    float a = (CLOUD_HEIGHT - cameraPosition.y) / ray.y;
    float b = (CLOUD_HEIGHT + 36.0 - cameraPosition.y) / ray.y;
    float begin = max(min(a,b), 0.0);
    float end = min(max(a,b), min(maximumDistance, 6000.0));
    if (end <= begin) return colour;
    float stride = (end - begin) / float(CLOUD_STEPS);
    float transmittance = 1.0;
    vec3 scattering = vec3(0.0);
    vec3 sunDirection = normalize(mat3(gbufferModelViewInverse) * sunPosition);
    float daylight = smoothstep(-0.12, 0.25, sunDirection.y);
    vec3 lightColour = mix(vec3(0.10,0.14,0.22), vec3(0.91,0.94,1.0), daylight);
    lightColour *= 1.0 - rainStrength * 0.48;
    for (int i = 0; i < CLOUD_STEPS; ++i) {
        vec3 position = cameraPosition + ray * (begin + (float(i) + 0.5) * stride);
        float density = cloudDensity(position);
        float opacity = 1.0 - exp(-density * stride * 0.10);
        float topLight = mix(0.50, 1.0, clamp((position.y - CLOUD_HEIGHT) / 36.0, 0.0, 1.0));
        scattering += transmittance * opacity * lightColour * topLight;
        transmittance *= 1.0 - opacity;
        if (transmittance < 0.025) break;
    }
    return colour * transmittance + scattering;
#else
    return colour;
#endif
}
void main() {
    vec4 scene = texture(colortex0, texcoord);
    float depth = texture(depthtex0, texcoord).r;
    vec4 view = gbufferProjectionInverse * vec4(texcoord * 2.0 - 1.0, depth * 2.0 - 1.0, 1.0);
    vec3 viewPosition = view.xyz / max(abs(view.w), 0.000001) * sign(view.w);
    vec3 ray = normalize(mat3(gbufferModelViewInverse) * viewPosition);
    bool sky = depth >= 0.999999;
    float distanceToScene = sky ? 6000.0 : length(viewPosition);
    vec3 colour = scene.rgb;
#if ZG_ATMOSPHERE == 1
    // Preserve the mod's galaxy panorama rather than painting a new opaque sky.
    if (!sky && depth > 0.56 && isEyeInWater == 0) {
        float outdoor = float(eyeBrightnessSmooth.y) / 240.0;
        float fog = 1.0 - exp(-distanceToScene * FOG_DENSITY * (1.0 + rainStrength * 1.8));
        colour = mix(colour, fogColor, clamp(fog * outdoor, 0.0, 0.85));
    }
#endif
    // A cloud slab naturally occludes only geometry farther away than itself.
    if (sky || depth > 0.56) colour = addClouds(colour, ray, distanceToScene);
    if (BLOOM_STRENGTH > 0.0) {
        vec2 pixel = 1.0 / vec2(viewWidth, viewHeight);
        vec3 glow = vec3(0.0);
        for (int x=-1; x<=1; ++x) for (int y=-1; y<=1; ++y) {
            vec3 sampleColour = texture(colortex0, texcoord + vec2(x,y) * pixel * 3.0).rgb;
            glow += max(sampleColour - vec3(0.80), vec3(0.0));
        }
        colour += glow * (BLOOM_STRENGTH / 9.0);
    }
#if REDUCED_FLASH == 1
    // Bound added bloom; this is not a guarantee of photosensitivity safety.
    colour = min(colour, vec3(1.0));
#endif
    fragColor = vec4(max(colour, vec3(0.0)), scene.a);
}
