# Brief: Prism Sentinel arena (Cerulon) - rework

**For:** the coding agent working on `1.21.x`. **Status of the current build:** it works as a first pass, but it has real
problems (free loot, functional gate parts used as decor, no way to start the fight, too many copies per world) and it
doesn't yet look like Cerulon or play like the boss in the spec. Read this whole file before starting, then work through
the checklist at the bottom in order.

Screenshots of the current build: `sheets/structures/prism_sentinel_arena_v1/` (front, top, three_quarter).

Sources of truth: design doc (Lore > Act 2 "The Quiet Mines"; Mobs > bosses), mob spec `sheets/mobs/data/mobs.json` >
`prism_sentinel`, and this brief. Files today: `data/zerog_tweaks/structure/prism_sentinel_arena.nbt` (47 x 22 x 47),
`worldgen/structure/`, `structure_set/`, `template_pool/prism_sentinel_arena/start.json`,
`tags/worldgen/biome/has_structure/prism_sentinel_arena.json`.

---

## 1. What the arena is (story and gameplay)

- Cerulon is the Concord's **peaceful mining world** ("The Quiet Mines"). The arena is not a fortress; it is a
  **Concord test chamber**: a crystal amphitheater the miners built to judge who may inherit their gates.
- The **Prism Sentinel is a test, not a hunt.** It asks "Are you Concord?", fights in light-refracting phases, and when
  beaten names the player an heir. The building should feel calm, precise and beautiful, lit by crystal light, with a mining
  theme (cut stone, crystal veins, old rails), not dark and spiky.
- Boss facts that drive the layout: **3.6 wide, 10.8 tall, floats** (blaze-style rig, shards orbit the core on a 4 s loop),
  **follow range 48**, beam attacks that **bounce off its orbiting shards**, phase 2 shards **circle the arena**,
  phase 3 the core opens. It needs a big, clear, tall space.

## 2. Problems in the current build (fix all of these)

| # | Problem | Why it matters | Fix |
| --- | --- | --- | --- |
| 1 | **74 `cerulite_block`** in the build | Each drops 9 Cerulite: about 660 free T3 gems before the fight | No storage blocks. Use decor blocks (see palette) |
| 2 | **35 `cerulite_ore`, 36 `starlite_ore`, 23 `lumenite_ore`** in the walls | Free ore; skips the mining ladder | No ores anywhere in the structure |
| 3 | **`cerulite_gate_frame`, `gate_pylon`, `gate_lens_housing`, `cyrrium_casing`** used as decor | Real teleporter multiblock parts: free gate parts and the risk of a gate forming | Use non-functional decor only |
| 4 | **Vanilla amethyst clusters/buds, sea lanterns** | Off-palette (purple, vanilla) | `cerulite_cluster`, `pulsar_lamp`, `spectral_lantern` |
| 5 | **Prismstone family** (purple dais, black-purple pillars, ~880 blocks) | Prismstone is the *crystal wasteland* stone, not Cerulon | Polished-black Cerulean Stone family; Prismstone at most as a tiny accent |
| 6 | `prism_cluster` (14) | Belongs to the crystal wasteland | `cerulite_cluster` |
| 7 | **No summon** (0 block entities, 0 entities) | Nothing starts the fight | Add the Concord Prism altar (section 5) |
| 8 | **`random_spread` spacing 24** | An arena every ~24 chunks; the boss should be unique | One arena per Cerulon (section 6) |
| 9 | Only **22 blocks tall**; dome ribs are low black arches | A 10.8-block floating boss with orbiting shards will clip ribs and lantern chains | 32 tall, clear headroom (section 3) |
| 10 | **8 tall pillars inside the fight floor** | They block beams and pathing at random; the boss gets stuck | 4 deliberate refractor pylons only (section 3) |
| 11 | Door is a plain open hole | Players can leave and reset; mobs wander in | Seal during the fight (section 5) |
| 12 | `spawn_overrides` empty | Hostile mobs can spawn in the dark parts | Block monster spawns in the whole box (section 6) |
| 13 | Flat brick outer wall, black "spider leg" ribs | Reads as a dark fortress, not a crystal amphitheater | Buttresses, crystal veins, open crystal lattice dome (section 4) |

## 3. Layout (top-down, sizes in blocks)

Keep one template piece if it stays **<= 48 x 48 x 48** (structure block limit). Target: **47 x 32 x 47**, floor at y = 3
inside the template so there is foundation below it.

```
                    N
        . . . . outer wall r20-23 . . . .
      .   tiered stands r16-19 (3 steps up)  .
    .        P                     P          .      P = refractor pylon (r12-14, diagonals)
   .                                           .
   .            fight floor r5-15               .
   .          ( flat, clear, no blocks )        .
   .                 [ dais r0-4 ]               .      dais: 2 steps up, Concord Prism at centre
   .                                           .
    .        P                     P          .
      .                                     .
        . . . . . [  ENTRANCE  ] . . . . .            entrance: south, 5 wide x 7 tall, sealable
                    S
```

| Ring (radius from centre) | What | Rules |
| --- | --- | --- |
| r0-4 | **Dais** | 9 x 9, 2 steps up, polished cerulean with cerulite-glass inlay. **Concord Prism** block at the exact centre. Boss spawns 3 blocks above it |
| r5-15 | **Fight floor** | Completely flat, no obstacles. Keep the radial **pulsar lamp lines** (they look great); recess them so the floor stays flush |
| r12-14 | **4 refractor pylons** on the diagonals | 3 x 3, 6 tall, crystal-glass core, cerulite-cluster caps. They are **beam cover**: the Sentinel's beams stop on them. They are the only things on the floor |
| r16-19 | **Tiered stands** | 3 steps rising outward (the amphitheater). Seats the arena visually and gives players high ground. No roof over them |
| r20-23 | **Outer wall** | 8-10 tall, with buttresses every 45 degrees and crystal-vein windows |
| above | **Headroom** | Nothing below **y = floor + 18** over the floor and dais, so the 10.8-tall boss can float and orbit freely |
| apex | **Dome** | Open lattice: 8 thin ribs (1 block) rising from the buttresses to a ring at about floor + 26, holding a **crystal-glass oculus** with a beam of light (Liquid Starlight or a pulsar column) straight down onto the dais |

## 4. Look and palette

Mood: Concord craftsmanship. Clean cut stone, glowing crystal seams, calm blue light. Think "crystal observatory in a
quarry", not "dark castle".

**Allowed (Cerulon):** `cerulean_stone` set (bricks, polished, chiseled, smooth, cracked bricks for age),
`polished_black_cerulean_stone(_bricks)` and chiseled black (trim and the dais), `crystal_glass`, `shimmer_glass`,
`cerulean_geode_shell`, `cerulite_cluster` (decor crystals), `azure_moss` (overgrowth at the base and in cracks),
`crystal_sand` (outside apron), `pulsar_lamp`, `spectral_lantern`, `starbloom` and `shardwood` (planters around the
outside), `liquid_starlight` (one channel or the oculus beam), stairs, slabs and walls of the above.

**Banned in the template:** any `*_ore`, any `*_block` storage block (cerulite, starlite, lumenite, ...), any gate or
machine part (`*_gate_frame`, `gate_*`, `*_casing`, `crystal_cell`, machines), vanilla amethyst, sea lantern, Prismstone
family (except up to ~20 accent blocks), chests with loot (the boss drops the loot).

**Details to add:**
- Exterior: buttresses with a cerulite-cluster crown, crystal veins running up the walls (crystal glass behind
  chiseled stone), azure moss and cracked bricks at the base, a crystal-sand apron with a walkway to the entrance.
- Entrance: a carved arch with the Concord mark (chiseled black stone) and two pulsar lamp pillars. Replace the
  gate-frame "portal" look with a stone arch, so nobody mistakes it for a teleporter.
- Mining theme: an old rail line along the stands with 2-3 decorative minecarts, and a few "half-cut" crystal blocks
  in the outer wall, as if the miners stopped mid-job.
- Light: every floor and stand block must be at light 8 or more (no dark corners), but keep it moody. Use pulsar lamps and
  spectral lanterns, no torches.
- Remove the hanging chain lantern from the apex: the boss orbits there.

## 5. Gameplay wiring (Java + data)

1. **Concord Prism** (new block `zerog_tweaks:concord_prism`, block entity, unbreakable in survival, no drops):
   - Right-click it (or step within 6 blocks) to start: chat line `prism_sentinel.ask` ("Are you Concord?"), then
     after 3 s the Sentinel spawns 3 blocks above the prism with a short rise animation.
   - The block entity tracks the state: `IDLE -> ACTIVE -> DEFEATED`. While `ACTIVE`, right-click does nothing.
2. **Seal the arena:** on start, place a `prism_barrier` (new decor block: translucent cyan, unbreakable, no drops) in the
   entrance. Remove it when the boss dies, or 10 s after every player has left or died, which also despawns the boss
   and resets to `IDLE`.
3. **Boss bar:** `ServerBossEvent` (BLUE, 3 notches), shown only to players inside the arena box (inflate 4).
4. **StayInArenaGoal:** a 20-block radius around the prism. If pushed out, the boss teleports back to the dais.
5. **Refractor pylons:** beams that hit a pylon block stop there (raycast against the block tag
   `zerog_tweaks:beam_blocking`, which holds the pylon blocks).
6. **Defeat:** chat line `prism_sentinel.heir` ("...you are Concord. Inherit."), drops from the existing loot table, the
   oculus beam turns on (swap the oculus core to lit Liquid Starlight or a pulsar column), the prism goes to `DEFEATED`
   (glowing, inert), the barrier opens, and the advancement `codex/prism_sentinel` triggers.
7. **Rematch (optional, decide with the owner):** a `DEFEATED` prism accepts a Sentinel Prism item to re-arm for another
   fight (no gate key on rematch).

## 6. Placement

- **One arena per Cerulon.** Replace `random_spread` with a `concentric_rings` placement (`count: 1`, small `distance`,
  `spread: 1`) so a single arena generates a few hundred blocks from (0, 0). Check it in the Cerulon dimension; if
  `concentric_rings` misbehaves in custom dimensions, use `random_spread` with `spacing: 256`, `separation: 128` and
  accept rare duplicates.
- Biomes: keep `azure_plains`, `shardwood_grove`. Don't place it on water or crystal-geode biomes.
- `terrain_adaptation: "beard_box"`, so the foundation fills down to the ground on uneven terrain (`beard_thin` leaves
  gaps under a 47-wide build). `max_height_difference` to 6.
- `spawn_overrides`: block monsters inside the whole structure:
  `"monster": {"bounding_box": "full", "spawns": []}`.
- Add the structure to a new tag `zerog_tweaks:boss_arenas`, so the Codex or star chart can point to it later.

## 7. Checklist (in order)

- [ ] Rebuild the template in a creative test world with the palette above (47 x 32 x 47), and save it over
      `structure/prism_sentinel_arena.nbt`.
- [ ] Run `python3 docs/zero-g-tweaks-bundle/generators/check_arena_palette.py <nbt>` (on the `Design` branch). It must
      print `OK` (no ores, storage blocks, gate parts, vanilla amethyst or sea lanterns; size and headroom correct).
- [ ] Add `concord_prism` and `prism_barrier` (blocks, items for creative only, models, lang, loot = none) and place the
      prism at the dais centre in the template.
- [ ] Wire the Sentinel: start, seal, boss bar, arena goal, beam blocking, defeat, reset (section 5).
- [ ] Update the structure, structure set and spawn overrides (section 6).
- [ ] `./gradlew build`, then `runClient`. In Cerulon: `/locate structure zerog_tweaks:prism_sentinel_arena` finds one arena;
      `/place structure ...` on a slope leaves no floating gaps; no hostile mobs spawn inside; fight start to finish in
      survival; leaving resets it; the floor is lit everywhere (F3 block light >= 8).
- [ ] Commit the code to `1.21.x`; screenshots (front, top, inside, mid-fight) to `Design` under
      `docs/zero-g-tweaks-bundle/sheets/structures/`.
