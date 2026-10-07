# Wasteland ruins — Prism Spire first implementation

This generator builds an original Concord ruin from the mod's existing
Prismstone/Chiseled Prismstone/Cracked Prismstone Bricks and Pulsar Lamps.
No textures or private reference artwork are copied. No new logs, characters,
hidden coordinates, factions or bosses are introduced.

`generate_prism_spire.py --resources <code checkout>/src/main/resources`
uses our existing Mars-template NBT writer. Regeneration emits both the live
resource data and matching `generated/` design copies. Run this independently
from texture generators. Existing Prism Spire loot is preserved unchanged.

## Layout

- Bounding size: 15 × 23 × 15 blocks, including explicit interior air.
- Foundation at y0, walkable floors y1/y7/y13.
- Three-block-wide north entrance at x6–8, y2–4.
- Continuous backed ladder at x7/z11, y1–15, with holes through the floors.
- One real chest at x7/y14/z7; its lid space is open.
- Four buttresses, broken wall windows and a fractured upper crown.
- Rotation is delegated to Minecraft's structure placement system.

## Placement contract

Crystal wasteland Prism Fields/Crystal Caverns only. The existing dry-land
jigsaw generator rejects wet or excessively uneven terrain; beard-box
adaptation blends the foundation. Initial spacing40/separation20 chunks,
search radius32, maximum terrain difference8. These are conservative starting
placement values, not a player-approved spawn-frequency balance.

This is the first implemented ruin, not a claim that all seven wasteland ruins
are complete. Lore text remains pending approval for this ruin. Headless
placement/reward checks are separate from natural-world sampling and the
owner's client visual review.
