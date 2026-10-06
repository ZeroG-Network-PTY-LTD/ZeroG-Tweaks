# Galaxy 3 (Skarn) build tracker

What is left before players can reach Skarn on a T3 gate, climb the Ruskite → Tectium → Skarnite ladder, beat the Rift Tyrant, explore the six wasteland slots and build the T4 gate.

- **Audited against:** `1.21.x` at `5273b965` on 5 Oct 2026; updated for `15200c39` (machines and power) on 6 Oct 2026.
- **Scope:** Skarn, wasteland slots `g3_p1` to `g3_p6`, the moon slot `g3_moons`, the T4 gate, and the Galaxy 3 gear. Galaxy 3 can only be reached once the Galaxy 2 blockers are fixed.
- **Live tracker:** the Galaxy 3 Build Tracker artifact (tick items there).
- **HTML copy:** [`galaxy3-build-tracker.html`](galaxy3-build-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.
- **Lore:** follow [`lore/README.md`](lore/README.md). Items with a **Lore** note must match it; don't invent new canon, flag gaps as "lore needed".

**15 open, 9 done.** Skarn's world is built: terrain, ores, Magma Slag, plants and trees. Nothing lives there yet. There are no Skarn mobs and no Rift Tyrant. The Ruskite, Tectium and Pyrium templates can't be found, so the gear ladder stops at Cerulite. One design question is open: whether Ember Crust should actually hurt.

## Lore: Act III: The Wound (Skarn)

- Skarn is where Vael tore space open.
- The Rift Tyrant is his lieutenant, fused into the rift; the fight pulls pieces of the arena into the void.
- After the Tyrant, Echo remembers she plotted the course here. Side quest: the Collapsed Forge, home of the smith who built the first gate.

Rules for everything on this list:

- Keep the approved Prologue and the five acts. Don't invent new coordinates, factions, characters or registry IDs.
- Echo remembers a world only after the player reaches it. Her lines arrive as Codex pages and advancement toasts; there is no dialogue system.
- Archon Vael is the villain, always one world ahead: he appears in logs and rift whispers, and is only revealed as the Dying Star in Act V.
- The Keepers are guardian constructs still following Concord orders. Don't reveal that the Splinter creatures are the Concord before Act V.
- Put player-facing story text in lang keys (en_us.json), not hardcoded strings.

Full guide: [`lore/README.md`](lore/README.md). Don't invent new canon; flag gaps as "lore needed".

## Open: Blockers

- [ ] **Rift Tyrant boss and arena** (Progression)
  - Galaxy 3's guardian doesn't exist in game. Its GeckoLib model, aura and animations are in the repo, and its loot table is ready (galaxy_4_gate_key and the Skarnite template). Missing: the entity, its AI and phases, the arena and how players find it. Act III, The Wound: Vael's lieutenant, fused into the rift, pulls pieces of the arena into the void. The Prism Sentinel's arena and Concord Prism controller are the pattern to follow.
  - **Lore:** Act III, The Wound: the Tyrant is Vael's lieutenant fused into the rift and pulls pieces of the arena into the void. Afterwards Echo remembers she plotted the course here. Vael himself only appears as rift whispers and logs.
  - Evidence: assets geo/rift_tyrant.geo.json and animations; loot_table/entities/rift_tyrant.json; no entity in EntityInit; no arena in worldgen/structure
- [ ] **Make the Ruskite, Tectium, Pyrium and Skarnite templates obtainable** (Progression)
  - Ruskite, Tectium and Pyrium templates only drop from the Collapsed Forge, which doesn't exist. Skarnite drops from the Collapsed Forge and the Rift Tyrant, and neither exists. Players can't go from Cerulite to Ruskite, can't mine Skarnite (Tectium pick), and can't build the T4 gate. This is the same problem as Galaxy 2. Build the Collapsed Forge (a volcanic-wasteland structure), or add the templates to Skarn loot in the meantime.
  - **Lore:** The Collapsed Forge is the approved side quest of the smith who built the first gate, and the Ashwrights descend from the Concord smiths. Their forge is the natural home for the Skarn templates.
  - Evidence: loot_table/chests/collapsed_forge.json and entities/rift_tyrant.json are the only sources; tags/block/needs_tectium_tool lists skarnite_ore
- [ ] **Make the Rift Tyrant's key unlock the T4 gate** (Gate & travel)
  - Same gap as Galaxy 2: galaxy_4_gate_key is in the Tyrant's loot, but no recipe or gate check uses it. The Skarnite gate frame only needs Skarnite. Fix both keys the same way.
  - **Lore:** Same rule as every guardian: the boss's defeat unlocks the next gate tier.
  - Evidence: loot_table/entities/rift_tyrant.json; no recipe or Java uses galaxy_4_gate_key

## Open: High

- [ ] **Skarn mobs** (Mobs)
  - Skarn has no mobs of its own. Its biomes spawn Rust Beetle as a placeholder, plus Void-C Blazes and glowbugs. Cinder Hound (packs on Ember Crust), Slag Boar (neutral, drops Boar Chop and Tusk) and Scorch Wyrmling (spits fire bolts, drops Scorch Tail and Scale) already have models and animations, so they only need registering, AI and spawns. Slagjaw and Shardmother come from the Shattered Skies library and have no models here yet. The food items already exist.
  - **Lore:** Canon roles: Slagjaw is a stone golem with ore teeth; Shardmother is a broodmother in rift zones; Cinder Hounds hunt in packs on Ember Crust. Rift-zone mobs should feel tied to Vael's tear.
  - Evidence: assets geo/cinder_hound, slag_boar, scorch_wyrmling .geo.json; registry/EntityInit.java has none; biome_modifier/planet_ready_skarn_mobs.json spawns rust_beetle
- [ ] **Ember Crust hazard (needs your call)** (Worlds)
  - The design says Ember Crust hurts to stand on, like magma, and Skarnite armor's Ember Walk makes you safe on it. It is a plain stone block today. This clashes with the agreed rule that environmental effects start non-damaging, so decide: real magma-style damage, or something softer such as setting you alight briefly or Slowness. Magma Slag already burns and damages.
  - **Lore:** Skarn is the hostile world, and the design's hazard gate says its burning ground needs fire protection (Skarnite's Ember Walk).
  - Evidence: BlockInit.java: EMBER_CRUST = new Block(props(STONE...)); ZGDimensionFluids case magma_slag ignites and deals lava damage
- [ ] **Tectium and Pyrium set bonuses, and the Skarnite tool perks** (Gear)
  - Ruskite (Heat Scale, 25% less fire damage) and Skarnite (fire immunity) work. Missing: Tectium Anchored (knockback resistance), Pyrium Kindled (tools auto-smelt ores 20% of the time), and the Skarnite tools' Ember Touch auto-smelt, burning axe and ember crits.
  - Evidence: item/ZGArmorSetBonuses.java has ruskite and skarnite only
- [ ] **3D worn models for Tectium and Pyrium armor** (Gear)
  - Ruskite and Skarnite use GeckoLib shells; Tectium and Pyrium fall back to vanilla layers. Follow the art-direction lock.
  - Evidence: item/ZGArmorItem.java IMPLEMENTED set
- [ ] **Play the Galaxy 3 loop in a real client** (Polish)
  - Arrive on Skarn with a T3 gate, mine the eight ores, survive Magma Slag lakes, beat the Rift Tyrant (once it exists), then build the T4 gate. Check heat, gravity (1.2) and mob pressure on screen.
  - **Lore:** Check the Act III beats: the arena tearing apart, Echo's memory returning afterwards, and the Ashwrights' scorched-marble masks.
  - Evidence: Docs ledger: headless tests only

## Open: Normal

- [ ] **Give each Skarn biome its own features** (Worlds)
  - Ember Fields, Marble Contact Zone and Charwood Barrens share the same feature list (charwood trees, magma lakes, emberthorn, cinder caps, rift glass). Make them differ: marble outcrops in the contact zone, dense ember crust and vents in the fields, burnt forest in the barrens. The design also says Skarn ores cluster where lava meets stone.
  - **Lore:** Rift Glass marks the fracture zones where Vael tore space; concentrate it there.
  - Evidence: worldgen/biome/ember_fields.json, marble_contact_zone.json, charwood_barrens.json
- [ ] **Ashwright signature profession and Cinnabrite trading** (Villagers)
  - Skarn's Ashwright villagers have vanilla jobs only. Add their signature profession and use Cinnabrite as the trade gem.
  - **Lore:** Canon signature profession: Ashwright Smith, job site Alloy Forge. They forged the first gate parts and know it; showing your fire is rude, hence the scorched-marble masks. Cinnabrite is Skarn's trade gem.
  - Evidence: registry/ZGPlanetVillagers.java THEMES skarn=ashwright; no Skarn trades
- [ ] **Codex pages for Act III (The Wound)** (Progression)
  - Add Skarn arrival and post-Tyrant pages. After the Tyrant, Echo remembers she plotted the course here.
  - **Lore:** Act III, The Wound: where Vael tore space open, and Echo remembering she plotted the course here. Story text needs approval before it ships.
  - Evidence: item/ConcordCodexItem.java has no Skarn pages; advancement/codex/skarn.json exists
- [ ] **Make the Tremor Lamp flicker** (Worlds)
  - The design calls for flickering light from Tremor Dust; today it is a fixed light-15 block.
  - Evidence: BlockInit.java: TREMOR_LAMP lightLevel(s -> 15)
- [ ] **Galaxy 3 wasteland content (shared with Galaxy 2)** (Wastelands)
  - g3_p1 to g3_p6 reuse the same wasteland biomes, so the Galaxy 2 tasks for wasteland structures, signature mobs, armor upgrades, hazards and the moon gate rule fix these slots too. Default order here: frozen, toxic, crystal, barren, ocean, desert; moons barren.
  - Evidence: dimension/g3_*.json; data-manifest galaxy_slots_default_type
- [ ] **Tectium casings and Magma Slag heat for the Alloy Forge** (Machines)
  - Once the Galaxy 2 machines exist: Tectium is the second casing tier, and Magma Slag is the Alloy Forge's heat source.
  - Evidence: tectium_casing registered as a plain block; design: Liquids and Machines
- [ ] **Real block properties for Skarn blocks** (Systems)
  - Scorched Marble, Ember Crust and the Skarn Rock families still use the generic stone props. Give Ember Crust its glow (light level) and the marble a calcite-like sound and hardness.
  - Evidence: registry/BlockInit.java generic props

## Done

- [x] **Skarn dimension** (Worlds): Three biomes (Ember Fields, Marble Contact Zone, Charwood Barrens), surface rules with Ember Crust, Slag and Scorched Marble, and gravity 1.2. Evidence: dimension/skarn.json; worldgen/noise_settings/planet/skarn.json; ZGProgressionConfig skarnGravity
- [x] **Skarn terrain, plants and decor** (Worlds): Skarn Rock, Scorched Marble, Slag (falls like gravel), Ember Crust, Rift Glass and Slag Glass. Emberthorn (slows and pricks like a sweet berry bush), Cinder Cap and Charwood trees with a full wood set. Tremor Lamp. Evidence: registry/BlockInit.java; ZGThornBushBlock.java; worldgen charwood_trees, patch_emberthorn, patch_cinder_cap, rift_glass_scatter
- [x] **All eight Skarn ores and their mining gates** (Worlds): Emberite, Ruskite, Tectium, Pyrium, Tremor Dust, Rift Opal, Skarnite and Cinnabrite. Ruskite needs a Cerulite pick, the other metals and gems need Ruskite, and Skarnite needs Tectium. Emberite burns in furnaces and the Combustion Generator. Evidence: tags/block/needs_cerulite_tool, needs_ruskite_tool, needs_tectium_tool; data_maps furnace_fuels; CombustionBlockEntity emberite
- [x] **Magma Slag liquid** (Worlds): Sets you on fire and deals lava damage. Water turns it into Slag and Liquid Starlight into Rift Glass. Lakes generate in all three biomes. Evidence: registry/ZGDimensionFluids.java; worldgen lake_magma_slag_surface
- [x] **Galaxy 3 tool tiers, Ruskite and Skarnite armor** (Gear): All four Skarn sets have real tiers and smithing recipes. Ruskite and Skarnite have 3D shells; Ruskite takes 25% less fire damage and Skarnite is fire-immune. Evidence: registry/ZGToolTiers.java; item/ZGArmorItem.java; ZGArmorSetBonuses.java
- [x] **T4 gate shape and cost** (Gate & travel): Skarnite ring with a taller half-arch; 8M FE; reaches Galaxy 4. Evidence: travel/SurvivalGateLayout.java tier 4; ZGProgressionConfig tier4FE
- [x] **Ashwright villagers on Skarn** (Villagers): The species is registered and placed in settlements. Lore: Descended from the Concord smiths caught at the forges when the rift opened. Evidence: registry/ZGPlanetVillagers.java
- [x] **Six wasteland slots and a moon** (Wastelands): g3_p1 to g3_p6 and g3_moons generate with the shared wasteland biomes, signature blocks and Galaxy 3 tint. Evidence: dimension/g3_*.json; client/ZGBlockColors.java
- [x] **Act III advancements** (Progression): Skarn and Rift Tyrant advancements exist; the Tyrant one can't trigger until the boss exists. Evidence: advancement/codex/skarn.json, rift_tyrant.json

## Mining ladder through Galaxy 3

| Ore | Needs | Template source | Status |
| --- | --- | --- | --- |
| Ruskite | Cerulite pick | Collapsed Forge | ✗ structure missing |
| Pyrium, Rift Opal, Cinnabrite, Tectium | Ruskite pick | Collapsed Forge | ✗ structure missing |
| Skarnite | Tectium pick | Collapsed Forge or Rift Tyrant | ✗ both missing |

