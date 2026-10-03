# ZeroG Realism — approved production direction

Status: specification and reference audit only; artwork and shaders are not
completed, GPU-tested or installed. Approved by the user on 2026-10-04:
**locally owned Optimum Realism for vanilla + original ZeroG overlay**.

Later prototype update: `ZeroG-Atmosphere-0.1.zip` and its validation JSON are
included alongside this brief. Twelve GLSL compile/link configurations passed;
the pack was installed locally with shaders disabled. The full PBR overlay and
realistic shader system described below remain unfinished and GPU-untested.
Original rendering source belongs on the code branch:
https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/1.21.x/tools/graphics/zero-g-atmosphere

## Ownership boundary

Optimum Realism R4.1.1 64x is a private reference/optional local base pack.
Do not commit its ZIP, extracted artwork, adapted textures or branding to any
repository branch. The creator prohibits redistribution without permission:
https://optimumrealism.com/faq

Audit of the provided ZIP:
- SHA256: `34034798ca2294562634cb8d7f3cc8f529f3492724e7f42ead16611f7d0351e2`
- 4,896 entries, including 4,392 PNGs.
- 1,439 `_n.png` normal maps and 1,439 `_s.png` specular maps.
- Sample stone colour/normal/specular images: 64×64 RGBA.
- Metadata declares pack_format 80 and several broad version-range fields.
  This declaration is not proof of Java 1.21.1 compatibility. Verify actual
  loading on 1.21.1 before marking the base pack supported.
- OptiFine-specific CTM/CEM assets are present; Iris alone does not prove those
  optional features work. Do not silently install OptiFine or incompatible mods.

The ZIP is not a canonical Game Development Studio package with a closed
receipt/hash roster. No canonical admission or distribution is asserted.
Existing filename and inspection do not waive the creator's restrictions.

## Target and visual language

Minecraft **Java 1.21.1 / NeoForge**, exact ZeroG CurseForge instance. No Bedrock
conversion, renderer injection, downloaded native DLLs or driver modifications.

Original ZeroG block surfaces: 64×64 colour maps with coordinated LabPBR normal,
roughness/specular and emission data. Preserve block readability, palette,
resource identity and existing registration/UV contracts. PBR materials must
read plausibly under neutral lighting, not bake permanent sunlit highlights into
every face. Tiling continuity matters more than random high-frequency noise.

Material groups: planetary stone/ore, sand/soil/farmland, wood/bark/leaves,
metals/machine casings, glass/crystal, liquid surfaces and organic hive/comb.
Maintain ore/mineral colour differences and crop-stage recognition.

Do not force all entity/item sheets into a square 64×64 canvas: preserve each
rig's aspect ratio and UV layout, scaling uniformly when justified. Keep
inventory silhouettes readable at actual GUI size. Inventory icons should not
be made photorealistic at the cost of identifying tools, ingredients or armour.

## Atmospheric shader target

Original Java-compatible shader work: atmospheric scattering, volumetric clouds,
distance fog/haze, weather lighting, water reflections and optional bloom.
Dust and storm visuals must respect each planet's atmosphere and environment.
Airless moons should not receive terrestrial rain clouds just because a global
shader preset is enabled. Weather state and planet-specific particles require
mod-side integration; a resource pack alone cannot implement those systems.

Lightning needs bounded exposure/bloom and a reduced-flash option. Visual storm
effects are not authorisation to introduce new damage or gameplay weather rules.
Normal/specular/emission support must be tested explicitly in the shader; simply
shipping `_n`/`_s` files does not prove they are used.

Do not advertise hardware ray tracing or DLSS. NVIDIA's official Minecraft RTX
integration is a Bedrock product, not a DLL drop-in for this Java client.
https://www.nvidia.com/en-us/geforce/news/minecraft-rtx-dlss-official-release/

## Optional profiles and startup safety

| Profile | Texture selection | Effects target |
| --- | --- | --- |
| Lightweight (default) | Existing ZeroG/vanilla art | Shaders off; bounded particles |
| Balanced Realism (opt-in) | Local Optimum 64x + original ZeroG 64x overlay | Reduced cloud samples/shadow distance; optional bloom |
| Advanced Realism (opt-in) | Same materials; no mandatory 256x/512x | Higher cloud/shadow quality; expensive reflections/POM optional |

These are unbenchmarked production targets, not hardware guarantees. The local
machine reports RTX 3050 Laptop GPU and Radeon 740M integrated graphics. VRAM,
power limits, active Minecraft GPU, thermals and frame-time results are not yet
verified. Do not force a GPU choice or assume the client uses the NVIDIA GPU.

Requirements for the future selector:
- Present the choice before world entry, with Lightweight selected by default.
- A genuinely pre-client-load recovery path must reset shader/resource-pack
  selection without loading their heavy assets. A title-screen selector alone
  cannot protect the earlier startup resource reload.
- Show missing/incompatible dependencies and disable unavailable profiles.
- No automatic downloads, native-library injection or driver modifications.
- Preserve unrelated packs, user settings and saved worlds.
- Back up changed graphics settings; provide one-step recovery to Lightweight.
- Persist explicit preferences, not automatic guesses about GPU model.
- Keep graphics client-only: dedicated servers must not load client classes.

## Production and acceptance gates

1. Validate a pinned Iris/Sodium NeoForge 1.21.1 dependency pair against the
   actual modpack. Neither was found installed during this audit.
2. Original material pilot: one stone/ore family, farmland, hive, metal and
   crystal, all with consistent colour/PBR maps and seam checks.
3. Implement original shader prototype and dimension-aware weather integration.
4. Implement profile selector plus pre-launch recovery before any default-on
   install. No world edits are required to switch graphics.
5. Compare the same scenes/time/weather across all three modes. Measure frame
   times, memory and visual artefacts; do not promise a fixed FPS beforehand.
6. Test foliage transparency, animated liquids, emissive bees, custom sky,
   machine/block entities, UI readability and shader-off fallback.
7. Expand the accepted pilot across the asset catalogue, then package previews,
   installation guide and checksums. Public commits remain approval-gated.

Code/integration belongs on `1.21.x`; original art, generators and editable
designs on `Design`; player guide, gallery and distribution checksums on `Docs`.
No edits or direct commits to `Released`.
