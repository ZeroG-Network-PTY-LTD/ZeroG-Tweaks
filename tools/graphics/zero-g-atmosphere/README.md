# ZeroG Atmosphere 0.1 — experimental Iris shader pack

Original GLSL for Minecraft Java 1.21.1. No Optimum Realism artwork, third-party
shader code or NVIDIA DLLs are included. Copyright 2026 ZeroG Network PTY LTD;
distribution follows the project's existing permissions; no new third-party
licence is imposed or granted by this prototype.

Implements bounded ray-marched moving volumetric clouds, rain-dependent cloud
coverage/darkening and distance haze, restrained bloom and three quality presets.
Moon/galaxy-moon dimensions, Nether and End suppress atmosphere/clouds.
Uses Iris's generated/default geometry passes and composites their scene colour;
keeps the ZeroG panorama beneath clouds rather than replacing it.

Requires a compatible **Iris + Sodium NeoForge 1.21.1 pair**, not installed by this
build tool. Copy ZIP to `shaderpacks`, then select explicitly in Iris's settings.
Disabled by default. `LIGHTWEIGHT` also disables these extra shader effects.
No game is launched by packaging. GPU loading/visuals/performance still need
testing; syntax compilation alone is not evidence of Iris patcher compatibility.

Not yet implemented: LabPBR lighting/POM, hardware ray tracing/DLSS, physically
accurate multi-scattering, cloud shadows, water reflections, new dust particles,
lightning simulation or automatic pre-world/pre-launch profile chooser. Existing
game lightning remains existing game behaviour. No FPS promise is made.

Interface references: https://shaders.properties/current/reference/programs/composite/
and https://shaders.properties/current/reference/miscellaneous/dimension_properties/.
