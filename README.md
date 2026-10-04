# ZeroG Tweaks

A NeoForge 1.21.1 content/companion mod for the ZeroG modpack — shattered-void
Nullifite progression, galaxy teleporters, planet ores, space woods, machine
blocks, and the food/economy layer that ties the ZeroG planet network's
economy together. Zero dependencies beyond NeoForge itself.

Mod version **1.0.0** · NeoForge **21.1.252** · Minecraft **1.21.1** · Java **21**

## Branches

| Branch | Contents |
| --- | --- |
| `Released` | Default branch. Release builds and this README. |
| `1.21.x` | **Active code line.** Full NeoForge source (src/) and Gradle build. |
| `Design` | All design and art work: texture previews, mob sheets, GUI layouts and the art-direction lock. |
| `Docs` | Guides, images and built JARs. |

## Art direction (required for every texture and model)

All ZeroG items, blocks and models must match the approved art references **to the T**. The full rules are in
[`docs/art-direction-lock.md` on the Design branch](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction-lock.md).

| Reference | What it sets |
| --- | --- |
| [Equipment art sheet](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction/zerog_equipment_art_reference.png) | The overall look: native 32x32 pixel art, dark-hue outlines (never pure black), hue-shifted shading, glowing violet/cyan accents only on meaningful parts, vegetation style. |
| [Gradients, depth and perspective](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction/zerog_gradients_depth_perspective.png) | The nine 6-tone material ramps, right/wrong shading techniques, 2D depth layers, viewing angle per asset type, 3D model depth. |
| [Block lighting GIF](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction/zerog_block_lighting.gif) | How blocks read under light: shadows step toward violet, never grey; glow inlays stay emissive. |
| [Floating items GIF](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction/zerog_floating_items.gif) | How dropped and held items read in 3D: 1 px extrusion, top-left light, darker edges, pulsing accents. |

![Block lighting](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/raw/Design/docs/art-direction/zerog_block_lighting.gif)

![Floating items](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/raw/Design/docs/art-direction/zerog_floating_items.gif)

Quick rules:
- **Ramps:** one hue-shifted ramp per material, using the exact hex values in [`style_kit.py`](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction/generator/style_kit.py). Never darken toward black.
- **Shading:** shade by stepping along the ramp. Use clustered bands with no dithering or pillow shading. The light comes from the top-left front.
- **Glow:** a dark rim, then the saturated tone, then a white core. Glow is never shaded by the light.
- **Galaxy-tinted blocks:** store a gray ramp; the tint adds the hue.
- **Viewing angle:**
  - items are drawn 3/4 oblique;
  - blocks are isometric on 2:1 pixel steps;
  - tools sit on the 45° diagonal, head top-right.
- **Model depth:** grip 1 px, blade 1.5 px, guard 2 px, inlays +0.25 px. Block icons use the GUI transform `[30, 225, 0]`.

## What's in this mod

- **86 planet/terrain blocks, stone families, woods** — lunar/martian/abyssal stone sets, a glass and sand type for every planet (lunar, rust, crystal, frost, tide, dune, shimmer), the Nullifite family.
- **4 standing crystals/clusters** — Brine Crystal, Frost Crystal, Cerulite Cluster, Prism Cluster. Render as vanilla amethyst-cluster-style billboards and behave like real clusters: thin spike hitbox, place against any clicked face, pop when the support block is removed, sheared off by pistons (PushReaction.DESTROY).
- **2 crops** — Rust Tuber Crop (drops Rust Tuber / Baked Tuber) and Skyberry Bush (drops Skyberries), 4 growth stages each, bonemeal-able.
- **17 machine/functional blocks** — gate frames / controller / energy ports / lens housing / pad plate, alloy forge, combustion generator, fusion reactor + lamp, ore refinery, salvage station, crystal growth chamber, solar array, landing platform, cryo pod, spectral lantern.
- **65 food/util items** — 30+ dishes, planet materials, 5 smithing templates, galaxy gate keys, Heart of Solvane, Ration Pack, Neutralizer.
- **9+ gear sets** — astrium, cerulite, cyrrium, moonsteel, olympium, nullifite, radiante, salvium, skarnite, solvanite... full 9-piece kits (pick/shovel/axe/hoe/sword + 4 armor pieces).
- **5 mobs** — Crystal Stag, Amethyst Stalker, Prismling, Rust Beetle, Dune Burrower — **loot/interaction data only for now; no live entity classes yet.** ZGInteractions.java documents the planned shearing (Crystal Stag antlers, Frost Yak wool) and bottle-filling behaviors.

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