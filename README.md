# ZeroG Tweaks

A NeoForge 1.21.1 content/companion mod for the ZeroG modpack — shattered-void
Nullifite progression, galaxy teleporters, planet ores, space woods, machine
blocks, and the food/economy layer that ties the ZeroG planet network's
economy together. Zero dependencies beyond NeoForge itself.

Mod version **1.0.0** · NeoForge **21.1.252** · Minecraft **1.21.1** · Java **21**

## Branches

| Branch | Contents |
| --- | --- |
| `1.21.1-update` | **Active line.** Full NeoForge source (src/), Gradle build wiring, working Gradle wrapper, crystal-cluster + crop fixes. Recommended. |
| `Released` | Release line. |
| `design/v1.2-assets` | Design v1.2 bundle: gear stats and abilities, six liquids, GeckoLib mob and armor models, wasteland tinting, spawn eggs, custom effects. Assets merged into `src/main/resources` (team edits kept); new Java stays in `docs/` until it is wired in. |
| `codex/hd-mob-assets-1.21.1` | Updated HD creature asset stack based on `design/v1.2-assets`: 69 creature looks, corrected eye layouts and rigs, Phantom-based Tidewraith, spawn eggs, drops, optional aura previews, gallery and local asset CLI. Asset work only; existing remote branches are unchanged. |

> **Building with an AI agent?** Start with [`AGENTS.md`](AGENTS.md): what exists, what data expects from Java, and the milestone checklist.

## Updated Blockbench assets

This branch contains **224 editable projects**: 28 ZeroG mob models, 41 Shattered Skies looks across 10 creatures, 38 spawn eggs, 65 drops and 52 optional creature/aura previews.

- [Download the complete Blockbench ZIP](docs/zero-g-tweaks-bundle/ZeroG_Mob_Blockbench_1.21.1.zip).
- [Current gallery](docs/zero-g-tweaks-bundle/blockbench/index.html): download/open the HTML locally to browse models, front/side eye reviews and animation previews. GitHub displays HTML source, not the interactive gallery.
- [Asset instructions and runtime limitations](docs/zero-g-tweaks-bundle/blockbench/README.md).
- [Recorded art requirements and input provenance](docs/zero-g-tweaks-bundle/blockbench/references/art_requirements.json).

Eye placements follow the repository's latest table. Single-eye creatures retain their bodies with one central, individually themed Eye-of-Ender-style eye. Bog Lurker, Gildcrab and Shardmother have articulated eyes above their heads. Tidewraith uses Minecraft 1.21.1 Phantom geometry and wing/tail hierarchy with original HD scale textures and manta gills. Only Prism Sentinel, Rift Tyrant, Eidolon Captain and The Dying Star use the 10.8-block guardian height; other bosses retain authored sizes.

Projects include embedded textures, discrete pixel-gradient material palettes, mirrored anatomy/joints, editable animation clips and separate emissive masks. Creature projects require the GeckoLib Blockbench plugin. Spawn eggs preserve vanilla runtime shell/spot layers and registered colours. Optional auras are render overlays, not emitted block light.

The [local asset CLI](docs/zero-g-tweaks-bundle/generators/zero_g_assets.py) runs without paid generation services. From the repository root (Python 3, Pillow and NumPy required):

```sh
python3 docs/zero-g-tweaks-bundle/generators/zero_g_assets.py doctor
python3 docs/zero-g-tweaks-bundle/generators/zero_g_assets.py validate
python3 docs/zero-g-tweaks-bundle/generators/zero_g_assets.py review --overwrite --zip
python3 docs/zero-g-tweaks-bundle/generators/zero_g_assets.py build --overwrite --zip
```

`list` shows creature/style ids; `open tidewraith` requests opening one project in an installed Blockbench. Generated output replacement requires `--overwrite`. This is a project wrapper, not Blockbench's native command API.

Static UV, hierarchy, symmetry, eye-placement/count, boss-scale and archive-integrity checks pass. Native Blockbench import/appearance and Minecraft entity rendering have **not** been verified. This asset branch does not implement the remaining entities, AI or runtime animation controllers. Obsolete creature exports were replaced on this branch; historical authored specifications and armour assets are preserved. Current exports use `assets/<namespace>/geo/`, `animations/` and `textures/entity/`; the pending renderer example has explicit matching paths.

**Build check, 1 October 2026:** the full Gradle build was attempted with Temurin Java 21. It is blocked by an inherited compile error in `registry/ZGFernBlock.java:21`: `SHAPE.move(state.getOffset(level, pos))` passes a `Vec3`, but Minecraft 1.21.1 requires three doubles. This asset branch does not alter that gameplay class. Consequently no successful new JAR or client test is claimed. The local asset validation is independent of this Java failure.

## What's in this mod

- **86 planet/terrain blocks, stone families, woods** — lunar/martian/abyssal stone sets, a glass and sand type for every planet (lunar, rust, crystal, frost, tide, dune, shimmer), the Nullifite family.
- **4 standing crystals/clusters** — Brine Crystal, Frost Crystal, Cerulite Cluster, Prism Cluster. Render as vanilla amethyst-cluster-style billboards and behave like real clusters: thin spike hitbox, place against any clicked face, pop when the support block is removed, sheared off by pistons (PushReaction.DESTROY).
- **2 crops** — Rust Tuber Crop (drops Rust Tuber / Baked Tuber) and Skyberry Bush (drops Skyberries), 4 growth stages each, bonemeal-able.
- **17 machine/functional blocks** — gate frames / controller / energy ports / lens housing / pad plate, alloy forge, combustion generator, fusion reactor + lamp, ore refinery, salvage station, crystal growth chamber, solar array, landing platform, cryo pod, spectral lantern.
- **65 food/util items** — 30+ dishes, planet materials, 5 smithing templates, galaxy gate keys, Heart of Solvane, Ration Pack, Neutralizer.
- **9+ gear sets** — astrium, cerulite, cyrrium, moonsteel, olympium, nullifite, radiante, salvium, skarnite, solvanite... full 9-piece kits (pick/shovel/axe/hoe/sword + 4 armor pieces).
- **38 creature designs** — 28 ZeroG mobs and 10 Shattered Skies creatures, with 69 editable visual looks and 38 spawn eggs. **These assets are not live entity implementations on this branch.** ZGInteractions.java documents planned shearing (Crystal Stag antlers, Frost Yak wool) and bottle-filling behaviors.

## Getting started

### Requirements

- Java 21 (Temurin recommended), on PATH or set via JAVA_HOME.

The mod has **zero required dependencies** — it is pure NeoForge. If you run
alongside GeckoLib-based mods, add the GeckoLib **4.9.3** jar for NeoForge
1.21.1 to the same mods/ folder. The build's flatDir repo points at `libs/`
(empty by default) for local jars if you ever vendor one.

### Build (developers)

    ./gradlew build          # Linux/macOS
    gradlew.bat build        # Windows

Output: build/libs/zerog-tweaks-1.21.1-1.0.0.jar

First build pulls NeoForge, NeoForm and Parchment, and recompiles vanilla
sources — expect 5–15 minutes. Incremental builds after that run ~15s
(--no-daemon on low-RAM machines).

### Install (players)

1. Copy the built jar (or download it from Releases) into your instance's mods/ folder.
2. Add the GeckoLib 4.9.3 jar for NeoForge 1.21.1 into the same mods/ folder.
3. Launch — the mod appears as "ZeroG Tweaks" with its own creative tab (zerog_tweaks).

## Project structure

    ZeroG_Tweaks/                (this repo)
    ├── src/main/java/net/zerog/tweaks/        Java source
    │   ├── registry/                           BlockInit / ItemInit / CreativeTabs / block classes
    │   └── event/                              ZGInteractions (shearing, bottles)
    ├── src/main/resources/                     assets + data + neoforge.mods.toml
    │   ├── assets/zerog_tweaks/                blockstates, models, textures, lang (878 blockstates)
    │   └── data/zerog_tweaks/                  loot tables, recipes, tags
    ├── docs/zero-g-tweaks-bundle/              preserved asset/design bundle (authority snapshot)
    │   ├── resources/                          original asset/data bundle
    │   ├── java/                               ZGFoodItems / ZGInteractions / ZGFoods reference
    │   ├── sheets/                             9.1MB art reference sheets (mobs, gear, blocks)
    │   ├── generators/                         the Python scripts that generated all art/JSON
    │   └── ZeroG_Tweaks_Design_Doc.md          full design document
    ├── gradle/ + gradlew(.bat)                 Gradle wrapper 8.x
    ├── build.gradle / settings.gradle / gradle.properties
    └── .gitignore                              build/ and IDE outputs excluded

## Credits

Jake M. and Co-Owner — ZeroG Network PTY LTD
