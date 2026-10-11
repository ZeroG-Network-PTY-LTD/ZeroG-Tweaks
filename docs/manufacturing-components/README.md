# Dimension-metal manufacturing components

Original native 32×32 artwork for 21 metal families, two parts per family: an eight-tooth machined cog and a thin, layered compressed plate. Transparent cog bores, balanced silhouettes, pale bevels, hue-shifted shadows and selective violet cog inlays follow the approved C direction. These are ordinary generated-item models, so inventory and dropped-item faces use the same texture. Painted accents are not runtime light emission.

![Native artwork, enlarged and inventory-size](manufacturing-preview.png)

The generator uses the exact approved `art-direction/generator/style_kit.py` ramps. Moon/Eidolon use Moonsteel, Mars/Skarn copper, Cerulon Cerulite and Solvane Solvanite. Metals in a planetary group deliberately share its approved palette; no new palettes were invented. `manifest.json` records every ID, source planet and palette.

Run `python3 docs/manufacturing-components/generate.py --code /absolute/path/to/1.21.x-checkout` from Design. This emits retained source PNGs plus runtime models, PNGs, English names and item tags. Run after older general-art batches so they cannot overwrite these components.

Only existing dimension-origin ingot metals are eligible. Overworld Nullifite, iron, copper, gold and all gemstone families are excluded. These new parts do not change tool tiers or make gate progression cheaper.

11 October follow-up: the owner continued after the proposed costs of two ingots per plate and four per cog. `recipes.py` now emits manual shaped crafting plus recipe-book unlocks for every family. This is initial bench fabrication, not a powered compressor. The original pending-cost note is superseded for these parts only; future machines and exact broader survival costs remain separate.

Four existing casing stages use two plates, one cog, two local dusts, the previous core and any of the purple/blue/teal Star Glass variants. Output remains two casings and the predecessor chain is preserved. Two empty grid spaces leave room for future designs, but currently must stay empty. No mining/tool tiers, armour upgrades, recipe outputs or existing items are removed.

Run `recipes.py --resources /absolute/path/to/1.21.x/src/main/resources` after older casing generators. Runtime and retained Design data must match. Step numbers refer to the existing mining ladder (profile level minus four), not new machine or gate tiers.
