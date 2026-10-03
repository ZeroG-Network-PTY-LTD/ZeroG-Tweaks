# Optional ZeroG Realism for Java 1.21.1

**Status: experimental atmosphere ZIP installed; full realism remains incomplete.** The user approved a locally owned
Optimum Realism base pack for vanilla and an original ZeroG overlay on
2026-10-04. The third-party pack is not included in this repository.

Latest update: the user subsequently approved installing Iris 1.8.12 with its
required Sodium 0.6.13 NeoForge pair. Both are now installed, publisher hashes
verified, shaders still disabled. `1.0.5-dev` adds opt-in local alien-weather
particles/bolts and title-screen controls. See [weather details and verification
limits](alien-weather-1.21.1.md). The earlier no-loader choice below is historical.

The planned choices are Lightweight (default, shaders off), Balanced Realism
and Advanced Realism. Both realism modes are opt-in. A startup recovery path
must work before heavy resource loading; a menu shown only after startup is
not sufficient protection for older systems.

The supplied pack includes 64×64 materials with normal and specular maps.
The original ZeroG overlay will cover mod materials while preserving their
identities, UVs and animation layouts. Atmosphere/cloud/fog effects belong to
the shader; planetary dust/storm behaviour needs mod integration as well.

[Iris supports NeoForge 1.21.1](https://irisshaders.dev/), but an exact compatible
Iris/Sodium pair has not been selected or installed in this instance. Support
for OptiFine-specific connected textures or custom entity models is a separate
compatibility check, not implied by Iris support.

The local hardware reports an RTX 3050 Laptop GPU and Radeon 740M. No FPS or
maximum-quality claim has been verified. GPU memory and the active Minecraft
renderer still need checking during authorised client benchmarking.

NVIDIA's official [Minecraft RTX/DLSS integration](https://www.nvidia.com/en-us/geforce/news/minecraft-rtx-dlss-official-release/)
is for Bedrock. Copying NVIDIA DLLs will not enable it in this Java/NeoForge
modpack. No DLLs, drivers or renderer replacements are being installed.

[Optimum Realism's FAQ](https://optimumrealism.com/faq) prohibits redistribution
without permission. Its ZIP and artwork stay local; only original ZeroG assets
and integration code are eligible for publication.

No shader/resource-pack settings, installed JARs or existing saves were changed
during the initial audit. On 2026-10-04 the user then requested a shader build
and JAR installation, choosing **no Iris/Sodium installation**.

`ZeroG-Atmosphere-0.1.zip` is now in the instance's `shaderpacks/` directory,
inactive without a shader loader. Its twelve GLSL compile/link configurations
passed glslang 15.1.0 checks. It implements moving ray-marched clouds,
rain-dependent cloud/haze changes, restrained bloom and quality options,
with atmosphere suppressed on airless moons. It preserves the existing scene
and custom galaxy panorama. This is not GPU/Iris-runtime validation.

Shader SHA256: `fd0c25469c5fd11495f8e494e6afe4f6ac451c30ce0048e27f24a5f7d686729b`.

Original PBR artwork, reflections, new dust/lightning effects, automatic
selection and GPU testing remain outstanding. The Optimum ZIP was not copied,
modified or published. No DLLs, drivers or graphics dependencies were installed.

The normal `1.0.4-dev` mod build passed and replaced the installed `1.0.3-dev`,
which was moved to `zerog-mod-backups/20261003-200232-UTC`. GeckoLib, Productive
Bees and aeroapiary/Binnie remained hash-identical. Model/blockstate references
and effective layered texture payloads passed static checks; the normal JAR
contains no GameTest classes or test-only vanilla flat-preset override.

The separate world `ZeroG Planet Test Hub — Seed 0` uses **seed 0** and the
isolated hub's 68 tested outbound/return routes across 34 mod dimensions.
Normal mob spawning, weather/daylight and random ticks are restored in this
new copy, not in the source test world or any existing player save. The earlier
route test does not certify complete ecology: limited samples contained no
tree logs. New village layouts and additional concept structures are unfinished.

Fully close and reopen the CurseForge Java client to use the replaced JAR.
No client was launched. Branch-separated publication is performed only after
the user's subsequent approval; this installation is not a shipped release.
