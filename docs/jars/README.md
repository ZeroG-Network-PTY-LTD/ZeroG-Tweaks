# Development candidate — not a shipped release

## Current: zerog-tweaks-1.21.1-1.0.5-dev.jar

See [test hub and gameplay update](../planet-test-hub-1.21.1.md),
[cosmetic weather](../alien-weather-1.21.1.md) and
[optional realism](../optional-realism-1.21.1.md). Includes earlier inventory,
planet-art/mineral/crop and occupied-hive threading fixes, plus food/recipe
repairs, Liquids tab, 10-block layered impacts, planet sky, cave ecology, hub
routes and opt-in client weather. Normal build and static asset checks passed.
The earlier isolated hub run checked 34 destinations / 68 routes; it does not
validate all current gameplay, trees or client rendering. No client was launched
for this candidate. Shader ZIP is separate and requires Iris/Sodium; neither
third-party graphics mod is embedded in the Tweaks JAR. Defaults remain lightweight.

## Historical: zerog-tweaks-1.21.1-1.0.3-dev.jar

See [planet artwork, seeds and minerals](../planet-art-and-minerals-1.21.1.md).
Adds six four-stage grain crops, plantable Solflower/Rust Tuber seeds, six tall
blossoms, redesigned soil/grass, twelve mineral families, scarce cosmic Blazes,
and built-in inventory texture repairs for the separate Binnie companion.
Normal build and packaged static checks only: no server tests or client launch
for this candidate. Historical test results below do not validate 1.0.3-dev.
The 1.0.2 hive-threading fix remains. Restart the Java CurseForge client after
installation; new ores/plant placement require newly generated chunks.

## Historical threading hotfix: zerog-tweaks-1.21.1-1.0.2-dev.jar

Fixes the Cerulon occupied-hive worldgen threading crash. See the
[cause, regression evidence and limits](../cerulon-threading-hotfix-1.21.1.md).
All 53 isolated server GameTests passed, including worker-thread hive population
and custom-bee release data. The normal candidate excludes test classes.
The 1.0.1-dev JAR below is historical and has this known crash.

Includes the latest Cerulon/Mossback/Prism Sentinel work plus budding crystals,
updated metal/crystal artwork, all 34 dimension farming/sand families,
dimensional fluids/pools, gas vents, damaging daily impacts, twelve half-size
bee/hive/honey families and six cosmic Blaze types with eighteen palettes.
Requirements: Minecraft Java 1.21.1, Java 21, NeoForge 21.1.150+ (built against
21.1.252), GeckoLib 4.9.3 for NeoForge 1.21.1.

See the [illustrated update and installation guide](../crystal-material-update-1.21.1.md)
and [build evidence](../crystal-material-build-evidence.json). Normal build/static
asset validation passed; 52 isolated server GameTests passed. All 6,408 model
and 1,166 blockstate reference sets resolve, including generated trim sprites.
No in-game/modpack approval is claimed. SHA256SUMS.txt covers the archived and current jars.
Keep only ONE Tweaks candidate installed, since all have the same mod ID.
Older jars below are retained unchanged. User-directed local installation backs
up conflicting Tweaks jars outside mods; it does not remove unrelated mods.

## Historical multiblock candidate

The new `zerog-tweaks-1.21.1-1.0.0-multiblock-dev.jar` includes the G-key guide,
the consolidated upstream runtime and the fern offset compatibility correction.
It requires Java 21, NeoForge (built against 21.1.252) and GeckoLib 4.9.3 for
NeoForge 1.21.1. Normal build passed; optional test classes are excluded.

Both older jars were retained unchanged, including the separate Binnie
expansion jar. The historical checksum file covered all three files. Do not install multiple Tweaks
versions at once: they share a mod ID. This publication installs neither.

The new candidate is not validated in the ZeroG CurseForge modpack. Preserve
mods/configs/worlds and back up saves before user-directed tests. No official
release is created; Released is unchanged. HD worn-armour mapping, Productive
Bees/machine gameplay and several mob features remain unfinished.
