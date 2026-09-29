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
| `main` | Placeholder line (empty). |
| `design/v1.2-assets` | Design v1.2 bundle: gear stats and abilities, six liquids, GeckoLib mob and armor models, wasteland tinting, spawn eggs, custom effects. Assets merged into `src/main/resources` (team edits kept); new Java stays in `docs/` until it is wired in. |

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