# Gear showcase: armor and tools in 3D

There is one sheet per armor set (`01_nullifite.png` … `20_solvanite.png`), plus `00_all_sets.png` with every set on display.

Each sheet shows:
- the set's current GeckoLib armor model on an armor stand;
- the **recommended chunky shell**, front and back: layered pauldrons, a raised breastplate with a glowing core gem, bracers, a belt, knee plates, boot cuffs, and a crown, brow rim and crest on the helmet;
- the five tools as **3D extruded models**: handle about 1.4 px thick, head about 2.4 px, gems 3 px;
- written notes on how to model the armor and the tools.

The chunky shell is a direction for the Blockbench pass, not a finished model. Build the extra cubes on the matching GeckoLib armor bones.

Everything here is rendered from the real assets (GeckoLib armor geo, armor textures and glowmasks, 16×16 tool icons) by `generators/gear_showcase.py`, using `generators/render3d.py`. Re-run the generator after changing any of those assets.
