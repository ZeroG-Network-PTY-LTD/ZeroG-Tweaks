# Moonsteel — chunky shell (3D) and trims

Implements `moonsteel_3d_design_sheet.png` (armor and tools in 3D) and
`moonsteel_trim_options_sheet.png` (trim patterns and materials).

| File | What it is |
| --- | --- |
| `moonsteel_chunky_shell.bbmodel` | Blockbench project of the GeckoLib armor: vanilla boxes + shell cubes on the armor bones |
| `moonsteel.geo.json`, `moonsteel.png`, `moonsteel_glowmask.png` | The exact files shipped on `1.21.x` (`geckolib/models/item/armor/`, `textures/item/armor/`) |
| `chunky_shell_front.png`, `chunky_shell_back.png` | Blockbench renders of the armor |
| `trim_preview_crater_solvanite_*.png` | Crater pattern in Solvanite on the shell, drawn the way `ZGGeoArmorRenderer` draws trims in game |
| `moonsteel_item_reference_sheet.webp` | 16x16 sprite reference. The held tools are 3D (Draconic style): see `docs/zero-g-tweaks-bundle/blockbench/tools/moonsteel/`. |
| `gen_armor.py` | Generates the geo model, texture and glowmask (edit cubes/palette here, then re-run) |

Shell cubes per piece: helmet (inflate 1.0) + crown ridge, crest, brow rim; chestplate (1.01) +
raised breastplate, glowing core gem, back plate, faulds, two stacked pauldrons and cuffs per arm;
leggings (0.5) + belt and knee plates; boots (1.0, ankle height) + flared cuff.

Trims: the trim draws on a vanilla-shaped box just above the base plates (inflate 1.05 / 0.55);
shell cubes sit on top of it. Moonsteel trim on Moonsteel armor uses the darker Moonsteel palette.

Regenerate the armor: `python gen_armor.py OUT_DIR`.
