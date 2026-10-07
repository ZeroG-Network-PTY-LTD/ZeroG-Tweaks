# AGENTS.md: build guide for ZeroG Tweaks

This file is for the AI coding agent (or human) turning this repo into a working mod. Read it top to bottom before writing code. The **design doc** is the source of truth for gameplay: `docs/zero-g-tweaks-bundle/ZeroG_Tweaks_Design_Doc.md`. (The `docs/` design bundle lives on the `Design` branch; player docs, images and release jars on the `Docs` branch.) This file tells you what already exists, what data expects from Java, and what is left to build.

## Branch layout — read before committing

This repo keeps code, design work and documentation on separate branches.
Put every change on the branch it belongs to.

| Branch | What goes here |
| --- | --- |
| `Released` | Major released code only. Never commit or push here directly; it is updated only by merging a version dev branch (via a pull request) when a release ships. |
| `1.21.x` | Dev branch for Minecraft 1.21.x. **All code**: `src/`, Gradle files (`build.gradle`, `settings.gradle`, `gradle.properties`, `gradle/`, `gradlew*`), `tools/`, `AGENTS.md`, `.gitignore`. Future Minecraft versions get their own dev branch (`26.1.x`, `26.2.x`, …). |
| `Design` | **All design work**: Blockbench models (`*.bbmodel`), work-in-progress textures, art and reference sheets, asset collections, concept art, generator scripts, design notes (`docs/zero-g-tweaks-bundle/`, `docs/asset-collection-*`, `docs/shattered-skies/`, `docs/tidewraith-approved/`, …). |
| `Docs` | **All documentation / wiki**: README content, `docs/HELP.md`, `docs/images/` (diagrams, gallery, logo), `docs/jars/` (release jars + `SHA256SUMS.txt`), guides. |

Rules:

1. `git fetch` first, then check out the right branch for each change. If a task
   touches code *and* docs/images/design, make **separate commits on separate
   branches**.
2. `Design` and `Docs` have histories unrelated to the code branches. **Never merge
   `Design` or `Docs` into `1.21.x` or `Released`** (or the reverse), and never use
   `--allow-unrelated-histories`.
3. Never put game code under `docs/`, and never add `docs/` folders to a code branch.
   The code-branch README links to `Docs`/`Design` with absolute GitHub URLs; keep
   those links working.
4. Never commit directly to `Released`, never force-push, never delete branches or
   the `archive/*` tags (they are backups of the pre-cleanup branches).
5. Code changes must pass `./gradlew build` before pushing. When new release jars
   are built, commit them to `Docs` under `docs/jars/` and regenerate
   `docs/jars/SHA256SUMS.txt`.
6. `git pull --rebase` before pushing so you don't overwrite someone else's work.
7. When done, report which files went to which branch, with commit hashes.

## Ground rules

- **Correctness-first extension (2026-10-05):** read the [storage/machinery workflow](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/storage-and-machinery-workflow.md) and [tracked TODO ledger](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/storage-and-machinery-todo.json) before new machine work. Existing purpose/GUI/port bugs take priority over new decorative machines. Equipment uses vanilla/netherite humanoid armour geometry with original retextures, except the four Sol sets (Nullifite, Ferrox, Moonsteel, Olympium), which the owner made GeckoLib chunky-shell 3D armour on 2026-10-06 (`ItemInit.GEO_ARMOR_SETS`; Nullifite and Ferrox borrow Moonsteel's shell). Keep those as 3D shells; do not switch them back to flat layers or re-enable shells for other sets without the owner's say. Mekanism/example JARs are read-only references, never copied code/art or required dependencies. Storage, generator and pipe upgrades must be independent, bounded and conserved; never consume filled tank contents in a recipe. Planetary crops survive darkness on farmland with slow growth; retain the complete maintains_farmland tag.

- **Current runtime workflow:** `genetics/` implements actual analysis, sampling, single-trait splicing and honey/jelly tank support using Productive Bees cage/attachment APIs. Concord Codex research gating is the approved future mechanism, not a verified completed feature. Alveary controllers use separate persistent 27-frame storage with tier unlocks, FE/tanks, verified recipe outputs and bounded automation; unavailable native lifespan/mutation/territory alleles are explicitly not invented. `transport/` implements six tiers, conserved loaded-only networks, cells, ports, filters, wrench upgrades and shared-owner Null Links. `travel/SurvivalGate*` implements player-built progression separately from admin hub gates. Disposable workflow/genetics/planet tests are opt-in; rebuild normally before distribution so test classes do not ship. See [the evidence ledger](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/sol-build-workflow-2026-10-05.md). Client visual approval, third-party claim integration and undefined hidden-world coordinates remain distinct from successful server checks. Never imply a preview or compile verifies them.

- **Locked artwork standard (Claude and all contributors):** read [Design/docs/art-direction-lock.md](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction-lock.md) before creating or changing textures. Equipment/materials use C magitech; vegetation blends A natural shading and C selective luminous buds/fruit. Use centred readable sprites, hue-shifted shadows/highlights, coherent pixel density, and matching inventory/placed artwork. No flat placeholders, no gems in dirt/farmland; update generators and validate active resource-pack layers. Concept previews are not in-game proof.

- **Platform:** Minecraft 1.21.1, NeoForge 21.1.x (ModDevGradle), Java 21, Parchment mappings. Mod id `zerog_tweaks`, package `net.zerog.tweaks`.
- **All logic is Java.** Don't use KubeJS or CraftTweaker.
- **Branches:**
  - `1.21.x` is the active code line.
  - `Released` is for releases.
  - `Design` owns art/generators; `Docs` owns documentation/jars. Never merge their histories into code.
- **Never rename or remove an existing registry id** (block, item, feature, biome, dimension, loot table). Save data, recipes and tags depend on them. Add new ids instead.
- **Match vanilla behaviour first.** When a ZeroG thing has a vanilla counterpart, copy the counterpart:
  - Pyrevine = cave vines.
  - Glowkelp = kelp.
  - Lichens = glow lichen.
  - Sands = sand/gravel.
  - Flower pots = vanilla potted plants.

  The plant classes in `registry/ZG*Block.java` show the pattern: extend or mirror the vanilla class and swap in our blocks and items.
- **Build before every commit:** run `./gradlew build`. Then `./gradlew runClient` and check the log for `Failed to load` / `Couldn't parse` datapack errors.

## Repository map

| Path | What it is |
| --- | --- |
| `src/main/java/net/zerog/tweaks/ZeroGTweaks.java` | Mod entry. Registers blocks, items and the creative tab. |
| `registry/BlockInit.java` | All 890 blocks (`DeferredRegister.Blocks`), plus flower-pot hookup in common setup. |
| `registry/ItemInit.java` | All items. |
| `registry/CreativeTabs.java` + `ZGCreativeTabContents.java` | Seven vanilla-style tabs (Building, Natural, Functional, Tools & Utilities, Combat, Food & Drinks, Ingredients) after the vanilla tabs. The contents file is **generated** by `generators/creative_tabs.py`; re-run it after adding items. Unlisted items fall into Ingredients. |
| `registry/ZG*Block.java` | Block classes: plants, crops, crystals, layers, doors, oriented machines. |
| `registry/ZGTrees.java` | TreeGrowers. Saplings grow `worldgen/configured_feature/<wood>_tree`. |
| `item/ZGFoods.java`, `item/ZGFoodItems.java`, `event/ZGInteractions.java` | Food properties and special food items. |
| `src/main/resources/assets/zerog_tweaks` | Textures, models, blockstates, lang, GeckoLib models and animations for 28 mobs and all armor sets. |
| `src/main/resources/data/zerog_tweaks` | Recipes, loot, tags, worldgen, dimensions, damage types, advancements. |
| `src/main/resources/data/{minecraft,c,neoforge}` | Vanilla/common tags and NeoForge data maps. |
| `docs/zero-g-tweaks-bundle/java/` | **Written but not yet wired Java:** effects, six fluids, block tinting, GeckoLib entities and armor, spawn eggs. Move these into `src/` when you do their milestone. |
| `docs/zero-g-tweaks-bundle/pending-data/` | **Data that needs Java first** (see "Pending data" below). Move each file into `src/main/resources/data/zerog_tweaks/` once its registry exists. |
| `docs/zero-g-tweaks-bundle/data-manifest.json` | Machine-readable summary: planets, gravity, ores per planet, wasteland types, galaxy slot defaults, structure loot tables, damage types. |
| `docs/zero-g-tweaks-bundle/sheets/` | Texture reference sheets. |
| `docs/zero-g-tweaks-bundle/sheets/mobs/` | **Mob spec pack:** `data/mobs.json` (start here), CSVs for attributes, AI goals, state transitions, animations, drops and spawns, `mobs.xlsx`, and diagrams (world map, food chain, boss progression, a state machine per mob). See its README. |
| `docs/zero-g-tweaks-bundle/generators/` | Python scripts that produced the art and data. Re-run `data_extra.py` to regenerate recipes, worldgen, tags, loot, advancements and damage types. |

## What the data layer already provides (no Java needed)

- **Recipes (1,777):**
  - Crafting, smelting, blasting, smoking and campfire recipes.
  - Stonecutting for every stone family.
  - Smithing upgrades: Nullifite → Olympium → Cerulite → Skarnite → Eidolite → Solvanite, plus template duplication.
  - Machines, casings, gate parts, lamps, hull and plating blocks, dyes from flowers, and mob-drop conversions.
- **Loot:**
  - Every block's loot table, including silk touch, shears, fortune and multiface lichen drops.
  - 28 entity loot tables. Bosses drop their gate key, trophy and next upgrade template.
  - 10 structure chest tables under `loot_table/chests/`: `sunken_relay`, `buried_observatory`, `collapsed_forge`, `frozen_outpost`, `sunken_lab`, `prism_spire`, `impact_site`, `derelict_wreck`, `mars_crash_site`, `solar_shrine`.
- **Tags:**
  - Mineable and tool-level tags, `needs_<tier>_tool`.
  - `c:` ores, ingots, gems, dusts, nuggets, raw materials and storage blocks.
  - Vanilla tool and armor item tags (enables enchanting): `swords`, `pickaxes`, `head_armor`, and the rest.
  - `trimmable_armor`, `coals`, `meat`, `fishes`, `flowers`, `small_flowers`, `flower_pots`, `climbable`, `cave_vines`.
  - `overworld_carver_replaceables` (caves carve through planet stone), `dirt`, `sand`, `ice`.
  - Damage-type tags.
- **NeoForge data maps:** `furnace_fuels` (planet fuels) and `compostables` (all plants).
- **Worldgen:**
  - **Ore features:** configured and placed ore features for all 38 planet ores, placed per the design doc's ore table. Nullifite is added to the Overworld deepslate by a biome modifier, with extra ore in the Deep Dark.
  - **Other features:** a Cerulite geode, trees for all four woods, flower and plant patches, Pyrevine columns, Glowkelp columns, and lichen growth.
  - **Signature blocks per wasteland:** brine crystal, ruinstone, vent rock, frost crystal, prism cluster, meteorite and similar.
- **Dimensions (34):**
  - **Fixed planets:** `zerog_tweaks:moon`, `mars`, `cerulon`, `skarn`, `eidolon`, `solvane`. Each has its own noise settings (base stone, surface blocks, sea level) and 3 biomes (sky, fog and water colours from the palettes).
  - **Galaxy slots:** `zerog_tweaks:g{2..5}_p{1..6}` wastelands plus `g{2..5}_moons`. Each slot uses one of 7 wasteland noise settings (ocean, desert, volcanic, frozen, toxic, crystal, barren) with 2–3 biomes each. The slot → type mapping in `data-manifest.json` is a **deterministic default**. The seeded galaxy generator (M5) replaces it.
- **Damage types:** `ember_crust`, `corona_crust`, `flare_vent`, `vent_rock`, `acid`, `polar_frost`, `void_rift`, each with death messages.
- **Advancements:** a Codex tree under `advancement/codex/`, written as Echo's campaign in five acts.
- **Lang:** names for everything above.

You can test the data today with `/execute in zerog_tweaks:cerulon run tp @s 0 120 0`.

## Pending data (move into `src/` after the Java exists)

| File(s) in `docs/zero-g-tweaks-bundle/pending-data/` | Needs | Move to |
| --- | --- | --- |
| `neoforge/biome_modifier/spawns_*.json` | The 28 entity types registered (ids = GeckoLib model names) | `data/zerog_tweaks/neoforge/biome_modifier/` |
| `recipe/refining/*` | Recipe type + serializer `zerog_tweaks:refining` {ingredient, result, upgraded_result_count, energy, time} | `data/zerog_tweaks/recipe/refining/` |
| `recipe/alloying/*` | `zerog_tweaks:alloying` {ingredients[{item,count}], optional catalyst{item,consumed}, result, energy, time} | same pattern |
| `recipe/crystal_growth/*` | `zerog_tweaks:crystal_growth` {seed, feed{item,count}, result, energy, time} | same pattern |
| `recipe/salvaging/*` | `zerog_tweaks:salvaging` {ingredient, results[{id,count,chance}], energy, time} | same pattern |
| `data_maps/item/combustion_fuels.json` | Data map `zerog_tweaks:combustion_fuels` {fe_per_tick, burn_ticks} | `data/zerog_tweaks/data_maps/item/` |

Shattered Skies mobs (Meteor Maw, Mossback, Slagjaw, Shardmother, Hollow Sentinel, Tidewraith, Amethyst Stalker, Stormbitten Wyvern) come from the shared mob library in its own namespace. Add their spawns in that library or with a biome modifier that references its ids.

## Java work remaining, in build-order milestones

Tick these off in order; each milestone should leave something testable. Ids referenced below already exist unless marked **new**.

### M0 Foundation

- [x] Add the GeckoLib 4.x NeoForge dependency to `build.gradle` (verified 4.9.3).
- [x] Add a `ModConfigSpec` with:
  - a global ore rarity multiplier;
  - FE costs per tier (design: 500k / 1M / 3M / 8M / 20M / 50M; +10% per passenger; 25% within a galaxy);
  - gravity overrides.
- [ ] Fix block properties. Most blocks were registered with the generic `props(STONE, 2.5F, 7.0F)`. Give each family sensible hardness, sound and map colour:
  - ores 3.0;
  - planks/wood `SoundType.WOOD`;
  - glass `SoundType.GLASS` with `noOcclusion` and a translucent/cutout render type;
  - leaves already use LeavesBlock;
  - wooden fences are already `FenceBlock`, and the sands, Rustsand, Regolith and Slag already fall like sand/gravel.
- [x] Make all 164 `*_stairs` pass their real base block state, not `Blocks.STONE`; base registrations precede stair suppliers. Design source: `docs/sol-runtime-source/repair_stair_bases.py`.

### M1 Sol materials and gear

- [x] **Tool tiers:** all 20 sets use their registered mining tiers:
  - incorrect-for tag `zerog_tweaks:incorrect_for_<set>_tool` (**new** tags);
  - strengths from the design doc Gear table.
- [x] **Tool classes:** registered `SwordItem`, `PickaxeItem`, `AxeItem`, `ShovelItem` and `HoeItem` with `Item.Properties().attributes(...)`.
- [x] **Armor materials:** all 20 real armor materials and 80 wearable items are registered. Sixteen sets use vanilla/netherite humanoid armor proportions with original material retextures on the verified Netherite UV coverage. The four Sol sets (Nullifite, Ferrox, Moonsteel, Olympium) wear GeckoLib chunky shells (`ZGGeoArmorItem`/`ZGGeoArmorRenderer`, with glow and trim layers), restored by the owner on 2026-10-06; keep them 3D.
- [x] **Mining gates:** tier tools use the incorrect-for tags and ore requirements; retain the existing registry IDs.
- [ ] **Set bonuses:** per the Gear table (Null Step, Dust Shield, Crystal Sight, Ember Walk, Phantom Veil, Starborne and the 14 metal perks). Check each tick or on equipment change.
- [x] **Armor trims (data + assets done):** 20 trim materials (`data/zerog_tweaks/trim_material/`, one per armor set) and 10 ZeroG trim patterns (`trim_pattern/`) with template items (`registry/ZGTrims.java`, generated by `generators/trims.py`), smithing and duplication recipes, overlay textures, atlas sources (`assets/minecraft/atlases/armor_trims.json`, `blocks.json`) and trimmed icons for all 80 armor pieces. Templates drop from the structure chests. To see trims worn:
  - the armor items must become real `ArmorItem`s (above);
  - the GeckoLib armor renderer needs a trim layer, because GeckoLib doesn't draw vanilla trims by itself.
  - Vanilla armor trimmed with a ZeroG material shows the amethyst trim on its icon (worn trims are correct). Fixing that means overriding the vanilla armor item models; leave it unless it matters.
- [ ] **Armor upgrades:** Abyssal Pearl, Heatproof Plating, Neutralizer and Grav Boots are smithing upgrades stored as a **new** data component.

### M2 Teleporter core

- [ ] **Gate multiblock:**
  - Part blocks: `gate_controller`, `gate_pad_plate`, `gate_pylon`, `gate_energy_port`, `gate_lens_housing`, `<tier>_gate_frame`.
  - Tier shapes follow the design doc's Multiblock table.
  - Ghost preview of the next tier. Breaking a part drops the gate one tier.
- [x] **Controller:** BlockEntity + menu, FE buffer, tiered star chart and upgrade slots; server revalidates destination, ownership, charge and current tier.
- [x] **Teleport:** `DimensionTransition` with pad passengers, ready countdown and eligible pets; cold home-gate footprint is loaded before return validation.
- [x] **Landing platform:** created on first survival arrival, crystal-cell trickle charge and home routing; admin hub remains separate.
- [x] **Recall and Group Anchors:** implemented items, home routing, FE costs and cooldowns.

### M3 Sol dimensions

- [x] **Gravity:** transient dimension modifiers and configured six Sol values; seeded wasteland gravity; clears on return and survives player clone correctly.
- [ ] **Surface hazards** use the damage types above:
  - Ember Crust and Corona Crust hurt like magma blocks;
  - Flare Vent erupts on a timer;
  - Vent Rock smokes and burns;
  - Polar Frost slows and freezes;
  - Glacial Ice is slippery (friction 0.98);
  - Phantom Ice glows and is translucent.
- [ ] **Crystals:** `budding_cerulite` grows `cerulite_cluster` like budding amethyst; the Prism Cluster buds likewise.

### M4 Machines

- [ ] **Machine blocks:** BlockEntities, menus and screens with FE for `combustion_generator`, `solar_array`, `fusion_reactor`, `ore_refinery`, `alloy_forge`, `crystal_growth_chamber`, `salvage_station`.
- [ ] **Recipe types:** register the four recipe types and serializers from **Pending data**, then move those JSONs in.
- [ ] **Casing tiers:** Cyrrium, Tectium, Wraithsteel and Astrium casings set speed and efficiency. `cryo_core` and the energy dusts are upgrades.
- [ ] **Solar Array output:** varies by dimension (weak on Eidolon, huge on Solvane).

### M5 Galaxy system

- [ ] **Seeded galaxy generator:** a custom `ChunkGenerator` (or a biome source + noise-settings swap) reads the world seed and picks each `g{N}_p{M}` slot's wasteland type. Reuse the 7 `wasteland_*` noise settings and biomes. Don't show unused slots on the star chart.
- [ ] **Catalog names:** display-only, e.g. `ZG-855 d "Vorrhex"`, from a seeded name pool.
- [x] **Block tinting:** `src/.../client/ZGBlockColors.java` is wired (it reads the galaxy from `gN_pM` dimension ids and falls back to Galaxy 2). Any new grayscale block must be added to its map, or it renders grey. See `docs/zero-g-tweaks-bundle/sheets/fixes/README.md` for the texture and model rules.

### M6–M9 Galaxies 2–5

- [ ] **Entities:** register the 28 entity types from `sheets/mobs/data/mobs.json` (attributes, goal order, states and mechanics are all there) with spawn placements, renderers (`docs/.../client/ZGGeoEntities.java`). Spawn eggs already exist (`registry/ZGSpawnEggs.java`, generated by `generators/spawn_eggs.py`): each egg looks its entity up by id (`zerog_tweaks:<mob>`, or for Shattered Skies creatures `shatteredskies:<id>`, then `zerog_tweaks:<id>`), so it works as soon as that entity type is registered. Then move the spawn biome modifiers in.
- [ ] **Bosses:** Prism Sentinel, Rift Tyrant, Eidolon Captain and Dying Star, with arenas on each key world. Loot tables are already done.
- [ ] **Structures (Jigsaw):** Sunken Relay, Buried Observatory, Collapsed Forge, Frozen Outpost, Sunken Lab, Prism Spire and Impact Site; Eidolon derelict wrecks; Mars crash site; Solar shrine. Point their chests at the matching `loot_table/chests/*`.
- [ ] **Liquids:** wire `docs/.../fluid/ZGFluids.java` and `client/ZGClientExtensions.java`. The fluid tags already exist.
- [ ] **Effects:** wire `docs/.../effect/ZGEffects.java` (Freeze Ward, Surefoot), then `ZGFoods` effects become live.
- [ ] **Foods:** register the remaining special foods from `docs/.../java/ZGFoodItems.java` and interactions (Frost Yak milk → `frost_milk`, Shardwood tap → `shardwood_syrup`).

### M10–M12

- [ ] **Travel polish:** launch animation, custom dimension transition screen, co-op ready-check.
- [ ] **Codex and ending:** Codex book UI (advancements already exist under `codex/`), plus the Heart of Solvane ending choice.
- [ ] **Compatibility:** Create and Mekanism recipes behind `neoforge:mod_loaded` conditions; optional Ad Astra and Galacticraft content.

## Conventions and gotchas

- **Block registration:** `BLOCKS.registerBlock(id, Ctor::new, props)` for custom classes, `BLOCKS.register(id, () -> new X(...))` otherwise. Item blocks go in `ItemInit` via `registerSimpleBlockItem`. Vanilla-style "no block item" blocks (like `pyrevine_plant`, `glowkelp_plant`, `potted_*`) intentionally have none.
- **Pyrevine is planted with Pyrefruit** (`ItemNameBlockItem`), exactly like glow berries.
- **Plant ground rule** lives in `ZGPlantSupport.canSupport`: dirt, farmland, or any sturdy top face. Reuse it for new plants.
- **1.21.1 data folders are singular:** `recipe/`, `loot_table/`, `tags/block`, `tags/item`, `advancement/`. Recipe results use `{"id": ..., "count": ...}`.
- **Biome features:** biomes list 11 feature steps; ores go in step 6 (`underground_ores`), plants and trees in step 9. Keep the same feature order in every biome of one dimension, or you get a "feature order cycle" crash.
- **Texture sources:** textures are generated. To change art, edit the generator in `docs/zero-g-tweaks-bundle/generators/` and re-run it rather than hand-editing PNGs, so the sheets stay in sync.

## Verification checklist per PR

1. `./gradlew build` passes.
2. `./gradlew runClient` gives a new world with no datapack errors in `logs/latest.log`.
3. `/execute in zerog_tweaks:<planet> run tp @s 0 150 0` for each changed dimension; the terrain, ores (`/locate` is not available for features, so dig) and plants look right.
4. JEI or the recipe book shows new recipes; loot tables drop what they should.
5. Push each change to its owning branch; describe changes and id additions.

## Intended testing instance

CurseForge Java/NeoForge: `C:\Users\jakem\curseforge\minecraft\Instances\ZeroG`.
Never launch Bedrock. Publishing alone does not authorise game launches, installed
jar replacement or world changes. Isolated test evidence is not modpack approval.
Archived Java drafts are in tools/design-code-archive/, not compiled or under the
root docs/ directory. Generator implementations live on Design.

## October 5 faceted-armour/visual repair boundaries

Run Design's `docs/full-art-rollout-v4/generate.py` last for native source artwork.
Forty worn layers are now 128x64 but preserve normalized vanilla Netherite alpha/UV
coverage; do not restore old flat 64x32 artwork. The four Sol sets are the owner-approved
exception: they wear the GeckoLib chunky shells (geo/item/armor, textures/item/armor/<set>.png).
Client visual approval is separate from the source/UV and isolated server checks.
Do not paint fake fluid inside tank textures: the synchronized fluid renderer owns it.
Transport physical save indices remain nine; energy/fluid families permit only
labelled legacy take-out recovery, never new incidental item insertion. Ghost controls
must match supported families and reject forged commands server-side.
The ordinary addon centrifuge's actual output regression PASSES: the earlier suspected
infusion dispatch was disproved. Smelter/weaver/infusion unused-input rejection applies
to menus and capabilities, while old stacks stay recoverable. Silk pattern handling
and staged generic processing recipes remain separate pending work.
Keep same-version delivery receipts distinct, preserve earlier published JARs/checksums,
install the verified JAR with backup before pushing the three owning branches.

## Contributor reconciliation before each implementation batch

Fetch the live code, Design and Docs heads before starting; inspect newly published
contributor commits and compare relevant runtime files with the installed JAR.
Do not treat Design previews, generators or progress trackers as implemented code,
and never merge Design/Docs histories into code. Carry approved runtime changes
and their matching source-generator corrections on their owning branches.
If a cited commit is not available from the verified origin or local object store,
record it as pending with its hash; do not fabricate its changes or silently restore
historical armour shells. Reconciliation on 2026-10-07 pulled the verified
95615d89/26b0ae2a Moonsteel corrections and ec74b61c/614864fa four-Sol-set shell
restoration through d50eaade; the previous accessibility deferral is superseded.
Keep the sixteen other sets vanilla-fit. Client visual approval remains separate.

## Processor card migration — 7 October

Four native processors accept Acceleration and Energy Coil cards tiers1–6, one
per family, with server-configurable caps2.5x speed/30% total-job FE saving.
The original upgrade save indices are unchanged: Acceleration first, Item Compact
second (old cooling items take-out only), Energy Coil third. Void is appended as
the fourth socket; normalize saved handler Size on load without moving old slots.
New casing/Cryo/dust upgrade insertion is
rejected; saved ingredients remain recoverable and retain their old effects only
while no card is installed. Do not compound legacy bonuses or refinery yield with
cards. Config/card changes reset paid jobs conservatively; unchanged jobs reload.
Compact capacities212/360/508/656/804/952 use separate component-aware reserves.
Never expose oversized ItemStacks. Void filters are36 saved item-type ghost
entries over four pages; only newly produced selected outputs are suppressed,
with the card installed. Existing output stacks, inputs, catalysts, fluids and
player cursor stacks are never voided. Empty/nonmatching filters still obey output
capacity. Require a live nearby menu, open Upgrades view and installed card to edit.
New external panels must override outside-click/drop handling and cancel quick-craft
distribution before copying a ghost selection. Client appearance is a separate check.
Exact survival crafting costs and additional machine contracts remain pending.
Card icons temporarily reuse existing
original filter-card artwork, not a completed unique-art rollout.

## Genetics and legacy cards — 7 October

Geno Station, Genetic Splicer, Centrifuge and Starmetal Smelter append two separate
Acceleration/Energy Coil sockets after the original machine and 36 player slots.
Never assume all addon menus have sixteen visible slots: centrifuge has seven,
smelter four. Preserve original indices, recipe dispatch and genetics outcomes.
LegacyCardJobs schedules 201 authoritative addon work calls with cumulative exact
FE rounding; its guarded recursive dispatch must bypass normal per-call charging.
Genetics uses base quarter-work units, preserves unpowered slow Geno mode and
tracks only powered units for card-adjusted FE. Card/input/config changes reset
paid progress conservatively; unchanged jobs persist. Break refunds are separate
from the sixteen original inventory slots. Compact/Void remain unsupported here.
Optional test source sets must share the common fixture directory only once.
Client socket/layout approval, dedicated icons and survival costs remain pending.

## Dedicated card artwork — 7 October

The19 upgrade-card icons now bind distinct transparent32x32 textures under
textures/item/upgrade_cards. Regenerate from Design's
docs/upgrade-card-icons/generate.py AFTER full-art-rollout-v4 and old card/model
generators; those older generators must not restore shared filter-card parents.
Tier colours copper/verdant/cyan/azure/violet/gold and six rank positions identify
tier; centre speed/coil/stack/vortex symbols identify family. Void remains un-tiered.
Do not change item IDs/effects to match artwork. Client visual approval remains separate.

## Tiered admin hub gates — 7 October

The designated planet-test-hub preset now migrates northern fixed-T6 exhibits once
to real SurvivalGateLayout tiers1–6. HubTieredGates.ADMIN is accepted only at the
six fixed Overworld controllers or their bound return platforms in that hub.
Final user choice is free ADMIN travel, not a survival progression demonstration.
Keep ordinary ownership, energy and destination restrictions outside this scope.
Use workflowHubPreset with zerog_hub_tiers for the focused test; the older full
planet audit/export assumes34 fixed outbound gates and needs topology migration
before it can certify this six-gate hub. Do not claim that legacy audit passed.
install_tiered_hub.py copies only scoped gate regions and merges the original
ledger; never replace level.dat/playerdata or test-server preparation counters.

## Compact hub / lazy planets — 7 October

New hub saves persist GateLedger.compactHub. They do not run the old 34-world
arrival/village sweep and do not force showcase/workshop/transport chunks.
Six admin gate centres are (-22/0/22,64,-22) and (-22/0/22,64,-44).
LandingPlatform is gate-footprint-only; ordinary paths and exhibit floors use
stone bricks. Do not restore giant floors or permanent chunk tickets.
Use export_compact_hub.py after the zerog_hub_tiers tests pass: export only four
bounded Overworld regions, omit all planetary terrain/test players/forced tickets,
and archive only the explicitly named former Cardinal Hub. Planets regenerate
on first actual gate visit; this is not pre-generation of all 34 destinations.
Legacy hub exports are not compatible with this contract.
Generate Docs layer plans with tools/generate_gate_build_guide.py; its mirrored
layout must be reviewed whenever SurvivalGateLayout.parts changes. Keep survival
crafting costs and unverified guardian-key activation separate from real formation.
Headless save timing is not installed-client performance approval. Measure the
next client save with tools/measure_shutdown.py and retain the 66.536-second baseline.
