# Concord Vault rooms: full design sheets

One sheet and one drop-in template per room. Rules: `../../briefs/concord_vault.md`.

| # | Room | Sheet | Template | Status |
| --- | --- | --- | --- | --- |
| 1 | Storage Hall | `01_storage_hall.png` | `storage_hall.nbt` | designed |
| 2 | Crystal Garden | `02_crystal_garden.png` | `crystal_garden.nbt` | designed |
| 3 | Starlight Pool | `03_starlight_pool.png` | `starlight_pool.nbt` | designed |
| 4 | Collapsed Mine | `04_collapsed_mine.png` | `collapsed_mine.nbt` | designed |
| 5 | Prismling Nest | `05_prismling_nest.png` | `prismling_nest.nbt` | designed |
| 6-10 | star_library, trap_hall, forge, observatory, concord_shrine | | | next |

Each sheet has two cutaway views, a plan of every layer (y 0-8), the block list with counts, a light map, the loot, connectors and gameplay notes, and the rule check.

To use a template, copy it over `1.21.x` `src/main/resources/data/zerog_tweaks/structure/concord_vault/rooms/<name>.nbt`. The name is the same, so the `branches` pool needs no change.
Generators: `../../generators/vault_rooms/room_<name>.py` (shared code in `room_kit.py`). Block textures come from `1.21.x`.

Room rule added by these designs: no `cerulite_cluster` (it drops Cerulite gems) and no `budding_*` blocks (an endless crystal farm). Use the small, medium and large cerulite buds for crystal decoration.
