# Prism Sentinel arena — "Keeper's Proving Hall" (Cerulon, Galaxy 2)

The first guardian boss arena. Design doc: the Prism Sentinel is a Keeper construct whose fight is "a test, not a
hunt" with light-refracting phases, on Cerulon, the Concord's peaceful mining world.

| File | What it is |
| --- | --- |
| `prism_sentinel_arena.nbt` | Structure template, 47 x 22 x 47 (also on `1.21.x` as `data/zerog_tweaks/structure/`) |
| `prism_arena_preview.png` | Top view and south elevation |
| `build_prism_arena.py` | The design: writes the `/fill` + `/setblock` commands used to build it in game |
| `export_arena_nbt.py` | Writes the `.nbt` from the same design (structure-block SAVE format, DataVersion 3955) |

Layout: cerulean-stone hall (ore seams of cerulite, lumenite and starlite; crystal and tinted-glass windows);
polished prismstone floor with a black prismstone ring and 8 pulsar-lamp light channels feeding the central dais
(cerulite core under crystal glass, prism clusters and amethyst); 8 crystal pillars with sea lanterns and gate lens
housings aimed at the dais; dome ribs rising to a crystal-glass oculus with a hanging lantern; south entrance through
a cerulite gate-frame arch with gate pylons, spectral lanterns and cyrrium machinery; azure moss and crystals outside.

In game: `/place template zerog_tweaks:prism_sentinel_arena <x> <y> <z>` (the floor sits at the given y).
Built on the mod's server in a superflat creative world, then checked: the placed template matches the built hall
block for block. Not yet in world generation, and the Prism Sentinel itself is not implemented yet.
