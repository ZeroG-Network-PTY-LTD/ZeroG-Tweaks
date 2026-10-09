# Planetary mines and cave ecology — 9 October 2026

The runtime implementation belongs to `1.21.x`; this note preserves the design
decisions for future art/layout work. No new texture placeholders are introduced.

## Original mine layouts

Use one 30-block spine and two to four staggered 10/15-block branches. Three-wide
passages have four blocks of clearance, fences with timber crossbeams, occasional
axis-correct rails and a chest. Planning uses only the supplied seed-local random.
Support spacing follows vanilla's readable segmented construction, not copied
vanilla templates. Minecraft 1.21.1 has no Nether mineshaft: charwood mines are
original hot-planet interpretations, not a claimed vanilla Nether structure.

| Planet theme | Existing local timber |
| --- | --- |
| Moon / Eidolon | Hoarwood |
| Mars / Skarn | Charwood |
| Cerulon | Shardwood |
| Solvane | Gildwood |

Galaxy slots retain their existing theme mapping. Existing ore generation and
tool progression remain authoritative; do not fill corridors with invented ores
or change rewards to bypass the storyline. Existing Buried Observatory chest
loot is retained, but a mine is not a completed dedicated observatory structure.

## Villages and vegetation

Keep rare region spacing, local wood doors, local wet farmland and native ground
edges. Reject unsuitable ravines and flooded terrain rather than building sky
platforms. Retain the hand-cut Aresite shrine in Rustborn settlements.

Cave vegetation uses approved A/C artwork: naturally shaded bodies and selective
glowing fruit/buds, no flat replacement sprites. Short supported wall-vine strands
stop at obstacles. Kelp uses only source water and always terminates in a head.
Existing planet-coloured dripstone, berries and mushrooms remain in use.

Prismlings are existing Cerulon cave inhabitants; covered high-altitude authored
caves may use them. Moon/Mars surface mobs must not become arbitrary cave mobs.
Missing creatures need their approved entity designs and behavior implemented
before new natural spawn entries can refer to them.

Natural placement and client visual approval are separate from these design
decisions. No player-world reset or new shared arrival-pad policy is implied.
