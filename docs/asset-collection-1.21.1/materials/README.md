# ZeroG Tweaks — Blockbench Material Production Set

Target: Minecraft Java 1.21.1, NeoForge, Java 21.

Open `blockbench/showcases/ZeroG_Tweaks_All_Materials_Showcase.bbmodel` first. Its Outliner is grouped by planet. Separate showcase tabs and all 94 block / 71 item source tabs are also included.

## Geometry rules

- Ores, storage blocks, and raw-storage blocks are full 16×16×16 Minecraft cubes with all six faces textured.
- Raw materials, ingots, nuggets, dusts, gems, crystals, fuels, and lore gems are transparent inventory sprites with only front/back faces.
- Authored emissive materials carry a separate emissive overlay in Blockbench.
- The original 16×16 source art is preserved exactly and enlarged to 64×64 with nearest-neighbour sampling. No blur, edge stretching, or palette substitution is used.

## Folder guide

- `blockbench/blocks/ores` — every ore cube
- `blockbench/blocks/storage_blocks` — processed material storage blocks
- `blockbench/blocks/raw_storage_blocks` — raw metal storage blocks
- `blockbench/items/*` — categorized inventory models
- `runtime_reference` — matching original Minecraft resource JSON/PNG files for integration reference
- `previews/materials_catalog.jpg` — visual catalog
- `validation_report.json` — face, embedding, and coverage checks

The original `ZeroG_Tweaks_full.zip` was not modified.
