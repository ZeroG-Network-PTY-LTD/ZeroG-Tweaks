# Approved art direction — 2026-10-05

User-approved direction from the ZeroG art comparison sheet:

- Weapons, armor, ingots and dusts: C (Magitech Accents).
- Plants, grasses, crops and other vegetation: a mixture of A (Enhanced Vanilla) and C.
- Retain recognizable Minecraft silhouettes and consistent pixel density.
- Aim for 32×32 inventory sprites, with clustered shading, hue-shifted cool shadows and crisp highlights.
- Use selective cyan/lilac accents for equipment; adapt accents to each existing material palette rather than recoloring every material identically.
- Keep ordinary foliage naturally shaded; reserve glow accents for selected buds, flowers, fruit and luminous species.
- Crops need distinct bushy, slender and trailing silhouettes, with visible produce appearing through growth stages.
- Ground vines should visibly connect to roots and climb supported block faces.
- Dirt and both dry/wet farmland MUST NOT contain ores, gems, glowing mineral flecks or crystal deposits. Use natural matte soil, ordinary pebbles and organic matter. Wet farmland remains visibly darker, with readable furrows.
- User approved the leaves/wood art direction: recognizable bark, square log end-grain, stripped wood fibers, timber planks and cutout leaf clusters, with selected luminous botanical accents.
- Inventory block models must use the same textures as placed blocks. Fruit and vegetable buds should appear in growth stages; match harvested-item palettes to their visible crop produce.
- Texture-painted glow is not evidence of emissive rendering or emitted world light. Test each independently.

## Moonsteel facing correction

User clarified that tools should face the opposite direction, after initially requesting 360° on Z.
Superseded by the user's latest correction: restore original Z angles and apply
a 180° X-axis change only to first- and third-person hand display rotations:

| Context | Rotation XYZ |
| --- | --- |
| Third person, right | 180, -90, 55 |
| Third person, left | -180, 90, -55 |
| First person, right | 180, -90, 25 |
| First person, left | -180, 90, -25 |

Preserve translations, scales, cube elements, UVs, shared texture, armor, ground and item-frame transforms.
Both model copies and tools3d.py must preserve these settings on regeneration.

## Evidence boundary

The comparison sheet is an AI-generated concept preview, not an installed or dimension-validated texture atlas.
The original terrain sheet is superseded by planetary-terrain-soil-corrected-concept.png, which removes mineral-like accents from soil/farmland. Preserve the original as historical reference, not as the soil implementation target.
Art direction approval does not mean the runtime textures have been replaced.
Moonsteel hand-facing changes need visual play testing in both hands and perspectives.
