# Sol (Galaxy 1) build tracker

What is left before players can play the Overworld prologue, build the T1 gate and explore the Moon and Mars.

- **Audited against:** `1.21.x` at `5273b965` on 5 Oct 2026 (previous audit: `49561f7`, 4 Oct).
- **Live tracker:** the Sol Build Tracker artifact. It holds the same list, and you can tick items there.
- **Rule:** an item is done only when the code exists. Headless server tests are not client approval. Items that need an in-game look stay open until someone plays them.

**8 open, 29 done.** All five blockers and all eight high items from the first audit are now in the code. The biggest gap is a real playthrough in a client.

## Open: High

- [ ] **Play the whole Sol loop in a real client** (Polish)
  - Every Sol system now exists and passed headless server tests, but nothing has been checked on screen. In a fresh survival world: mine Nullifite, find the Courier, craft and build the T1 gate, power it with a combustion generator, go to the Moon, then Mars, loot a crash site, come home on the landing platform and with a Recall Anchor. Check menus, shift-click, worn armor, particles and gravity feel.
  - Evidence: Docs: sol-build-workflow-2026-10-05.md says client approval is pending for menus, armor fit, particles and hand models

## Open: Normal

- [ ] **Real block properties for the rest of the Sol blocks** (Systems)
  - Base Sol terrain (lunar stone, regolith, rustsand, polar frost, ice) and all 164 stair bases are fixed. 571 blocks still use the generic stone props. For Sol, fix: metal and storage blocks (Nullifite, Ferrox, Moonsteel, Olympium, Aresite, raw blocks) with SoundType.METAL; gate parts, landing platform and crystal cell; Olympium plating slab/wall; oxide crust slab/wall. Decorative stone families (polished, bricks, chiseled, cobbled) can keep stone sound but need vanilla-like hardness (1.5 / 2.0).
  - Evidence: registry/BlockInit.java: 571 x props(MapColor.STONE, SoundType.STONE, 2.5F, 7.0F); 0 stairs on Blocks.STONE
- [ ] **Check Moonsteel 3D tools in hand** (Gear)
  - Still needs an in-game look: first person, third person and item frame, both hands. The ledger lists this as client approval pending; no capture exists yet.
  - Evidence: Docs: sol-build-workflow-2026-10-05.md, Known limits
- [ ] **Launch animation and transition screen** (Polish)
  - Done: ready countdown with a ready check for everyone on the pad, and a short purple edge fade on arrival. Still missing: pylons lighting up while charging, the rift opening, players floating, the white-out and the galaxy zoom transition screen.
  - Evidence: client/GateArrivalEffects.java (32 lines, edge fade only); SurvivalGateBlockEntity countdown + ready set
- [ ] **Give Lunar Highlands its own mob spawns** (Mobs)
  - Regolith Crawler and Moon Hopper only spawn in Lunar Mare and Shadowed Craters, so the Highlands has no Moon mobs. Add one or both there (or a highlands variant).
  - Evidence: neoforge/biome_modifier/sol_regolith_crawler.json, sol_moon_hopper.json
- [ ] **Working Solar Array (strong on the Moon)** (Power)
  - The Combustion Generator is the only working Sol power. The Solar Array is still a plain block. Give it a block entity with daylight output scaled per dimension (no atmosphere on the Moon, so it is a good Sol reward; weak on Eidolon, huge on Solvane).
  - Evidence: registry/BlockInit.java: SOLAR_ARRAY = new Block(props(...)); AGENTS.md M4 unticked
- [ ] **Cinder Mite adds for the Ironfall Meteor Maw** (Mobs)
  - The Ironfall fight is designed to spawn Cinder Mites, but no Cinder Mite entity exists, so the adds are skipped. Needs a model sheet, entity and a hook in MeteorMaw.
  - Evidence: Docs ledger, Known limits; entity/MeteorMaw.java
- [ ] **Show items and fluids moving in transport lines** (Systems)
  - Transport works on the server (six tiers, filters, Null Links), but nothing is drawn moving inside the lines. Add a client renderer, using the Design transport previews.
  - Evidence: Docs ledger, Known limits; transport/TransportBlockEntity.java has no renderer

## Done

- [x] **Player-built T1 gate multiblock** (Gate & travel): travel/SurvivalGateLayout.java (tiers 1–6, 5x5 Nullifite ring, 3x3 pad, pylons, port, controller); SurvivalGateBlockEntity.preview() shows the next tier as END_ROD particles; formed tier is re-checked live, so a broken part drops the tier
- [x] **Gate Controller block entity, menu and star chart** (Gate & travel): travel/SurvivalGateBlockEntity.java + SurvivalGateMenu + client/SurvivalGateScreen: owner lock, FE buffer (2x tier cost), star chart filtered by tier, 4 upgrade slots; costs from config/ZGProgressionConfig.java (500k/1M/3M/8M/20M/50M)
- [x] **Landing platform on first arrival, and the trip home** (Gate & travel): SurvivalGateBlockEntity: first survival arrival builds a return platform with a crystal_cell (+1,000 FE trickle) routed to the home controller
- [x] **Mars Crash Site structure** (Progression): worldgen/structure/mars_crash_site.json + structure_set; structure/mars_crash_site/wreck_a.nbt and wreck_b.nbt chests use chests/mars_crash_site
- [x] **A Sol-era way to make 500k FE** (Power): machine/CombustionBlockEntity.java burns coal/charcoal (1,600 ticks) at 50 FE/t, about 80k FE per coal, so a T1 jump is roughly 6–7 coal
- [x] **Planet gravity (Moon 0.5, Mars 0.7)** (Worlds): event/PlanetGravity.java; values in ZGProgressionConfig (Moon 0.5, Mars 0.7, configurable); cleared on return
- [x] **Register Regolith Crawler and Moon Hopper** (Mobs): entity/RegolithCrawler.java, MoonHopper.java; biome_modifier/sol_regolith_crawler.json and sol_moon_hopper.json (Lunar Mare and Shadowed Craters)
- [x] **Register Dust Grazer on Mars** (Mobs): entity/DustGrazer.java; biome_modifier/sol_dust_grazer.json (Rust Plains, Oxide Badlands, Polar Caps)
- [x] **Meteor Maw (Ironfall) during Moon meteor events** (Mobs): entity/MeteorMaw.java (Ironfall, leap/slam and heat pulse), spawned by event/DailyPlanetImpacts.java; built into ZeroG Tweaks instead of the Shattered Skies library. Its Cinder Mite adds are a separate open task.
- [x] **Olympium 3D armor and Dust Shield set bonus** (Gear): Olympium GeckoLib shell; ZGArmorSetBonuses.dustProtected() hides Mars dust and vortex effects. Dust storms are visual only today, so the bonus is visual only too.
- [x] **Polar Frost hazard** (Worlds): worldgen/PolarFrostBlock.java: Slowness while standing on it, no damage or freezing (matches the agreed non-damaging rule)
- [x] **Recall Anchor item** (Gate & travel): item/RecallAnchorItem.java, registered in travel/SurvivalGates.java with Group Anchor; recipes recall_anchor.json, group_anchor.json; cooldown in config
- [x] **Null Fluid pools in the Overworld Deep Dark** (Worlds): neoforge/biome_modifier/deep_dark_null_fluid.json (pools with deepslate lining)
- [x] **Give each Moon and Mars biome its own features** (Worlds): worldgen/SolBiomeSignatureFeature.java, added to all six Moon and Mars biomes
- [x] **Lunari and Rustborn signature professions** (Villagers): registry/ZGSolTrades.java: regolith_refiner (Ore Refinery) and rust_mechanic (Combustion Generator) POIs, professions and trades; SettlementAnchorBlockEntity places both job sites
- [x] **Aresite core shrine in Rustborn villages** (Progression): worldgen/structure/mars_aresite_shrine.json + structure/mars_aresite_shrine/shrine.nbt
- [x] **T2 gate upgrade (leave Sol)** (Gate & travel): SurvivalGateLayout tier 2: Moonsteel ring, arch, lens housing, Selenite and Aresite blocks; canReach() opens Galaxy 2 at T2
- [x] **Main config file** (Systems): config/ZGProgressionConfig.java (COMMON): oreRarityMultiplier (used by ConfiguredPlanetOreFeature), tier FE costs, six gravity values, recall cooldown
- [x] **Codex pages for the Moon and Mars** (Progression): item/ConcordCodexItem.java: zerog_codex_moon and zerog_codex_mars pages unlock on arrival
- [x] **Update the AGENTS.md milestone checkboxes** (Polish): AGENTS.md M0–M3 ticked in 01ec5d9f; set bonuses, armor upgrades, hazards and Solar Array are correctly still open
- [x] **Signal prologue: Courier pod, Dormant Wisp, Codex** (Progression): lore/ConcordPrologue.java, structure/concord_courier.nbt
- [x] **Nullifite ore in deepslate and the Deep Dark** (Worlds): neoforge/biome_modifier/add_nullifite_ore*.json
- [x] **Sol tool tiers and mining ladder** (Gear): registry/ZGToolTiers.java, ItemInit.java, tags/block/needs_*
- [x] **Nullifite, Ferrox and Moonsteel armor with set bonuses** (Gear): item/ZGArmorItem.java, ZGArmorSetBonuses.java
- [x] **Moon and Mars dimensions with ores and surfaces** (Worlds): dimension/moon.json, mars.json; worldgen/noise_settings
- [x] **Lunari and Rustborn villagers in settlements** (Villagers): registry/ZGPlanetVillagers.java; biome_modifier/planet_settlements.json
- [x] **Rust Beetle on Mars** (Mobs): entity/RustBeetle.java
- [x] **Upgrade templates and copy recipes** (Progression): registry/ZGUpgradeTemplates.java
- [x] **Act I Codex advancements** (Progression): advancement/codex/*.json

## Not Sol (left for later galaxies)

- Armor upgrades: Abyssal Pearl, Heatproof Plating, Neutralizer and Grav Boots.
- Surface hazards: Ember and Corona Crust, Flare Vent, Vent Rock and Glacial Ice.
- Set bonuses for the Galaxy 2–5 sets.
- Frost Yak shorn model.
- Hidden-world pool for the Star Map Fragment.
