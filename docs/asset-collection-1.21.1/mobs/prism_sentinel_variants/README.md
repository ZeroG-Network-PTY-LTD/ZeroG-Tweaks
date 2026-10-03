# Prism Sentinel variants

Rolled when the Sentinel spawns (owner's choice, 2026-10-03). All four use the one model
(`blockbench/mobs/prism_sentinel.bbmodel`); only the texture and glowmask change.

| Variant | Chance | Look | Stats |
| --- | --- | --- | --- |
| Cerulean | 60% | the original cyan crystals | 300 HP, 10 damage, 15 armor |
| Aurelion | 20% | gold crystals on the blue stone body | same |
| Nebulite | 15% | indigo crystals, dark violet body | same |
| **Radiant** (rare) | 5% | bright gold crystals, gold band, ivory plinth; bigger gold aura, white boss bar | **1.5x: 450 HP, 15 damage, 22.5 armor** |

The textures are recolours made by `make_sentinel_variants.py`. It sorts each texel into the design sheet's palette
groups (crystal, core, stone, gold band) and maps each group to the variant's colours, keeping the shading. They are
placeholders until there's hand-painted art: replace `prism_sentinel_<variant>.png` and `_glowmask.png` (same UV layout)
in `1.21.x` `assets/zerog_tweaks/textures/entity/`.

In game: `/summon zerog_tweaks:prism_sentinel ~ ~ ~ {Variant:3}` (0 Cerulean, 1 Aurelion, 2 Nebulite, 3 Radiant).
Code: `1.21.x` 406a4db6.
