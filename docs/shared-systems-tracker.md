# Shared systems tracker (pipes, bees, machines and mod-wide)

Everything that isn't tied to one galaxy: transport pipes and cells, Orbital Bees genetics and the Alveary, machines and power, storage, and mod-wide systems.

- **Audited against:** `1.21.x` at `15200c39` on 6 Oct 2026.
- **Scope:** `transport/`, `genetics/` and the aeroapiary integration, `machine/`, `power/`, `storage/`, mining rules and block properties, guide, test hub, weather, ecology, trims and compat. Per-galaxy content is in the Sol and Galaxy 2–5 trackers.
- **Live tracker:** the Shared Systems Tracker artifact (tick items there).
- **HTML copy:** [`shared-systems-tracker.html`](shared-systems-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.

**33 open, 13 done.** Transport, storage, the three processing machines, power and the core genetics and Alveary runtime all work on the server. Three things block survival play: ores drop for any tool so the mining ladder isn't enforced, the bee machines and consumables have no recipes in ZeroG Tweaks, and the Ore Refinery still runs a 5-item hardcoded table. Several bee features wait on design decisions because Productive Bees doesn't expose them.

## Open: Blockers

- [ ] **Ores drop for any tool, so the mining ladder isn't enforced** (Mining & blocks)
  - None of the blocks in BlockInit call requiresCorrectToolForDrops(), and the ore loot tables only check for Silk Touch. The needs_<tier>_tool tags make the wrong pick slow, but it still drops the ore, even by hand. That bypasses the whole Nullifite-to-Solvanite ladder in every galaxy. Add requiresCorrectToolForDrops() to the ore properties (and to stone-like blocks that should need a pickaxe). The planet mineral blocks in ZGPlanetMaterials already do this correctly.
  - Evidence: registry/BlockInit.java: props() has no requiresCorrectToolForDrops (0 uses in the file); loot_table/blocks/cerulite_ore.json only checks silk_touch; registry/ZGPlanetMaterials.java line 27 does call it
- [ ] **No crafting recipes for the bee machines, Alveary parts or genetics consumables (please confirm)** (Bees & genetics)
  - Nothing in ZeroG Tweaks has a recipe for the Genetic Splicer, Geno Station, Alveary controllers and tier parts, the Zero-G Hive, Serum Vials, Royal or Cosmic Jelly, Honey Drops or frames, and the copy of the aeroapiary addon jar available here only has Productive Bees recipes. If the current addon or the modpack adds them, tick this off; otherwise none of the bee systems can be built in survival.
  - Evidence: data/zerog_tweaks has no aeroapiary: recipes; checked addon jar data has only PB bee, breeding, produce and centrifuge recipes; current addon repo not available to check
- [ ] **Rebuild the Ore Refinery on the refining recipe type** (Machines & power)
  - The Ore Refinery is a hardcoded table of 5 inputs with no FE use, no casing or upgrade slots and no upgraded output count. The refining recipe type is registered, but the refinery doesn't use it, and the 38 refining recipe files are still in pending-data in the old format. Move it onto ProcessingBlockEntity like the other three machines and bring the recipes in.
  - Evidence: registry/OreRefineryBlockEntity.Recipes.resolve (fixed 200 ticks); no data/zerog_tweaks/recipe/refining/; Design pending-data/recipe/refining/ (38 files)

## Open: High

- [ ] **Large transport networks silently stop at 256 nodes** (Transport)
  - When a network passes 256 pipes and cells, the network search returns nothing, so items, fluids and power stop moving and the screen shows a 0 limit, with no warning. Raise or remove the cap, and warn the player if one is kept.
  - Evidence: transport/TransportBlockEntity.network(): found.size()<256 then return List.of()
- [ ] **Routing: setting only works on one node, and 'Nearest' isn't nearest** (Transport)
  - Only the node with the lowest position runs the network and uses its own routing setting, so changing Route on any other pipe does nothing. Nearest routing sorts by priority then position, not by path length as the spec says.
  - Evidence: TransportBlockEntity.tick (nodes.get(0)!=be; be.routing); endpoints.sort by priority only
- [ ] **Items jump straight to the destination and can jam a tube** (Transport)
  - Items move instantly from a tube buffer to an endpoint rather than travelling at tier speed. If nothing accepts them they sit in that tube's 9-slot buffer and can block it; the spec says they return to the source or drop. The movement renderer is a 10-tick visual pulse only.
  - Evidence: TransportBlockEntity.push()/tick; client/TransportMotionRenderer.java
- [ ] **Dangerous-fluid tier rule is only checked where fluid enters** (Transport)
  - A high-tier pull pipe can send Acid or Solar Plasma through low-tier pipes in the same network, because only the entry pipe's tier is checked. The 'can't carry this fluid' tooltip is missing too.
  - Evidence: fluidHandler().isFluidValid uses the entering block's tier; push() has no tier check; no tooltip.zerog_tweaks.transport.* in en_us.json
- [ ] **The Genetic Splicer's jelly tank can never fill** (Bees & genetics)
  - The tank only accepts fluids named *royal_jelly or *cosmic_jelly, and neither ZeroG nor the addon registers such a fluid. Either register jelly fluids or remove the tank and keep item catalysts.
  - Evidence: genetics/GeneticsTank.java; no jelly fluid registered
- [ ] **The Alveary honey tank and honey port never fill** (Bees & genetics)
  - The tank is only filled by ZeroG planet honey bottles sitting in the output slots, but Alveary outputs are combs and Productive Bees products, which never include those bottles. Nothing else fills it, so the T3 honey tank and the honey port do nothing in practice.
  - Evidence: genetics/AlvearyRuntime.collectHoney; AlvearyServiceModules only drains
- [ ] **Genetics research gating (needs a decision)** (Bees & genetics)
  - AGENTS.md says research gating exists, but the only gate is 'analyse before you sample or splice'. The spec's trait caps behind Quantum Queen Chamber research aren't built. Decide what research means (per-trait unlocks, a research item or advancements), then build it, and correct AGENTS.md meanwhile.
  - Evidence: no 'research' in src/main/java; AGENTS.md Current runtime workflow note
- [ ] **Every Alveary tier needs ZeroG ports, even T1 (confirm intended)** (Bees & genetics)
  - Formation requires exactly 2 item, 2 fluid and 1 energy port on the bottom ring at every tier. The addon has no matching ports at T1, T2 or T4, so those shells depend on ZeroG transport blocks, and the spec says T1 and T2 have no power.
  - Evidence: genetics/AlvearyFormation serviceBase
- [ ] **Alveary screen hides why the structure isn't formed** (Bees & genetics)
  - The new runtime screen only says 'Structure incomplete'. The detailed reason (for example 'Bottom ports: items 1/2') is only sent to the addon's old menu.
  - Evidence: client/AlvearyRuntimeScreen status 12; AlvearyMenuSync targets ZeroGMachineMenu only
- [ ] **Right-clicking with an item in hand may open the old addon menus (check in game)** (Bees & genetics)
  - The new genetics and Alveary menus only open with an empty hand. With an item in hand the addon's own menu likely opens: the old genetics menu has no Analyse, Sample or Splice buttons and still says 'Planned', and frames put into the old Alveary frame slots are probably ignored.
  - Evidence: GeneticsIntegration.open and AlvearyInteraction.open require an empty hand; addon block overrides useWithoutItem only; gui/machine_profiles.json
- [ ] **Planet bees can't find planet hives** (Bees & genetics)
  - No point-of-interest type is registered for the 12 planet hives, which is how vanilla bees find homes. Bees released from worldgen hives remember them, but spawned or bred glowbugs won't move in and player-placed hives won't attract bees.
  - Evidence: no PoiType for *_hive; only regolith_refiner and rust_mechanic in registry/ZGSolTrades.java
- [ ] **Bee features blocked by the Productive Bees API (needs design decisions)** (Bees & genetics)
  - Productive Bees doesn't expose these, so they need our own rules: queen lifespan, temperature, humidity and gravity tolerances, the T2 heater/fan/humidifier/dryer and T4 to T7 special parts (they count as plain shell blocks today), mutation and territory, drone breeding and fertility, and flower requirements. The screens show these as sealed or '--'.
  - Evidence: AGENTS.md known limits; AlvearyRuntime; genetics-runtime-v1 boundaries
- [ ] **Ore Refinery can be jammed by hoppers and can't be piped** (Machines & power)
  - It's a plain container with no slot rules, so hoppers can push anything into the catalyst or output slot, and it has no item capability for pipes. It also turns a Raw Nullifite block (9 raw) into only 2 ingots, and its catalyst accepts aeroapiary:stardust instead of ZeroG's stardust. Fixing the refinery blocker should cover these.
  - Evidence: registry/OreRefineryBlockEntity: no canPlaceItem or WorldlyContainer; Recipes table
- [ ] **Machine recipes can't be seen anywhere** (Compat)
  - Processing recipes are marked special, so they don't show in the recipe book, and there is no JEI or EMI plugin. Players can't find out what the Alloy Forge, Crystal Growth Chamber or Salvage Station make. Add a JEI/EMI plugin (or recipe-book categories).
  - Evidence: machine/ProcessingRecipe isSpecial()=true; no jei/emi in build.gradle or code

## Open: Normal

- [ ] **Transport visuals: dye colour, energy pulses, fluid fill, gas pipes** (Transport)
  - Painted pipes look unpainted because the colour isn't synced or tinted. Energy movement isn't drawn, fluids show as a small cube pulse, and the gas pipe family from the v2 spec doesn't exist.
  - Evidence: getUpdateTag sends motion fields only; no transport entries in ZGBlockColors; TransportMotionRenderer items and fluids only
- [ ] **Pipe hitboxes and connection updates** (Transport)
  - Pipes have full-block hitboxes, so 4 to 8 px pipes block movement and clicks like cubes. Connections only refresh every 10 ticks and freeze while redstone disables the pipe; there's no neighbour-change hook.
  - Evidence: transport/TransportBlock has no getShape; updateVisualState runs after the enabled() check
- [ ] **Cells, ports and Null Link quirks** (Transport)
  - The cell model doesn't rotate, so the output face can't be seen, and an in-place upgrade resets it. Ports are tier 0 (refuse dangerous fluids, slow item moves) and accept pipes on every face outside an Alveary. The Null Link never pushes by itself, and its owner end moves items for free.
  - Evidence: TransportRegistry add(...,0) for ports; cell blockstate keyed on level only; TransportBlockEntity remoteFactor
- [ ] **Cache transport networks and add a config** (Transport)
  - Networks are rebuilt every tick instead of cached per level and recalculated on change. Rates, the node cap, Null Link fees and buffers are hardcoded; add a transport config section.
  - Evidence: TransportBlockEntity.network() topologyTick cache only; TransportTier constants
- [ ] **Transport text and recipes polish** (Transport)
  - Screen labels and wrench/card messages are hardcoded English, and the spec's rate and mode tooltips are missing. Port recipes skip the tier-1 casing from the spec, and no recipes unlock in the recipe book.
  - Evidence: Component.literal in TransportScreen/TransportToolItem; recipe/transport/*_port.json
- [ ] **Genetics and Alveary screens to match the GUI specs** (Bees & genetics)
  - The genetics screen is 256x270 with opaque fills, no energy bar, allele bars, helix or chance badge, and its hover tooltips show traits before the bee is analysed. The Alveary runtime screen lacks the tier badge, status lamp, ledger tabs and module lamps, and uses letters for buttons. Text is hardcoded English.
  - Evidence: client/GeneticsScreen.java, client/AlvearyRuntimeScreen.java; Design docs/alveary-controller-gui-v1, orbital-bees-genetics-v1
- [ ] **Bee loose ends** (Bees & genetics)
  - Orbital-species outputs need aeroapiary bee items the addon doesn't register, so that path never runs. Planet hives have no crafting recipe and the 12 planet honeycombs have no uses. Pipes can pull silk thread back out of the Silk Weaver's input. There's no version guard on the addon, so a changed addon method crashes the game at load.
  - Evidence: AlvearyRuntime.species(); SilkWeaverRuntime; neoforge.mods.toml has no aeroapiary dependency entry; mixins required=true
- [ ] **Move combustion fuels to the data map** (Machines & power)
  - Fuels are hardcoded in CombustionBlockEntity, the pending combustion_fuels data map was never moved in, and the values differ from it. Fuel blocks such as the Nebulite block are rejected by the generator.
  - Evidence: machine/CombustionBlockEntity.burnTime; Design pending-data/data_maps/item/combustion_fuels.json
- [ ] **Configurable sides and liquids for machines** (Machines & power)
  - Processing machines use fixed faces and generators push on every side; only tanks and transport have the side panel. The design's liquids aren't used: Liquid Starlight for crystal growth, Magma Slag heat for the Alloy Forge, Solar Plasma for the Fusion Reactor. The Combustion Generator doesn't look lit when running.
  - Evidence: client/SideConfigurationPanel used by tank and transport only; combustion blockstate keyed on facing only
- [ ] **Real block properties across the mod** (Mining & blocks)
  - 570 blocks still use the generic stone properties (2.5 hardness, stone sound), including planks, casings and gate frames. The galaxy trackers list each galaxy's own blocks; this is the mod-wide pass.
  - Evidence: registry/BlockInit.java props(MapColor.STONE, SoundType.STONE, 2.5F, 7.0F)
- [ ] **Hook up villager attire** (Systems)
  - 24 villager attire types and their textures are registered, but nothing assigns them to villagers.
  - Evidence: registry/ZGVillagerAttire.TYPES is never referenced
- [ ] **Multiblock guide and test hub gaps** (Systems)
  - The multiblock guide only has Alveary layouts; add the teleporter gate tiers. The test hub aborts its whole district without the aeroapiary addon, leaves out the Ore Refinery, and its chests have nothing to test alloying, crystal growth or salvaging.
  - Evidence: assets/.../guides/multiblocks.json; travel/HubExhibits.build
- [ ] **Weather settings and permissions** (Systems)
  - The storm cycle has no server config, ambient particles default to off, /zgweather works for creative players who aren't ops, and the storm is chosen from the first player's biome only.
  - Evidence: event/PlanetStorms; ZGWeatherConfig (client only)
- [ ] **Clean up unused armor code and stale docs** (Polish)
  - ZGGeoArmorRenderer and ZGGeoArmorItem are never used and can be archived. AGENTS.md still says GeckoLib armor needs a trim layer (trims already draw through vanilla armor layers) and claims research gating exists. single-block-machines-v1/README.md still calls the machines read-only.
  - Evidence: AGENTS.md; Design docs/single-block-machines-v1/README.md
- [ ] **Create and Mekanism compat (M12)** (Compat)
  - c: ore and raw-material tags exist, but there are no Create or Mekanism recipes behind neoforge:mod_loaded conditions.
  - Evidence: no mod_loaded conditions in data/; AGENTS.md M12
- [ ] **Automated checks for transport and machines** (Polish)
  - There's no src/test. The transport spec asks for checks on conservation, unloaded chunks and mixed tiers.
  - Evidence: Design docs/transport-next-stage/README

## Done

- [x] **Six-tier transport: item tubes, fluid pipes, energy conduits and cells** (Transport): All 28 blocks and 4 tools are registered with recipes, loot, mining tags, blockstates, models and 32x32 textures. Tier materials are obtainable in survival. Mixed tiers run at the slowest tier's rate, and each fluid network carries one fluid. Evidence: transport/TransportRegistry, TransportTier, TransportBlockEntity; recipe/transport/ (47 files)
- [x] **Transport controls** (Transport): Face modes (normal, push, pull, disabled), the Flux Wrench (cycle faces, pick up with contents), redstone control, nearest/round-robin/random routing, per-face priority, item and fluid template filters, dye and cleaning, and in-place tier upgrades. Evidence: TransportBlockEntity, TransportToolItem, TransportInteraction, TransportMenu, client/TransportScreen + SideConfigurationPanel
- [x] **Null Link** (Transport): Bind with a frequency card; one shared buffer works across dimensions, with a fee that doubles between dimensions. Evidence: TransportBlockEntity remoteFactor; recipe/transport/null_link.json
- [x] **Moving items and fluids are drawn in pipes** (Transport): A short pulse follows the real route after the server completes each transfer. Evidence: client/TransportMotionRenderer.java, transport/TransportMotion.java (15200c39)
- [x] **Fluid tanks and wood storage** (Storage): Six tank tiers (5k to 5M mB) with buckets, side panel, wrench pickup, in-place upgrade and a fluid renderer. Chests, barrels, panel doors and lattice trapdoors for four woods, with a 54-slot expansion module. Evidence: storage/StorageTank*, WoodStorage*; recipe/storage/
- [x] **Alloy Forge, Crystal Growth Chamber and Salvage Station** (Machines & power): FE machines with alloying, crystal_growth and salvaging recipe types (19 recipes), casing tiers, a Cryo Core slot and energy-dust efficiency upgrades. Evidence: machine/Processing*; recipe/alloying, crystal_growth, salvaging
- [x] **Combustion Generator, Solar Array and Fusion Reactor** (Machines & power): Combustion burns coal, wood and the four planet fuels with flux module upgrades. Solar output depends on the world and weather. Fusion burns Fusion Dust at 1,000 FE/t. Evidence: machine/Combustion*; power/PowerBlockEntity, PowerConfig
- [x] **Geno Station and Genetic Splicer** (Bees & genetics): Analyse, sample and splice the five real Productive Bees traits, with FE costs and timings, jelly catalysts (75% and 100%), no partial outputs, a 4,000 mB tank and pipe access. Evidence: genetics/GeneticsRuntime, GeneticsMenu, ProductiveBeeGenes; client/GeneticsScreen
- [x] **Alveary runtime** (Bees & genetics): 27-frame storage unlocking 3/4/6/8/12/18/27 by tier, its own controller menu with paging, sort, eject and void, FE and tanks from T3, ports and service modules, shell checks, real Productive Bees production, and day/night and rain rules. Evidence: genetics/AlvearyRuntime, AlvearyFormation, AlvearyPorts, AlvearyServiceModules, AlvearyMenu
- [x] **Planet bees and hives** (Bees & genetics): 12 bee types (six glowbugs, six bees) with spawns, renderers and eggs; 12 hive families with combs, honey, fluids and buckets; natural hives generate with bees inside. Evidence: registry/ZGGlowbugs, ZGPlanetApiary; biome_modifier/*bee*, *glowbug*
- [x] **Silk Weaver** (Bees & genetics): Turns silk thread into woven silk in 200 ticks. Evidence: genetics/SilkWeaverRuntime
- [x] **Multiblock guide, test hub, weather and ecology** (Systems): 3D multiblock guide (G key) for the Alveary layouts; the admin test hub with 34 gates and exhibits; server-synced planet storms with fog, particles and lightning; six ecology worldgen features; progression, power, ecology and weather configs. Evidence: client/MultiblockGuideScreen; travel/PlanetTestHub, HubExhibits; event/PlanetStorms; registry/ZGEcologyFeatures; config/
- [x] **Armor trims** (Systems): 20 trim materials, 10 patterns and templates; all 80 armor pieces are trimmable and trims show when worn through vanilla armor layers. Evidence: data/zerog_tweaks/trim_material, trim_pattern; item/ZGArmorItem

