# AGENTS.md: build guide for ZeroG Tweaks

This file is for the AI coding agent (or human) turning this repo into a working mod. Read it top to bottom before writing code. The **design doc** is the source of truth for gameplay: `docs/zero-g-tweaks-bundle/ZeroG_Tweaks_Design_Doc.md`. This file tells you what already exists, what data expects from Java, and what is left to build.

## Ground rules

- **Platform:** Minecraft 1.21.1, NeoForge 21.1.x (ModDevGradle), Java 21, Parchment mappings. Mod id `zerog_tweaks`, package `net.zerog.tweaks`.
- **All logic is Java.** Don't use KubeJS or CraftTweaker.
- **Branches:**
  - `1.21.1-update` is the active line.
  - `Released` is for releases.
  - `design/v1.2-assets` receives every design/data update. Push new work there and let the owner merge.
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
| `registry/ItemInit.java` | All items. The creative tab lists every item in the namespace automatically. |
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

- [ ] Add the GeckoLib 4.x NeoForge dependency to `build.gradle`. The `dependencies {}` block is empty today; the docs Java needs GeckoLib.
- [ ] Add a `ModConfigSpec` with:
  - a global ore rarity multiplier;
  - FE costs per tier (design: 500k / 1M / 3M / 8M / 20M / 50M; +10% per passenger; 25% within a galaxy);
  - gravity overrides.
- [ ] Fix block properties. Most blocks were registered with the generic `props(STONE, 2.5F, 7.0F)`. Give each family sensible hardness, sound and map colour:
  - ores 3.0;
  - planks/wood `SoundType.WOOD`;
  - glass `SoundType.GLASS` with `noOcclusion` and a translucent/cutout render type;
  - leaves already use LeavesBlock;
  - wooden fences are already `FenceBlock`, and the sands, Rustsand, Regolith and Slag already fall like sand/gravel.
- [ ] Make `*_stairs` pass their real base block state, not `Blocks.STONE`.

### M1 Sol materials and gear

- [ ] **Tool tiers:** tools and armor are plain `Item`s today. Give each of the 20 sets its own `SimpleTier`:
  - incorrect-for tag `zerog_tweaks:incorrect_for_<set>_tool` (**new** tags);
  - strengths from the design doc Gear table.
- [ ] **Tool classes:** register `SwordItem`, `PickaxeItem`, `AxeItem`, `ShovelItem` and `HoeItem` with `Item.Properties().attributes(...)`.
- [ ] **Armor materials:** register an `ArmorMaterial` per set in `Registries.ARMOR_MATERIAL`. Use `docs/.../java/item/ZGGeoArmorItem.java` for the GeckoLib worn models.
- [ ] **Mining gates:** each planet's rare ore requires the previous tier's pickaxe. The tags `needs_<tier>_tool` already list the ores.
- [ ] **Set bonuses:** per the Gear table (Null Step, Dust Shield, Crystal Sight, Ember Walk, Phantom Veil, Starborne and the 14 metal perks). Check each tick or on equipment change.
- [ ] **Armor upgrades:** Abyssal Pearl, Heatproof Plating, Neutralizer and Grav Boots are smithing upgrades stored as a **new** data component.

### M2 Teleporter core

- [ ] **Gate multiblock:**
  - Part blocks: `gate_controller`, `gate_pad_plate`, `gate_pylon`, `gate_energy_port`, `gate_lens_housing`, `<tier>_gate_frame`.
  - Tier shapes follow the design doc's Multiblock table.
  - Ghost preview of the next tier. Breaking a part drops the gate one tier.
- [ ] **Controller:** BlockEntity + menu, FE buffer (`IEnergyStorage` capability), star-chart screen, upgrade slots (`refracting_lens`, `cryo_core`, `star_map_fragment`, `capacity_coil`).
- [ ] **Teleport:** `DimensionTransition` to `zerog_tweaks:*`. Carry players and tamed or leashed pets standing on the pad.
- [ ] **Landing platform:** generate one on first arrival (`landing_platform` + `crystal_cell`); it sends everyone home.
- [ ] **Recall and Group Anchors:** these are **new** items.

### M3 Sol dimensions

- [ ] **Gravity:** on `PlayerEvent.PlayerChangedDimensionEvent`, set the `minecraft:generic.gravity` attribute modifier from `data-manifest.json` → `planets.<id>.gravity`. Wastelands roll 0.6–1.3× from the seed.
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

- [ ] **Entities:** register the 28 entity types from `sheets/mobs/data/mobs.json` (attributes, goal order, states and mechanics are all there) with spawn placements, renderers (`docs/.../client/ZGGeoEntities.java`) and spawn eggs (`docs/.../item/ZGSpawnEggs.java`). Then move the spawn biome modifiers in.
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
5. Push to `design/v1.2-assets`, describe what changed, and note any id additions.
