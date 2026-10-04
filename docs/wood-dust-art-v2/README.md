# Native wood, leaf and dust art — second implementation batch

Original deterministic 32×32 pixel artwork drawn by `generate.py`. This follows the approved A/C direction; it does not claim to reproduce every pixel of the AI concept sheets. No commercial resource-pack or Mojang texture bytes are copied.

## Coverage

- Existing Shardwood, Charwood, Hoarwood and Gildwood: longitudinal bark, separate square end grain, stripped-log side/end grain, board-seamed planks, cutout leaf clusters and sparse botanical highlight accents (24 block textures).
- All 17 existing `zerog_tweaks` dust PNGs: colored shaded heaps, clustered grains and restrained floating particles. Preserve each material palette rather than making all dust cyan/purple.
- Native botany generator separately redraws 24 harvested-vegetable icons, including the 18 older crops previously excluded from its icon output. Carrots/parsnips/radishes, bulbs, corn, leafy heads and aubergines have distinct silhouettes. Harvest palettes match their existing crop-stage palette. Twelve tree-fruit icons, seeds and gourd slices continue using the same native shading pass.

Models retain their existing registry IDs, UV conventions and inventory parents. Log inventory models inherit the placed-block model. Slabs/stairs/fences referencing the same plank texture inherit the new artwork automatically. This pass does not redraw doors/trapdoors/saplings or armor/tool atlases.

## Reproduction order

Run `planet_art_refresh.py`, then `docs/planet-botany-v2/generate.py`, then this generator against the separate `1.21.x` checkout. This generator is the last dust overlay. The source manifest records hashes and palettes, and static validators check both the old source layers and final runtime/JAR payloads; they do not silently discard historical-source validation.

## Review and evidence

`native-textures-preview.png` shows source textures, not GPU game renders. The botany folder also contains `vegetable-items.png`. Painted bright pixels are not a claim of emitted light or a new emissive layer. Leaf textures retain alpha cutouts and existing `cutout_mipped` model settings. No growth mechanics, recipes, worldgen, saves or light-level settings are changed by this artwork pass.

License: All Rights Reserved. These are original project-authored drawings; generated concepts remain visual references only.
