# Moonsteel tools: 3D models (Draconic Evolution style)

Preview: `../../../sheets/gear/moonsteel_tools_3d.png`. Generator: `../../../generators/tools3d.py`.

| File | What it is |
| --- | --- |
| `models/item/moonsteel_{sword,pickaxe,axe,shovel,hoe}.json` | Java item models built from 17-22 cubes each (parent `minecraft:item/handheld`) |
| `textures/item/3d/moonsteel_tools.png` | Shared 64 x 64 texture with 12 material swatches: steel, edge, grip, cord, collar, plate, glow, gem, core, trim |

## Install (asset-only, goes on `1.21.x`)
1. Copy `models/item/*.json` over `src/main/resources/assets/zerog_tweaks/models/item/`. This replaces the flat sprite models.
2. Copy `textures/item/3d/moonsteel_tools.png` to `src/main/resources/assets/zerog_tweaks/textures/item/3d/`.
3. No Java is needed. Run `./gradlew build` and `runClient`, then check the tools in the inventory, in first and third person, and dropped on the ground.

## Notes
- Open any model in Blockbench with **File > Open Model**. Each one is a plain Java Block/Item model.
- Every cube is rotated -45 deg on Z around (8, 8, 8), so each tool sits on the same diagonal as the old sprite and the vanilla hand, GUI and ground poses still fit.
- Glowing cubes (the fuller, inlays, gems and moon cores) have `"neoforge_data": {"block_light": 15, "sky_light": 15}` and `"shade": false`, so they are full-bright in the dark. Blockbench can drop `neoforge_data` when it saves; add it back after editing.
- For a flat sprite in the inventory but 3D in hand, wrap the model with the `neoforge:separate_transforms` loader and give the `gui` perspective the old sprite model.
- Other tool sets can reuse these models: recolour the 64 x 64 texture and point `textures.0` at it.
