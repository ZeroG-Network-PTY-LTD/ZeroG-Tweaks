# Alien weather — experimental client effects

Added in `1.0.5-dev`. **Off by default**, independent of Iris/shaders. On the
title screen, use **ZeroG Weather** and choose Off, Low or High. Thunder audio
and extra sky flashes have separate controls; extra flashes are off by default.
These controls are not a guarantee of photosensitivity safety.

Effects are cosmetic and local to each player's surroundings. They do not
change server weather, terrain, block entities, health, crops or mob behaviour.
Funnels do not pull players, break blocks or implement tornado physics.

| Planet theme | Current prototype |
| --- | --- |
| Mars | Rust-coloured blowing dust, small dust devils / larger particle funnels |
| Skarn | Dark ash-coloured gusts and particle vortices |
| Cerulon | Spore winds, blue-green funnels, native-rendered cosmetic lightning and thunder |
| Eidolon | Snowflake flurries |
| Solvane | Electrical sparks, golden vortices, cosmetic lightning and thunder |
| Airless Moon / galaxy moons | No added atmosphere/weather |

Galaxy planet slots follow the existing ecology theme mapping. Events use
six-minute cycles with 90-second active windows, offset per dimension. Large
funnels occur on every third active cycle. Electrical events can occur every
30 seconds during an active window. The player must be outdoors and not
underwater; no added particles with Minecraft's Minimal particle setting.
Low permits at most four emitted particles/tick; High twelve; Decreased halves
that budget. One short-lived bolt per electrical event is client-only and skips
vanilla bolt fire, damage and loud sound behaviour. No server entities are spawned.

This is a particle-based weather prototype, not a verified photorealistic storm
system. The animated cloud shader is a separate ZIP. The new weather clock does
not drive the shader's `rainStrength`: shader rain response still follows native
weather uniforms. Dust particles/funnels and flakes work with shaders off.

Normal build and static asset checks passed; no client/GPU or runtime weather
test was launched. Menu placement, lightning appearance, particle density and
modpack rendering compatibility need in-game review before artistic approval.

## Installed graphics dependencies

The user approved installing the NeoForge 1.21.1 pair on 2026-10-04:
- Iris release file `iris-neoforge-1.8.12+mc1.21.1.jar` (Modrinth `t3ruzodq`).
- Its exact required Sodium version `sodium-neoforge-0.6.13+mc1.21.1.jar`
  (Modrinth `Pb3OXVqC`), not an arbitrary newer Sodium.

Publisher SHA512 hashes and installed SHA256 were verified. The Iris JAR labels
its internal mod version `1.8.12-snapshot+mc1.21.1-local`; this is the publisher's
byte-identical stable-listed file, not a locally modified build.

Iris's metadata declares `[1.21,1.21.1)`. An ordinary Maven range excludes
1.21.1, so that prompted an additional loader check. Installed FML 4.0.44's
`VersionSupportMatrix` explicitly grants 1.21.1 compatibility with Minecraft
1.21 / NeoForge 21.0.166 ranges. Verified from the actual loader bytecode.
No JAR metadata was patched or checks bypassed. This supports the dependency
selection but does not prove full modpack/GPU compatibility.

Shader activation remains `enableShaders=false` in `config/iris.properties`.
No installer GUI, driver modification, DLL injection or game launch was used.
All five pre-existing mod JARs stayed hash-identical during dependency install.

Iris SHA256: `3e3f94d2d5cdcb8145c4385d521974aa2d8669b2cc212351f70cf06488182e83`.
Sodium SHA256: `7acd7af2ef75ec883a6872c17494ead65e38025151eb08a1d60e36d34377f403`.

Restart CurseForge Java. To review the separate cloud shader, explicitly select
`ZeroG-Atmosphere-0.1.zip` through Iris's Shader Packs menu; start with Balanced.
For older systems, leave shaders and alien weather off. This is not the finished
pre-launch graphics recovery/pack-selection workflow described in the design brief.
