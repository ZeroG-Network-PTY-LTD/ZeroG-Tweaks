# Dimension-metal manufacturing components

Original native32×32 artwork for21 planetary metals plus Copper, two parts per family: an eight-tooth machined cog and a thin, layered compressed plate. Transparent bores, balanced silhouettes, pale bevels and selective violet inlays follow approved C direction. Ordinary generated-item models use the same texture in inventory and dropped-item faces. Painted accents are not runtime emission.

![Native artwork, enlarged and inventory-size](manufacturing-preview.png)

The old shared planet palettes were a bug, not the approved material identity.
Each metal now takes its six principal non-inlay tones directly from its current
native ingot sprite. Copper takes its tones from vanilla's16px Copper ingot in
the local1.21.1 resource JAR; vanilla art is unchanged. Planet groups are metadata
only. `manifest.json` records palettes, source hashes and output/layer hashes.
All44 sprites have distinct bytes and are mirrored into the built-in visual
refresh layer. Run `validate.py --code <checkout>` for native size, alpha,
palette, uniqueness and byte-equality checks. This is not GPU/client approval.

Run `python3 docs/manufacturing-components/generate.py --code /absolute/path/to/1.21.x-checkout` from Design. This emits retained source PNGs plus runtime models, PNGs, English names and item tags. Run after older general-art batches so they cannot overwrite these components.

Copper is the explicit owner-approved Overworld exception; iron, gold, Nullifite
and gemstone families remain excluded. No tool tiers or gate costs change.
Copper uses the powered compressor only; no new bench or machine/press survival
crafting costs are invented. Compressor supports44 recipes across22 metals.

The native generator/validator is the documented local fallback while the
optional game-dev package CLI is unavailable. No paid provider job, GLB/PBR
package or Blender/GPU receipt is claimed. Canva is review-only, not a texture
source; source PNGs are the ones actually packaged in the game.

11 October follow-up: the owner continued after the proposed costs of two ingots per plate and four per cog. `recipes.py` now emits manual shaped crafting plus recipe-book unlocks for every family. This is initial bench fabrication, not a powered compressor. The original pending-cost note is superseded for these parts only; future machines and exact broader survival costs remain separate.

Four existing casing stages use two plates, one cog, two local dusts, the previous core and any of the purple/blue/teal Star Glass variants. Output remains two casings and the predecessor chain is preserved. Two empty grid spaces leave room for future designs, but currently must stay empty. No mining/tool tiers, armour upgrades, recipe outputs or existing items are removed.

Run `recipes.py --resources /absolute/path/to/1.21.x/src/main/resources` after older casing generators. Runtime and retained Design data must match. Step numbers refer to the existing mining ladder (profile level minus four), not new machine or gate tiers.
