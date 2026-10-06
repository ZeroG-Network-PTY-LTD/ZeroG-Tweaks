# Galaxy 4 (Eidolon) build tracker

What is left before players can reach Eidolon on a T4 gate, salvage the wrecks, climb the Salvium → Wraithsteel → Eidolite ladder, settle with the Eidolon Captain and build the T5 gate.

- **Audited against:** `1.21.x` at `5273b965` on 5 Oct 2026; updated for `15200c39` (machines and power) on 6 Oct 2026.
- **Scope:** Eidolon, wasteland slots `g4_p1` to `g4_p6`, the moon slot `g4_moons`, the T5 gate, and the Galaxy 4 gear. Reaching Galaxy 4 in survival depends on the Galaxy 2 and 3 blockers.
- **Live tracker:** the Galaxy 4 Build Tracker artifact (tick items there).
- **HTML copy:** [`galaxy4-build-tracker.html`](galaxy4-build-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.
- **Lore:** follow [`lore/README.md`](lore/README.md). Items with a **Lore** note must match it; don't invent new canon, flag gaps as "lore needed".

**14 open, 11 done.** Eidolon's frozen landscape is built: terrain, eight ores, Cryo Fluid, Hoarwood trees and the Frost Yak. The derelict fleet the planet is about is not. No wrecks generate, the wreck blocks do nothing, and the Eidolon Captain doesn't exist, so the Salvium, Wraithsteel and Palladine templates can't be found and the gear ladder stops at Skarnite.

## Lore: Act IV: The Frozen Fleet (Eidolon)

- The Concord survivors fled here and froze; the Hollow Fleet is a ghost crew waiting for a rescue that never came.
- The Eidolon Captain can be fought, or shown the crew's final log with enough Remnant Shards. Either way he yields the key, and the peaceful route gives a unique reward.
- Remnant Shards and Broken Consoles carry the fleet's story.

Rules for everything on this list:

- Keep the approved Prologue and the five acts. Don't invent new coordinates, factions, characters or registry IDs.
- Echo remembers a world only after the player reaches it. Her lines arrive as Codex pages and advancement toasts; there is no dialogue system.
- Archon Vael is the villain, always one world ahead: he appears in logs and rift whispers, and is only revealed as the Dying Star in Act V.
- The Keepers are guardian constructs still following Concord orders. Don't reveal that the Splinter creatures are the Concord before Act V.
- Put player-facing story text in lang keys (en_us.json), not hardcoded strings.

Full guide: [`lore/README.md`](lore/README.md). Don't invent new canon; flag gaps as "lore needed".

## Open: Blockers

- [ ] **Derelict wrecks on Eidolon** (Progression)
  - Wrecks are Eidolon's core content, and none generate. The Salvium, Wraithsteel, Palladine and Eidolite templates drop from the derelict_wreck chest, so the gear ladder stops at Skarnite. Build wreck structures (small and large, using Hull Plating, Corroded Hull, Broken Consoles and Cryo Pods) with chests pointing at chests/derelict_wreck. Large wrecks host the Frost Warden mini-boss.
  - **Lore:** The wrecks are the Hollow Fleet's ships: Concord survivors who fled here and froze waiting for a rescue that never came. Broken Consoles and Remnant Shards carry their memories, the main lore source of the mod.
  - Evidence: loot_table/chests/derelict_wreck.json is the only Salvium/Wraithsteel/Palladine template source; no wreck structure or feature; Hull Plating only appears in mineshaft supports (worldgen/PlanetMineshaftFeature.java)
- [ ] **Eidolon Captain boss, with the peaceful ending** (Progression)
  - Galaxy 4's guardian doesn't exist in game. Its GeckoLib model and animations are in the repo, and its loot table is ready (galaxy_5_gate_key and the Eidolite template). Act IV, The Frozen Fleet: players can fight him, or show him the crew's final log with enough Remnant Shards, and he yields the key and a unique reward.
  - **Lore:** Act IV, The Frozen Fleet: the Captain is the ghost of the fleet commander. Players can fight him, or show him the crew's final log with enough Remnant Shards; both routes give the key, and the talk-down route adds a unique reward.
  - Evidence: assets geo/eidolon_captain.geo.json; loot_table/entities/eidolon_captain.json; advancement/codex/captain.json; not in EntityInit
- [ ] **Make the Captain's key unlock the T5 gate** (Gate & travel)
  - Same gap as Galaxies 2 and 3: galaxy_5_gate_key is in the Captain's loot, but no recipe or gate check uses it. The Eidolite gate frame only needs Eidolite.
  - **Lore:** Same rule as every guardian, but the peaceful route must give the key too.
  - Evidence: loot_table/entities/eidolon_captain.json; no recipe or Java uses galaxy_5_gate_key

## Open: High

- [ ] **Eidolon mobs** (Mobs)
  - Only the Frost Yak lives here (plus Comet Blazes and glowbugs). Frost Warden (mini-boss guarding big wrecks) and Ice Leech (latches on and drains hunger, drops Leech Gel) have models and animations in the repo, so they only need registering, AI and spawns. Hollow Sentinel (haunts wrecks) comes from the Shattered Skies library and has no model here.
  - **Lore:** Hollow Sentinel haunts the wrecks (Shattered Skies roster); the Frost Warden guards the big ones. The Hollow Fleet ghosts are mournful, not hostile by default.
  - Evidence: assets geo/frost_warden, ice_leech .geo.json; biome_modifier/planet_ready_eidolon_mobs.json spawns frost_yak only
- [ ] **Broken Console, Cryo Pod and Phantom Ice behaviour** (Worlds)
  - Broken Console should give Remnant Shards and story fragments (the main lore source). Cryo Pod should hold loot. Phantom Ice should be translucent and glow faintly. All three are plain stone blocks today.
  - **Lore:** Broken Console logs are Codex content: each gives Remnant Shards and a story fragment. Story text needs approval before it ships.
  - Evidence: registry/BlockInit.java: PHANTOM_ICE, BROKEN_CONSOLE, CRYO_POD = new Block(props(STONE...))
- [ ] **Salvium, Wraithsteel and Palladine set bonuses, and Phantom Veil** (Gear)
  - Eidolite gives freeze immunity, but not the second half of Phantom Veil (invisible while sneaking). Missing: Salvium Scrapper (extra Salvium from wreck blocks), Wraithsteel Chill Guard (Slowness immunity) and Palladine Lucky (+1 Fortune and Looting).
  - Evidence: item/ZGArmorSetBonuses.java: eidolite freezing only
- [ ] **3D worn models for Salvium, Wraithsteel and Palladine armor** (Gear)
  - Eidolite uses a GeckoLib shell; the other three Eidolon sets fall back to vanilla layers.
  - Evidence: item/ZGArmorItem.java IMPLEMENTED set
- [ ] **Play the Galaxy 4 loop in a real client** (Polish)
  - Arrive on Eidolon, survive Cryo Fluid and the cold, salvage wrecks, beat or talk down the Captain, then build the T5 gate. Check gravity (0.8), the Frost Yak and the Cryo Fluid freeze on screen.
  - **Lore:** Check both Captain routes (fight and final log) and that the wrecks read as the Fleet's ships.
  - Evidence: Docs ledger: headless tests only

## Open: Normal

- [ ] **Milk the Frost Yak for Frost Milk** (Mobs)
  - Shearing works, but there is no bucket interaction. The Frost Milk food exists. The ledger also notes there is no separate shorn-body model yet.
  - Evidence: entity/FrostYak.java has shear only; item/ZGFoods.java FROST_MILK
- [ ] **Give each Eidolon biome its own features** (Worlds)
  - Frozen Graveyard, Phantom Ice Sheets and Hoarwood Taiga share one feature list. The Graveyard should hold the wrecks, the Ice Sheets should be mostly Phantom Ice with few trees, and the Taiga should be dense Hoarwood.
  - **Lore:** The Frozen Graveyard is where the Fleet's wrecks belong.
  - Evidence: worldgen/biome/frozen_graveyard.json, phantom_ice_sheets.json, hoarwood_taiga.json
- [ ] **Hollow-kin signature profession and Rimeglass trading** (Villagers)
  - Eidolon's villagers have vanilla jobs only. Add their signature profession and use Rimeglass as the trade gem. Ration Packs fit their trades.
  - **Lore:** Canon signature profession: Salvager, job site Salvage Station. The Hollow Kin are the Fleet's children, thawed first; everything they own is salvaged and their lanterns burn with the ghosts' cold light. Rimeglass is Eidolon's trade gem.
  - Evidence: registry/ZGPlanetVillagers.java THEMES eidolon=hollow_kin
- [ ] **Codex pages for Act IV (The Frozen Fleet)** (Progression)
  - Add Eidolon arrival pages, Remnant Shard fragments and the Captain's final log.
  - **Lore:** Act IV, The Frozen Fleet, and the crew's final log. Story text needs approval before it ships.
  - Evidence: item/ConcordCodexItem.java has no Eidolon pages
- [ ] **Galaxy 4 wasteland content (shared with Galaxy 2)** (Wastelands)
  - g4_p1 to g4_p6 reuse the shared wasteland biomes, so the Galaxy 2 wasteland tasks cover them. Default order here: barren, ocean, desert, volcanic, frozen, toxic; moons barren.
  - Evidence: dimension/g4_*.json; data-manifest galaxy_slots_default_type
- [ ] **Real block properties for Eidolon blocks** (Systems)
  - Permafrost, Hull Plating, Corroded Hull and the derelict blocks still use the generic stone props. Hull Plating is the mod's first metal palette, so it should sound like metal.
  - Evidence: registry/BlockInit.java generic props

## Done

- [x] **Salvage Station for wreck blocks, Wraithsteel casings and the Solar Array on Eidolon** (Machines): Once the machines exist: the Salvage Station breaks wreck blocks into Salvium and lore items, Wraithsteel is the third casing tier, Cryo Fluid is the machine coolant, and the Solar Array is weak here. Evidence: 15200c39: Salvage Station recipes for Broken Console, Corroded Hull and Cryo Pod; wraithsteel_casing tier; Solar Array x0.25 on Eidolon
- [x] **Eidolon dimension** (Worlds): Frozen Graveyard, Phantom Ice Sheets and Hoarwood Taiga, with Permafrost, Frozen Regolith and Phantom Ice in the surface rules; gravity 0.8. Evidence: dimension/eidolon.json; worldgen/noise_settings/planet/eidolon.json; ZGProgressionConfig eidolonGravity
- [x] **Eidolon terrain, plants and decor blocks** (Worlds): Permafrost, Frozen Regolith, Phantom Ice, Hull Plating, Corroded Hull, Broken Console and Cryo Pod are registered. Frostfern, Ghostbloom (Invisibility stew effect), Hoarwood trees with a full wood set, and the Spectral Lantern. Evidence: registry/BlockInit.java; worldgen hoarwood_trees, patch_frostfern, patch_ghostbloom, phantom_ice_scatter
- [x] **All eight Eidolon ores and their mining gates** (Worlds): Cryocite, Salvium, Wraithsteel, Palladine, Spectral Dust, Remnant Shard, Eidolite and Rimeglass. Salvium needs a Skarnite pick, the others need Salvium, and Eidolite needs Wraithsteel. Cryocite is a fuel. Evidence: tags/block/needs_skarnite_tool, needs_salvium_tool, needs_wraithsteel_tool; data_maps furnace_fuels; CombustionBlockEntity cryocite
- [x] **Cryo Fluid** (Worlds): Slowness II and freezing; full Eidolite armor is exempt. Water turns it into Glacial Ice and lava into Frostrock. Lakes generate on Eidolon. Evidence: registry/ZGDimensionFluids.java case cryo_fluid; worldgen lake_cryo_fluid_surface
- [x] **Frost Yak** (Mobs): Passive, with shear and regrow for Yak Wool, and spawns across Eidolon. Evidence: entity/FrostYak.java; biome_modifier/planet_ready_eidolon_mobs.json
- [x] **Galaxy 4 tool tiers and Eidolite armor** (Gear): All four Eidolon sets have real tiers and smithing recipes. Eidolite has its 3D shell and freeze immunity. Evidence: registry/ZGToolTiers.java; item/ZGArmorItem.java; ZGArmorSetBonuses.java
- [x] **T5 gate shape and cost** (Gate & travel): Eidolite ring, full arch and four energy ports; 7x7 pad for 8 players; 20M FE; reaches Galaxy 5. Evidence: travel/SurvivalGateLayout.java tier 5; ZGProgressionConfig tier5FE
- [x] **Hollow-kin villagers on Eidolon** (Villagers): The species is registered and placed in settlements. Evidence: registry/ZGPlanetVillagers.java
- [x] **Six wasteland slots and a moon** (Wastelands): g4_p1 to g4_p6 and g4_moons generate with the shared wasteland biomes and the Galaxy 4 tint. Evidence: dimension/g4_*.json; client/ZGBlockColors.java
- [x] **Act IV advancements** (Progression): Eidolon and Captain advancements exist; the Captain one can't trigger until the boss exists. Evidence: advancement/codex/eidolon.json, captain.json

## Mining ladder through Galaxy 4

| Ore | Needs | Template source | Status |
| --- | --- | --- | --- |
| Salvium | Skarnite pick | Derelict wreck | ✗ wrecks missing |
| Palladine, Remnant Shard, Rimeglass, Wraithsteel | Salvium pick | Derelict wreck | ✗ wrecks missing |
| Eidolite | Wraithsteel pick | Derelict wreck or Eidolon Captain | ✗ both missing |

