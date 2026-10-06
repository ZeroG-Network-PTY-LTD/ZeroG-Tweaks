# Sol (Galaxy 1) build tracker

What is left before players can play the Overworld prologue, build the T1 gate and explore the Moon and Mars.

- **Audited against:** `1.21.x` at `ba544335` on 6 Oct 2026 (first audit `5273b965`).
- **Scope:** The Overworld prologue, the Moon, Mars, the T1 and T2 gates, and Sol-era power and gear.
- **Live tracker:** the Sol Build Tracker artifact (tick items there).
- **HTML copy:** [`sol-build-tracker.html`](sol-build-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.
- **Lore:** follow [`lore/README.md`](lore/README.md). Items with a **Lore** note must match it; don't invent new canon, flag gaps as "lore needed".

**8 open, 34 done.** The Rustborn shrine is checked across all four settlement layouts. Moon/Mars Codex localization preserves approved wording and passes item-use arrival, return and player save/reload checks in loaded planetary levels. Still open: real-client playthrough, mob rendering and polish. Moon impact-wreck debris remains deferred; Star Map Fragments are the interim lore carrier. Server checks do not certify client appearance or physical portal travel.

## Lore: Prologue: The Signal, and Act I: The Falling Star

- Earth was meant to be the Concord's refuge. Their Pathfinder ship crashed deep in its rock, and its shattered gate core became Nullifite.
- First Raw Nullifite pickup makes the Moon relay answer: a Courier Pod lands the next night with Echo's Dormant Wisp, the Concord Codex and a Broken Console ("Refuge signal received. Courier dispatched. Rebuild the gate. We are waiting.").
- The Gate Controller is built around the Dormant Wisp. Echo wakes asking "How long have I been asleep?" and remembers only the Moon relay and the Mars waystation, so T1 reaches only those two.
- On the Moon, the Lunari greet "the one who answered the signal". Meteor Maws bring Concord debris to the Moon. On Mars, the Rustborn's hand-cut Aresite core is the first proof the Concord was real.

Rules for everything on this list:

- Keep the approved Prologue and the five acts. Don't invent new coordinates, factions, characters or registry IDs.
- Echo remembers a world only after the player reaches it. Her lines arrive as Codex pages and advancement toasts; there is no dialogue system.
- Archon Vael is the villain, always one world ahead: he appears in logs and rift whispers, and is only revealed as the Dying Star in Act V.
- The Keepers are guardian constructs still following Concord orders. Don't reveal that the Splinter creatures are the Concord before Act V.
- Put player-facing story text in lang keys (en_us.json), not hardcoded strings.

Full guide: [`lore/README.md`](lore/README.md). Don't invent new canon; flag gaps as "lore needed".

## Open: High

- [ ] **Play the whole Sol loop in a real client** (Polish)
  - Every Sol system now exists and passed headless server tests, but nothing has been checked on screen. In a fresh survival world: mine Nullifite, find the Courier, craft and build the T1 gate, power it with a combustion generator, go to the Moon, then Mars, loot a crash site, come home on the landing platform and with a Recall Anchor. Check menus, shift-click, worn armor, particles and gravity feel.
  - **Lore:** Check the Prologue and Act I beats in order: first Raw Nullifite, then the Courier the next night (backup pod after 7 days), then Echo's Dormant Wisp inside the Gate Controller and her "How long have I been asleep?". T1 must only reach the Moon and Mars, because that is all Echo remembers. The Lunari should treat the player as "the one who answered the signal", and the Rustborn should keep their Aresite core shrine.
  - Evidence: Docs: sol-build-workflow-2026-10-05.md says client approval is pending for menus, armor fit, particles and hand models
- [ ] **Confirm Moon and Mars mobs no longer render solid black** (Mobs)
  - Rust Beetles, Dune Burrowers, Dust Grazers and the Moon Hopper showed up as solid-black silhouettes in a real client. The likely cause (a glow pass on mobs that have no glow texture) was patched in ba544335 and the fixed JAR is installed, but nobody has looked yet. Restart the client and check those four with shaders off and on, adults and babies, plus one mob that should glow.
  - Evidence: 1.21.x ba544335 client/OptionalGlowingGeoLayer.java; Docs: black-mob-rendering-hotfix-2026-10-07.md (client confirmation pending)

## Open: Normal

- [ ] **Real block properties for the rest of the Sol blocks** (Systems)
  - Base Sol terrain (lunar stone, regolith, rustsand, polar frost, ice), all 164 stair bases and the ores are fixed. Still on the generic stone props (2.5 hardness, stone sound): the Nullifite, Ferrox, Moonsteel, Olympium and Aresite blocks and raw blocks (should be metal sound), gate parts, landing platform and crystal cell, Olympium plating slab/wall, oxide crust slab/wall, and the decorative stone families (polished, bricks, chiseled, cobbled), which need vanilla-like hardness.
  - Evidence: registry/BlockInit.java at ba544335: 570 x props(MapColor.STONE, SoundType.STONE, 2.5F, 7.0F), e.g. MOONSTEEL_BLOCK, GATE_PYLON, LANDING_PLATFORM, CRYSTAL_CELL, LUNAR_STONE_BRICKS
- [ ] **Check Moonsteel 3D tools in hand** (Gear)
  - Still needs an in-game look: first person, third person and item frame, both hands. The ledger lists this as client approval pending; no capture exists yet.
  - Evidence: Docs: sol-build-workflow-2026-10-05.md, Known limits
- [ ] **Launch animation and transition screen** (Polish)
  - Done: ready countdown with a ready check for everyone on the pad, and a short purple edge fade on arrival. Still missing in code: pylons lighting up while charging, the rift opening, players floating, the white-out and the galaxy-to-planet transition screen. The transition screen's design and art are ready on Design (docs/gate-transition-screen-v1): spec, timings, layout, sprites and previews.
  - **Lore:** The gate is rebuilt Concord tech built around Echo's wisp. Echo only remembers a world after the player reaches it, so on a first trip her lines must not describe the destination. The Echo lines in the transition-screen previews are placeholders, not canon. Story text needs approval before it ships.
  - Evidence: client/GateArrivalEffects.java (edge fade only); Design: docs/gate-transition-screen-v1/README.md
- [ ] **Give Lunar Highlands its own mob spawns** (Mobs)
  - Regolith Crawler and Moon Hopper only spawn in Lunar Mare and Shadowed Craters, so the Highlands has no Moon mobs. Add one or both there (or a highlands variant).
  - **Lore:** Keep to the Act I cast: Regolith Crawler and Moon Hopper (plus Meteor Maws during impacts). Don't add a new Moon species without approval.
  - Evidence: neoforge/biome_modifier/sol_regolith_crawler.json, sol_moon_hopper.json
- [ ] **Cinder Mite adds for the Ironfall Meteor Maw** (Mobs)
  - The Ironfall fight is designed to spawn Cinder Mites, but no Cinder Mite entity exists, so the adds are skipped. Needs a model sheet, entity and a hook in MeteorMaw.
  - **Lore:** Act I says Meteor Maws carry Concord debris to the Moon. Cinder Mites have no written origin yet; ask before deciding what they are. Keep them wildlife, not Concord or Splinter creatures.
  - Evidence: Docs ledger, Known limits; entity/MeteorMaw.java
- [ ] **Meteor Maws should carry Concord debris (lore gap)** (Progression)
  - Owner decision7Oct2026: keep the existing Star Map Fragment drop as an interim lore carrier. Future small Moon impact wrecks may use approved crater, meteorite fragments, pod-shell and chest pieces, without a Wisp, Codex or Broken Console. Wreck implementation remains pending and does not block Sol progression.
  - **Lore:** Preserve Broken Consoles for the Courier and Eidolon story moments; no whole-console mob drop. Act I debris should read as an impact-site remnant.
  - Evidence: loot_table/entities/meteor_maw.json only has star_map_fragment; event/DailyPlanetImpacts.java places no Concord material
- [x] **Put an Aresite core shrine in every Rustborn village** (Villagers)
  - Each newly generated Rustborn layout places one hand-cut Aresite core on a low Martian brick pedestal, clear of homes, farms and the resident anchor. The standalone large shrine and its loot remain unchanged; existing villages are not retrofitted.
  - **Lore:** Rustborn are the first people who remember the Concord by name; the hand-cut Aresite core in every village is the first proof the Concord was real.
  - Evidence: worldgen/PlanetSettlementFeature.java and SolLoreGameTests actual four-layout construction; same-version shrine JAR installed7October2026. Client composition approval remains pending.
- [x] **Move the Moon and Mars Codex pages into lang keys** (Progression)
  - Act I Moon and Mars pages now use language keys alongside the three Prologue pages. The approved English wording is unchanged.
  - **Lore:** Story text goes in en_us.json. Keep the approved wording: the Lunari relay listened for the Pathfinder's hum for thousands of years; the Rustborn's hand-cut Aresite core is the first proof of the Concord.
  - Evidence: item/ConcordCodexItem.java uses codex.zerog_tweaks.moon_relay/mars_waystation from lang/en_us.json; all2 required lore tests passed20261006_234711 in actual loaded Moon/Mars levels, including no premature pages, Mars-first unlock, return and player save/reload.

## Done

- [x] **Player-built T1 gate multiblock** (Gate & travel): 5x5 Nullifite frame, 3x3 pad, 4 short pylons, 1 energy port and the controller, with formation check and ghost preview of the next tier. Right now the only gate is an admin-built T6 test layout, so survival players cannot leave the Overworld. Evidence: travel/SurvivalGateLayout.java (tiers 1–6, 5x5 Nullifite ring, 3x3 pad, pylons, port, controller); SurvivalGateBlockEntity.preview() shows the next tier as END_ROD particles; formed tier is re-checked live, so a broken part drops the tier
- [x] **Gate Controller block entity, menu and star chart** (Gate & travel): FE buffer, star-chart screen that lists only what the tier reaches (T1: Moon and Mars by catalog name), upgrade slot. Per-tier costs from the design: T1 500k FE, 25% inside a galaxy, +10% per passenger. The ledger uses a flat 50M FE cost and capacity for every jump. Evidence: travel/SurvivalGateBlockEntity.java + SurvivalGateMenu + client/SurvivalGateScreen: owner lock, FE buffer (2x tier cost), star chart filtered by tier, 4 upgrade slots; costs from config/ZGProgressionConfig.java (500k/1M/3M/8M/20M/50M)
- [x] **Landing platform on first arrival, and the trip home** (Gate & travel): Generate landing_platform + crystal_cell the first time a player arrives on a planet; it charges slowly and sends everyone on it home. Today platforms are only built by the test hub. Evidence: SurvivalGateBlockEntity: first survival arrival builds a return platform with a crystal_cell (+1,000 FE trickle) routed to the home controller
- [x] **Mars Crash Site structure** (Progression): The Ferrox, Moonsteel and Olympium upgrade templates only drop from the Mars Crash Site chest, and the structure does not exist, so Sol gear progression stops after Nullifite. Build the jigsaw structure on Mars and point its chests at chests/mars_crash_site. Evidence: worldgen/structure/mars_crash_site.json + structure_set; structure/mars_crash_site/wreck_a.nbt and wreck_b.nbt chests use chests/mars_crash_site
- [x] **A Sol-era way to make 500k FE** (Power): The T1 jump needs FE, but the Combustion Generator is a plain block with no block entity, and the design's fuels start in Galaxy 2. Either make the Combustion Generator burn coal and charcoal in the Overworld, or decide the pack relies on other mods' generators and say so. Evidence: machine/CombustionBlockEntity.java burns coal/charcoal (1,600 ticks) at 50 FE/t, about 80k FE per coal, so a T1 jump is roughly 6–7 coal
- [x] **Planet gravity (Moon 0.5, Mars 0.7)** (Worlds): Set the generic.gravity attribute modifier on dimension change from data-manifest planets.<id>.gravity, and clear it on the way home. No gravity code exists yet. Evidence: event/PlanetGravity.java; values in ZGProgressionConfig (Moon 0.5, Mars 0.7, configurable); cleared on return
- [x] **Register Regolith Crawler and Moon Hopper** (Mobs): The Moon's threat and ambient mob. Models, textures and animations are in the repo; the entity types are not registered. Then replace the Dune Burrower placeholder in the Moon spawn list. Evidence: entity/RegolithCrawler.java, MoonHopper.java; biome_modifier/sol_regolith_crawler.json and sol_moon_hopper.json (Lunar Mare and Shadowed Craters)
- [x] **Register Dust Grazer on Mars** (Mobs): Mars's passive mob (Rust Beetle is already done). Model is in the repo; add the entity, AI and spawns in Rust Plains and Oxide Badlands. Evidence: entity/DustGrazer.java; biome_modifier/sol_dust_grazer.json (Rust Plains, Oxide Badlands, Polar Caps)
- [x] **Meteor Maw (Ironfall) during Moon meteor events** (Mobs): Act I has Meteor Maws carrying Concord debris to the Moon. It comes from the Shattered Skies mob library: add that dependency or a biome modifier that references its ids, and hook it to the existing daily impacts. Lore: Act I: Meteor Maws bring Concord debris to the Moon. What that debris is (item, drop or impact structure) still needs approved lore. Evidence: entity/MeteorMaw.java (Ironfall, leap/slam and heat pulse), spawned by event/DailyPlanetImpacts.java; built into ZeroG Tweaks instead of the Shattered Skies library. Its Cinder Mite adds are a separate open task.
- [x] **Olympium 3D armor and Dust Shield set bonus** (Gear): Olympium is the only Sol set without a GeckoLib worn model or its perk (Dust Shield: immune to storm and dust effects). Nullifite, Ferrox and Moonsteel are done. Evidence: Olympium GeckoLib shell; ZGArmorSetBonuses.dustProtected() hides Mars dust and vortex effects. Dust storms are visual only today, so the bonus is visual only too.
- [x] **Polar Frost hazard** (Worlds): Design: dry-ice caps that slow and chill. It is a plain stone-like block today. Add slowness/freezing like powder snow (no damage), using the polar_frost damage type only for long exposure. Evidence: worldgen/PolarFrostBlock.java: Slowness while standing on it, no damage or freezing (matches the agreed non-damaging rule)
- [x] **Recall Anchor item** (Gate & travel): Bound to the home gate; pulls the holder home from the home buffer with a cooldown and extra cost. New id. (Group Anchor can wait for a later tier.) Evidence: item/RecallAnchorItem.java, registered in travel/SurvivalGates.java with Group Anchor; recipes recall_anchor.json, group_anchor.json; cooldown in config
- [x] **Null Fluid pools in the Overworld Deep Dark** (Worlds): The design's early Nullifite hint: small Null Fluid pools near ancient cities. Only the Moon's surface lakes exist. Add a placed feature and a biome modifier for minecraft:deep_dark. Evidence: neoforge/biome_modifier/deep_dark_null_fluid.json (pools with deepslate lining)
- [x] **Give each Moon and Mars biome its own features** (Worlds): All three Moon biomes share one feature list, and so do all three Mars biomes; only the surface rules differ. Add per-biome features (crater ice pockets in Shadowed Craters, basalt flows on the Mare, frost spires on the Polar Caps, oxide spires in the Badlands). Evidence: worldgen/SolBiomeSignatureFeature.java, added to all six Moon and Mars biomes
- [x] **Lunari and Rustborn signature professions** (Villagers): Both species spawn in settlements with vanilla professions only. Add Regolith Refiner (job site: Ore Refinery) and Rust Mechanic (job site: Combustion Generator) with the trades from the villager sheets. Lore: Regolith Refiner (Lunari) and Rust Mechanic (Rustborn) are the canon signature professions. Evidence: registry/ZGSolTrades.java: regolith_refiner (Ore Refinery) and rust_mechanic (Combustion Generator) POIs, professions and trades; SettlementAnchorBlockEntity places both job sites
- [x] **Aresite core shrine in Rustborn villages** (Progression): The Mars beat of Act I: a hand-cut Aresite core kept as a shrine, so the Mars advancement has a place to happen. Lore: The hand-cut Aresite core is the first proof that the Concord was real; every Rustborn village keeps one as a shrine. Evidence: worldgen/structure/mars_aresite_shrine.json + structure/mars_aresite_shrine/shrine.nbt
- [x] **T2 gate upgrade (leave Sol)** (Gate & travel): Moonsteel ring, low arch and Selenite lens on top of the T1 core; unlocks Galaxy 2 on the star chart. Needs the tier logic from the T1 work. Evidence: SurvivalGateLayout tier 2: Moonsteel ring, arch, lens housing, Selenite and Aresite blocks; canReach() opens Galaxy 2 at T2
- [x] **Main config file** (Systems): ModConfigSpec with the ore rarity multiplier, FE cost per gate tier and gravity overrides. Only weather and ecology configs exist. Evidence: config/ZGProgressionConfig.java (COMMON): oreRarityMultiplier (used by ConfiguredPlanetOreFeature), tier FE costs, six gravity values, recall cooldown
- [x] **Codex pages for the Moon and Mars** (Progression): The Codex has three prologue pages. Add Act I pages that unlock on arrival (Echo remembers the Moon relay, then the Mars waystation). Lore: Codex pages are Echo's voice. Act I pages: the Moon relay listened for the Pathfinder's hum for thousands of years; the Mars waystation and its Aresite core. Evidence: item/ConcordCodexItem.java: zerog_codex_moon and zerog_codex_mars pages unlock on arrival
- [x] **Update the AGENTS.md milestone checkboxes** (Polish): Several finished items are still unticked (GeckoLib, tool tiers, armor materials, set bonuses), which misleads the next agent. Evidence: AGENTS.md M0–M3 ticked in 01ec5d9f; set bonuses, armor upgrades, hazards and Solar Array are correctly still open
- [x] **Working Solar Array (strong on the Moon)** (Power): The Combustion Generator is the only working Sol power. The Solar Array is still a plain block. Give it a block entity with daylight output scaled per dimension (no atmosphere on the Moon, so it is a good Sol reward; weak on Eidolon, huge on Solvane). Evidence: 15200c39: power/PowerBlockEntity.java + PowerConfig: 20 FE/t base in daylight, x2 on the Moon, x0.25 on Eidolon, x8 on Solvane, x0.25 in rain
- [x] **Show items and fluids moving in transport lines** (Systems): Transport works on the server (six tiers, filters, Null Links), but nothing is drawn moving inside the lines. Add a client renderer, using the Design transport previews. Evidence: 15200c39: client/TransportMotionRenderer.java + transport/TransportMotion.java draw content moving along real routes; on-screen check is part of the client playtest
- [x] **Signal prologue: Courier pod, Dormant Wisp, Codex** (Progression): First Raw Nullifite triggers the Courier; its chest holds the Dormant Wisp and Concord Codex; backup Wisp in loot. Lore: Built to the approved Prologue (briefs/prologue_the_signal.md). Don't change the Courier, Wisp or console text without approval. Evidence: lore/ConcordPrologue.java, structure/concord_courier.nbt
- [x] **Nullifite ore in deepslate and the Deep Dark** (Worlds): Biome modifiers add the ore, with extra in the Deep Dark. Evidence: neoforge/biome_modifier/add_nullifite_ore*.json
- [x] **Sol tool tiers and mining ladder** (Gear): Nullifite, Ferrox, Moonsteel and Olympium tiers; real sword/pickaxe/axe/shovel/hoe classes; needs_ and incorrect_for_ tags. Since d659d926 all 39 ores require the correct tool, so the wrong pick no longer drops Moonsteel, Olympium, Aresite or Selenite. Evidence: registry/ZGToolTiers.java, ItemInit.java, tags/block/needs_*; BlockInit.java ores use requiresCorrectToolForDrops() (d659d926)
- [x] **Nullifite, Ferrox and Moonsteel armor with set bonuses** (Gear): GeckoLib worn models and perks (Null Step, Sturdy, Lunar Stride). Evidence: item/ZGArmorItem.java, ZGArmorSetBonuses.java
- [x] **Moon and Mars dimensions with ores and surfaces** (Worlds): Three biomes each, planet ores, lichen, Moon Null Fluid lakes, surface blocks via noise rules. Evidence: dimension/moon.json, mars.json; worldgen/noise_settings
- [x] **Lunari and Rustborn villagers in settlements** (Villagers): Species registered with renderers; settlements placed on Moon and Mars biomes. Lore: Lunari are the stay-behinds who watch the Moon relay; Rustborn are the families who stayed to work the Olympium seams. See the peoples table in lore/README.md. Evidence: registry/ZGPlanetVillagers.java; biome_modifier/planet_settlements.json
- [x] **Rust Beetle on Mars** (Mobs): Registered with AI and spawns. Evidence: entity/RustBeetle.java
- [x] **Upgrade templates and copy recipes** (Progression): Template items and duplication recipes exist (but see the Mars Crash Site blocker). Evidence: registry/ZGUpgradeTemplates.java
- [x] **Act I Codex advancements** (Progression): Root, Falling Star, Builder's Template, First Gate, The Moon, Mars, Aresite Core, Null Step. Evidence: advancement/codex/*.json
- [x] **Sol story beats in the game** (Progression): Checked against the approved Prologue and Act I: first Raw Nullifite schedules the Courier for the next night, with a second pod after 7 days and a Dormant Wisp backup in ancient-city chests. The console says 'Rebuild the gate. We are waiting.' The Gate Controller needs the Dormant Wisp, and Echo asks 'How long have I been asleep?'. T1 only reaches the Moon and Mars. The Lunari greet 'the one who answered the signal' on arrival, and the Codex has the Signal, Builder's Template and Awaiting Coordinates pages. Lore: Matches briefs/prologue_the_signal.md and the Act I lore. Evidence: lore/ConcordPrologue.java (RECOVERY_TICKS=7*24000, ancient_city backup pool, lunari_signal_greeting); recipe/gate_controller.json needs dormant_wisp; lang codex.zerog_tweaks.*

## Not Sol (left for later galaxies)

- Armor upgrades: Abyssal Pearl, Heatproof Plating, Neutralizer and Grav Boots.
- Surface hazards: Ember and Corona Crust, Flare Vent, Vent Rock and Glacial Ice.
- Set bonuses for the Galaxy 2–5 sets.
- Frost Yak shorn model.
- Hidden-world pool for the Star Map Fragment.
