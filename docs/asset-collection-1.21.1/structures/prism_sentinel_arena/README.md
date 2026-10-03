# Prism Sentinel arena: "Keeper's Proving Hall" (Cerulon, Galaxy 2)

This is the first guardian boss arena. It's a Concord test chamber in Cerulon's Quiet Mines: "a test, not a hunt".
Version 2 is rebuilt to `docs/zero-g-tweaks-bundle/briefs/prism_sentinel_arena.md`, and
`generators/check_arena_palette.py` prints **OK** for it (v1 failed 15 checks).

| File | What it is |
| --- | --- |
| `prism_sentinel_arena.nbt` | Structure template v2, 47 x 32 x 47 (same file on `1.21.x` in `data/zerog_tweaks/structure/`) |
| `build_prism_arena_v2.py` | The design: `python build_prism_arena_v2.py out.nbt` writes the template directly |
| `prism_arena_v2_preview.png` | Top view and south elevation, made by `render_arena_preview.py <nbt> <png>` |
| `*_v1*` | The first build, kept for reference (see `sheets/structures/prism_sentinel_arena_v1/`) |

## Layout (radius from the centre; the fight floor is template y 3)

- **Dais r0-4:** two steps of polished black and polished cerulean, crystal-glass inlay, lamp studs. The **Concord Prism**
  sits at the centre (template 23, 6, 23).
- **Fight floor r5-15:** flat polished cerulean with a smooth trim ring and 8 radial pulsar-lamp lines set flush.
- **4 refractor pylons** at the diagonals (9, 9): 3 x 3, 6 tall, crystal-glass core with a spectral lantern, cerulite-cluster
  cap. They are the only things on the floor and serve as beam cover.
- **Tiered stands r16-19:** 3 steps with lit risers (spectral lanterns every 30 degrees), an old rail line on the top
  step and 3 parked minecarts.
- **Outer wall r19.6-21.6, 9 tall:** cracked bricks at the base, a chiseled band, crystal-vein slits (crystal glass inside,
  shimmer glass outside) and half-cut geode shell. Buttresses every 45 degrees with cluster crowns and azure moss at their feet.
- **Entrance (south):** 5 wide x 7 tall stone arch, pulsar-lamp pillars, a lit keystone (the Concord mark), and a
  walkway with a crystal-sand apron and starbloom.
- **Dome:** 8 single-block ribs (with crystal veins) rising from the buttresses to a ring at y 28, holding a crystal and
  shimmer glass oculus lit by a pulsar lamp. Nothing over the floor below floor + 18.

Palette: Cerulon blocks only. There are no ores, storage blocks, gate or machine parts, vanilla amethyst, sea lanterns or Prismstone.

## In the game (`1.21.x`, 97522e8a)

- One arena per world (`concentric_rings`, count 1), placed 200-500 blocks from (0, 0) in azure_plains or shardwood_grove.
  Find it with `/locate structure zerog_tweaks:prism_sentinel_arena` (or the tag `#zerog_tweaks:boss_arenas`).
- Structure type `zerog_tweaks:dry_land_jigsaw`: it rejects water and uneven ground (max 6), and searches up to 80 blocks
  around the placement for dry land. It uses a `beard_box` foundation and blocks monster spawns inside.
- Blocks: `concord_prism` (state idle, active or defeated) and `prism_barrier` (entrance seal). Both are unbreakable with no drops.
- Next step: the Prism Sentinel entity and the fight wiring (summon, seal, boss bar, stay-in-arena goal, beam blocking,
  defeat, reset). A rematch re-arms with a Sentinel Prism, with no gate key on a rematch (owner's decision, 2026-10-02).
- `/place template zerog_tweaks:prism_sentinel_arena <x> <y> <z>` puts the template's bottom at y, so the fight floor
  lands at y + 3.
