# Brief: the Concord Vault (Prism Sentinel arena, v4)

**Status:** working first version on `1.21.x` (bd4ab216). The rooms are script-built placeholders that follow every rule
below. Rebuild any of them by hand to improve it; nothing else needs to change.

## The idea

The Sentinel's chamber is no longer a building on the surface. It is the hub of an underground complex, the **Concord
Vault**, about 45 blocks under Cerulon. It generates once per world and prefers Concord Quarries.

- A **shrine** on the surface leads to a **spiral stair shaft** that goes down to the chamber.
- **Mine corridors** branch out from the chamber's 4 doorways, like a vanilla mineshaft. Each world gets a different
  layout.
- Each **room** at the end of a corridor is picked at random from **10 designs**, each with its own loot chests.
- The **chamber starts empty**: plain floor, walls, and a **Concord Lock** in the middle.
- **Exactly 4 rooms** hold a **Key Altar** with a **Concord Key**. Taking a key wakes 3 Prismling guardians.
- Each key used on the lock **builds the next part of the chamber**:

| Key | Builds |
| --- | --- |
| 1 | the lit floor: lamp lines, trim ring, floor edge |
| 2 | the dais and the 4 refractor pylons |
| 3 | the stands, rail line, buttress crowns and crystal dome |
| 4 | the Concord Prism, after which the existing fight takes over (seal, boss, variants, rematch) |

## How it is built (for anyone editing it)

| Part | Where | Size |
| --- | --- | --- |
| Chamber shell | `structure/concord_vault/chamber.nbt` | 67 x 40 x 67 (v3 arena, 4 doorways) |
| Build stages | `chamber_stage_1..3.nbt`: only that stage's blocks, no air | same frame as the chamber |
| Corridors | `corridor_straight / _turn / _junction / _crossing`, `corridor_cap` | 7 wide, 7 tall (5 x 5 inside) |
| Entrance | `entrance_shaft.nbt`: tunnel and a 46-high spiral stair to the shrine | 9 x 53 x 16 |
| Rooms | `rooms/<design>.nbt` | **17 x 9 x 17** |

Template pools (`worldgen/template_pool/concord_vault/`):

- `start`: the chamber.
- `entrance`: the shaft.
- `corridors`: what rooms and the chamber connect to.
- `branches`: what corridors lead to. This holds the 10 rooms plus more corridors.
- `caps`: the dead ends.

The code is `ConcordVaultStructure`, which builds the layout and places the 4 altars, plus `KeyAltarPiece`,
`ConcordLockBlock` and `VaultKeyAltarBlock`. The templates come from `build_concord_vault.py` (in this folder).

## Rules for a room design (do this properly and it will just plug in)

1. **Size: exactly 17 x 9 x 17.** The floor is y 0 and the ceiling y 8. Rooms are recognised by size: anything at least
   15 wide in both directions that isn't the chamber counts as a room and can get a key.
2. **Doors:** 5 wide x 5 tall (y 1-5), centred on a side (cells 6-10).
3. **Connectors:** on each door, put a **jigsaw block** at the centre cell (8, 1, 0 for north; 8, 1, 16 for south;
   0, 1, 8 for west; 16, 1, 8 for east), facing **out**. Set name and target to `zerog_tweaks:door`, pool to
   `zerog_tweaks:concord_vault/corridors`, final state `minecraft:air`, joint `aligned`.
4. **Keep the centre free:** the 3 x 3 cells around (8, 8) must have solid floor at y 0 and air at y 1-3. That is where the
   Key Altar goes when the room is chosen as a key room.
5. **Loot:** chests use loot tables, never fixed items. Use `zerog_tweaks:chests/concord_vault/common`, `uncommon` or `rare`.
   In game: `/data merge block x y z {LootTable:"zerog_tweaks:chests/concord_vault/rare"}`.
6. **Palette:** Cerulon blocks, Shardwood, and vanilla utility blocks (chests, barrels, bookshelves, furnaces, anvils,
   dispensers, rails). **No ores or storage blocks** (free loot), and **no gate or machine parts**.
7. **Light:** spectral lanterns or pulsar lamps; no torches. Keep it readable, but rooms may be moodier than the chamber.
8. **Save it:** with a structure block (17 x 9 x 17 fits under the 48 limit) to
   `data/zerog_tweaks/structure/concord_vault/rooms/<name>.nbt`. Add a new room to the `branches` pool, weight 1.

## The 10 designs (current placeholders)

| Room | Doors | Feature | Chests |
| --- | --- | --- | --- |
| storage_hall | N S E | barrel racks, Shardwood floor | 3 common |
| crystal_garden | N W | Azure Moss, Starbloom, crystal clusters, shimmer-glass ceiling | 1 uncommon |
| starlight_pool | N S | ring pool of Liquid Starlight around the centre | 1 rare |
| collapsed_mine | N E | rubble, fallen beam, rails, chest minecart | 1 common + minecart |
| prismling_nest | N S W | geode spikes, Prismling spawner | 1 uncommon |
| star_library | N E W | bookshelves, lectern, lamps | 1 common, 1 uncommon |
| trap_hall | N S | pressure plates and arrow dispensers | 1 rare |
| forge | N E | furnaces, blast furnaces, anvil, smithing table | 1 uncommon |
| observatory | N | star-chart lamp ring, telescope | 1 rare |
| concord_shrine | N S E W | black pillars with cluster crowns, lamp ring | 1 rare |

## Still to do

- Hand-built versions of the rooms, if wanted.
- Room-specific loot tables (one per design, if wanted).
- A "build up" animation for the chamber stages. Right now each stage appears at once with particles and sound.
- In-game screenshots for `sheets/structures/`.
