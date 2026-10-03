# Concord Vault rooms: full design sheets

One sheet and one drop-in template per room. **All 10 are designed**; `00_overview.png` shows them side by side. Rules: `../../briefs/concord_vault.md`.

| # | Room | Sheet | Template | Status |
| --- | --- | --- | --- | --- |
| 1 | Storage Hall | `01_storage_hall.png` | `storage_hall.nbt` | designed |
| 2 | Crystal Garden | `02_crystal_garden.png` | `crystal_garden.nbt` | designed |
| 3 | Starlight Pool | `03_starlight_pool.png` | `starlight_pool.nbt` | designed |
| 4 | Collapsed Mine | `04_collapsed_mine.png` | `collapsed_mine.nbt` | designed |
| 5 | Prismling Nest | `05_prismling_nest.png` | `prismling_nest.nbt` | designed |
| 6 | Star Library | `06_star_library.png` | `star_library.nbt` | designed |
| 7 | Trap Hall | `07_trap_hall.png` | `trap_hall.nbt` | designed |
| 8 | Forge | `08_forge.png` | `forge.nbt` | designed |
| 9 | Observatory | `09_observatory.png` | `observatory.nbt` | designed |
| 10 | Concord Shrine | `10_concord_shrine.png` | `concord_shrine.nbt` | designed |

Each sheet has two cutaway views, a plan of every layer (y 0-8), the block list with counts, a light map, the loot, connectors and gameplay notes, and the rule check.

To use a template, copy it over `1.21.x` `src/main/resources/data/zerog_tweaks/structure/concord_vault/rooms/<name>.nbt`. The name is the same, so the `branches` pool needs no change.
Generators: `../../generators/vault_rooms/room_<name>.py` (shared code in `room_kit.py`). Block textures come from `1.21.x`.

Room rule added by these designs: no `cerulite_cluster` (it drops Cerulite gems) and no `budding_*` blocks (an endless crystal farm). Use the small, medium and large cerulite buds for crystal decoration.

## Installing all 10
Copy every `*.nbt` here over `1.21.x` `src/main/resources/data/zerog_tweaks/structure/concord_vault/rooms/`. The names match the placeholders, so the `branches` pool needs no change. Then:
- run `python3 ../../generators/check_arena_palette.py`-style checks if you edit them (each generator already runs the vault rule check);
- in game, `/place template zerog_tweaks:concord_vault/rooms/<name>` and walk through each one;
- check the spawner in the Prismling Nest and the dart traps in the Trap Hall fire, and that the Star Library's lectern book opens.

Rules these designs added to the brief: no `cerulite_cluster` or `budding_*` blocks (free gems or an endless farm); no lava (Shardwood burns); fluids sit in raised basins with a floor under them; every walkable cell at light 1 or more so nothing spawns naturally, except a spawner's own area, which must stay at light 11 or lower.
