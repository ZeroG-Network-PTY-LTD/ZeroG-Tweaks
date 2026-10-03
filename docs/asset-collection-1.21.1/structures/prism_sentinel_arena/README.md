# Prism Sentinel arena: "Keeper's Proving Hall" (Cerulon, Galaxy 2)

This is the first guardian boss arena. It's a Concord test chamber in Cerulon's Quiet Mines: "a test, not a hunt".
Version 3 is the brief's layout (`docs/zero-g-tweaks-bundle/briefs/prism_sentinel_arena.md`) scaled about 1.5x, because
the 47-block v2 looked small next to the 10.8-tall Sentinel in game (owner feedback 2026-10-03). It is 67 x 40 x 67.
That is over the brief's 48-block structure-block limit; world generation and `/place` don't need that limit, but it
can't be loaded into a structure block. `generators/check_arena_palette.py <nbt> --max 72 --radius 22 --headroom 24`
prints **OK** (v1 failed 15 checks).

| File | What it is |
| --- | --- |
| `prism_sentinel_arena.nbt` | Structure template v3, 67 x 40 x 67 (same file on `1.21.x` in `data/zerog_tweaks/structure/`) |
| `build_prism_arena_v3.py` | The design: `python build_prism_arena_v3.py out.nbt` writes the template directly |
| `prism_arena_v3_preview.png` | Top view and south elevation, made by `render_arena_preview.py <nbt> <png>` |
| `*_v2_47*` | v2, the same layout at 47 x 32 x 47 |
| `*_v1*` | The first build, kept for reference (see `sheets/structures/prism_sentinel_arena_v1/`) |

## Layout (v3; radius from the centre; the fight floor is template y 3)

- **Dais r0-4:** two steps of polished black and polished cerulean, crystal-glass inlay, lamp studs. The **Concord Prism**
  sits at the centre (template 33, 6, 33).
- **Fight floor r5-22 (about 45 across):** flat polished cerulean with a smooth trim ring at r14 and 8 radial pulsar-lamp
  lines set flush. The Sentinel fights on this floor.
- **4 refractor pylons** at the diagonals (13, 13): 3 x 3, 8 tall, crystal-glass core with spectral lanterns, cluster cap.
  They are the only things on the floor and serve as beam cover.
- **Tiered stands r23-27:** 4 steps with lit risers, an old rail line on the top step and 3 parked minecarts.
- **Outer wall r27.4-29.6, 13 tall:** cracked bricks at the base, two chiseled bands, crystal-vein slits and half-cut
  geode shell. Buttresses every 45 degrees out to r32.5 with cluster crowns and azure moss.
- **Entrance (south):** 7 wide x 9 tall stone arch, pulsar-lamp pillars, a lit keystone (the Concord mark), and a walkway
  with a crystal-sand apron and starbloom.
- **Dome:** 8 single-block ribs rising from the buttresses to a ring at y 37, holding a crystal and shimmer glass
  oculus lit by a pulsar lamp. Nothing over the floor below floor + 24.

Palette: Cerulon blocks only. There are no ores, storage blocks, gate or machine parts, vanilla amethyst, sea lanterns or Prismstone.

## In the game (`1.21.x`, 8e4b59f9)

- One arena per world (`concentric_rings`, count 1), placed 200-500 blocks from (0, 0) in azure_plains or shardwood_grove.
  Find it with `/locate structure zerog_tweaks:prism_sentinel_arena` (or the tag `#zerog_tweaks:boss_arenas`).
- Structure type `zerog_tweaks:dry_land_jigsaw`: it prefers dry, level ground (max 6), searching up to 48 blocks around
  the placement. With `always_place` it falls back to the best site it found, so every world gets its arena. It uses a
  `beard_box` foundation and blocks monster spawns inside.
- The boss and the Concord Prism read the arena through `arena/PrismArena.java`; change it together with the template.
- Blocks: `concord_prism` (state idle, active or defeated) and `prism_barrier` (entrance seal). Both are unbreakable with no drops.
- The fight is wired (047a7171, 8e4b59f9): right-click the prism to start; the entrance seals; the Sentinel forms on the
  floor and glides on it, so melee reaches it. If the arena is empty for 10 s it resets. Victory opens the barrier and lights
  the oculus. A Sentinel Prism re-arms it for a rematch, which drops no gate key (owner's decision, 2026-10-02).
- `/place template zerog_tweaks:prism_sentinel_arena <x> <y> <z>` puts the template's bottom at y, so the fight floor
  lands at y + 3. The arena is 67 x 67.
