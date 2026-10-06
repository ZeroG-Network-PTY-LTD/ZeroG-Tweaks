# Galaxy 2 (Cerulon) build tracker

What is left before players can reach Cerulon on a T2 gate, climb the Cobaltium → Cyrrium → Cerulite ladder, beat the Prism Sentinel, explore the six wasteland slots and build the T3 gate.

- **Audited against:** `1.21.x` at `5273b965` on 5 Oct 2026; updated for `15200c39` (machines and power) on 6 Oct 2026.
- **Scope:** Cerulon, wasteland slots `g2_p1` to `g2_p6`, the moon slot `g2_moons`, the T3 gate, and the Galaxy 2 gear and machines.
- **Live tracker:** the Galaxy 2 Build Tracker artifact (tick items there).
- **HTML copy:** [`galaxy2-build-tracker.html`](galaxy2-build-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.
- **Lore:** follow [`lore/README.md`](lore/README.md). Items with a **Lore** note must match it; don't invent new canon, flag gaps as "lore needed".

**18 open, 14 done.** Cerulon itself is mostly built: dimension, ores, geodes, Liquid Starlight, mobs and the Prism Sentinel. The progression is not. The Cobaltium, Cyrrium and Aurelion templates can't be found, so players can't climb the ladder, and the Sentinel's key doesn't unlock anything. The wasteland slots generate, but their structures, signature mobs and rewards are missing.

## Lore: Act II: The Quiet Mines (Cerulon)

- Cerulon is the Concord's peaceful mining world.
- The Prism Sentinel is a test, not a hunt: it asks whether you are Concord, fights in light-refracting phases, and once beaten accepts you as an heir.
- Side quests in this galaxy's wastelands: the Sunken Relay (a distress signal still broadcasting) and the Buried Observatory (it leads to a hidden planet).

Rules for everything on this list:

- Keep the approved Prologue and the five acts. Don't invent new coordinates, factions, characters or registry IDs.
- Echo remembers a world only after the player reaches it. Her lines arrive as Codex pages and advancement toasts; there is no dialogue system.
- Archon Vael is the villain, always one world ahead: he appears in logs and rift whispers, and is only revealed as the Dying Star in Act V.
- The Keepers are guardian constructs still following Concord orders. Don't reveal that the Splinter creatures are the Concord before Act V.
- Put player-facing story text in lang keys (en_us.json), not hardcoded strings.

Full guide: [`lore/README.md`](lore/README.md). Don't invent new canon; flag gaps as "lore needed".

## Open: Blockers

- [ ] **Make the Cobaltium, Cyrrium and Aurelion upgrade templates obtainable** (Progression)
  - Every set after Nullifite is made at the smithing table with a template. These three templates only drop from the Prism Spire chest, and the Prism Spire doesn't exist, so players can't go from Olympium to Cobaltium. Without Cyrrium gear they can't mine Cerulite, so the T3 gate is blocked too. Fix by building the Prism Spire (see the wasteland structures task) or adding the templates to Cerulon loot (Concord Vault common/uncommon chests, Glintfolk trades) in the meantime.
  - **Lore:** Upgrade templates are Concord craft knowledge. Put them where the Concord left them: the Concord Vault and the Prism Spire, or Glintfolk trades once the player is an heir. Don't scatter them into unrelated wasteland loot.
  - Evidence: loot_table/chests/prism_spire.json is the only source; chests/concord_vault/*.json hold only the Cerulite template; worldgen/structure has no prism_spire; tags/block/needs_cyrrium_tool lists cerulite_ore and cerulite_cluster
- [ ] **Make the Prism Sentinel's key unlock the T3 gate** (Gate & travel)
  - The design says beating each galaxy's guardian unlocks the next gate tier. The Sentinel drops galaxy_3_gate_key, but nothing uses it: the Cerulite gate frame recipe needs only Cerulite and bricks, and the controller never checks for a key. Either put the key in the T3 frame or lens recipe, or have the controller need it in a slot before it forms T3.
  - **Lore:** The Prism Sentinel is a Keeper and a test, not a hunt. Beating it ends with "...you are Concord. Inherit." and the key. The T3 gate should only be buildable after that acceptance.
  - Evidence: loot_table/entities/prism_sentinel.json drops galaxy_3_gate_key; no recipe or Java uses it; recipe/cerulite_gate_frame.json

## Open: High

- [ ] **Build the seven wasteland structures** (Wastelands)
  - Sunken Relay (ocean), Buried Observatory (desert), Collapsed Forge (volcanic), Frozen Outpost (frozen), Sunken Lab (toxic), Prism Spire (crystal) and Impact Site (barren). Their loot tables already exist and hold the Galaxy 2 and 3 templates and Star Map Fragments. Since 15200c39, Abyssal Pearl, Heatproof Plating, Neutralizer and Cryo Core can also be made in the Alloy Forge, so the structures are no longer their only source. Reuse DryLandJigsawStructure, which the crash site already uses.
  - **Lore:** Approved side quests: Sunken Relay is a distress signal still broadcasting; Buried Observatory leads to a hidden planet (Star Map Fragments); Collapsed Forge is the smith who built the first gate. Frozen Outpost, Sunken Lab, Prism Spire and Impact Site have no story yet: build them as Concord ruins and flag their text. Story text needs approval before it ships.
  - Evidence: loot_table/chests/{sunken_relay,buried_observatory,collapsed_forge,frozen_outpost,sunken_lab,prism_spire,impact_site}.json exist; worldgen/structure has only concord_vault, prism_sentinel_arena and the two Mars structures
- [ ] **Register the wasteland signature mobs** (Mobs)
  - Ash Strider (volcanic), Rime Stalker (frozen), Bog Lurker (toxic), Amethyst Stalker (crystal) and Crater Drifter (barren) aren't registered. All except the Amethyst Stalker already have GeckoLib models and animations in the repo; the Amethyst Stalker comes from the Shattered Skies library. Tidewraith is registered but never spawns naturally on ocean worlds. Volcanic and toxic slots spawn Rust Beetle as a placeholder. Several of these mobs drop wasteland rewards: Rime Stalker drops the Cryo Core, Bog Lurker the Neutralizer, Ash Strider the Heatproof Plating.
  - **Lore:** Wasteland mobs are wildlife. Only the Keepers (guardian constructs) are Concord-made, and Splinter creatures mustn't be explained before Act V. Tidewraith and Amethyst Stalker come from the Shattered Skies roster.
  - Evidence: registry/EntityInit.java; assets geo/ash_strider, rime_stalker, bog_lurker, crater_drifter .geo.json; biome_modifier/planet_ready_skarn_mobs.json spawns rust_beetle in acid swamps and ash plains
- [ ] **Armor upgrade system (Abyssal Pearl, Heatproof Plating, Neutralizer)** (Gear)
  - The upgrade items exist but do nothing. Add the smithing upgrade stored as a new data component (one slot per piece up to Cerulite), with water breathing, fire resistance and poison immunity. Grav Boots isn't registered at all.
  - Evidence: ItemInit.java registers the items as plain items; no data component; AGENTS.md M1 'Armor upgrades' unticked
- [ ] **Seeded galaxy and catalog names on the star chart** (Worlds)
  - The g2_p1 to g2_p6 slot types are fixed (ocean, desert, volcanic, frozen, toxic, crystal; moons barren), not rolled from the world seed. The star chart shows raw ids like "g2 p1" instead of catalog names such as ZG-855 d "Vorrhex".
  - **Lore:** Catalog names follow ZG-[galaxy] [letter] "Name" plus a class tag (Resource, Hostile, Frozen, Derelict…). Resource planet names are fixed; only wasteland and moon names come from the seeded pool.
  - Evidence: dimension/g2_p*.json fixed biome lists; ZGDimensionTerrain.java: 'independent of the future seeded galaxy generator'; client/SurvivalGateScreen.java uses the id as the button label
- [ ] **Cyrrium, Aurelion and Cerulite set bonuses and Cerulite tool perks** (Gear)
  - Only Cobaltium (Quick Hands) is done. Missing: Cyrrium Tempered (+20% durability), Aurelion Silver Tongue (better alien trader prices), Cerulite Crystal Sight (night vision, nearby ores glow), plus the Cerulite tool perks Ore Sense and Crystal Edge.
  - Evidence: item/ZGArmorSetBonuses.java has no cyrrium, aurelion or cerulite case
- [ ] **3D worn models for Cyrrium, Aurelion and Cerulite armor** (Gear)
  - Cobaltium uses its GeckoLib shell. The other three Galaxy 2 sets fall back to vanilla armor layers. Follow the art-direction lock.
  - Evidence: item/ZGArmorItem.java IMPLEMENTED set includes cobaltium but not cyrrium, aurelion or cerulite
- [ ] **Play the Galaxy 2 loop in a real client** (Polish)
  - Build a T2 gate, reach Cerulon, mine the eight ores, open a geode, find the Concord Vault keys, beat the Prism Sentinel, visit each wasteland slot, then build the T3 gate. Check the Sentinel fight, Liquid Starlight effects, mob behaviour and spawn density on screen.
  - **Lore:** Check the Act II beats: the Vault feels calm and Concord-crafted; the Sentinel asks "Are you Concord?", fights in light-refracting phases and names the player an heir; afterwards the Glintfolk call the player "heir" in their trade titles.
  - Evidence: Docs ledger: all checks so far are headless server tests

## Open: Normal

- [ ] **Let the T2 gate reach Galaxy 2's moon** (Gate & travel)
  - canReach() only allows *_moons destinations at T6, so Cerulon's moon (Cinder, g2_moons) can't be visited until the end game. Allow a galaxy's moons at that galaxy's gate tier.
  - **Lore:** Moons use the planet's catalog id plus a Roman numeral, e.g. ZG-855 b I "Cinder".
  - Evidence: travel/SurvivalGateBlockEntity.canReach(): (!id.endsWith("_moons")||tier==6)
- [ ] **Wasteland surface effects, and a Neutralizer exemption for Acid** (Wastelands)
  - Glacial Ice should be slippery (friction 0.98) and Vent Rock should smoke; both are plain blocks. Acid already works as designed: Poison II, armor wear and dropped items dissolving after 5 seconds. But no armor can resist it until the Neutralizer upgrade exists (see Armor upgrade system).
  - Evidence: BlockInit.java: VENT_ROCK and GLACIAL_ICE = new Block(props(STONE...)); registry/ZGDimensionFluids.java case "acid"
- [ ] **Glintfolk signature profession and Lumenite trading** (Villagers)
  - Cerulon's Glintfolk villagers exist with vanilla jobs only. Add their signature profession and use Lumenite as the alien-trader currency (it also makes the Aurelion Silver Tongue perk mean something).
  - **Lore:** Canon signature profession: Crystal Tender, job site Crystal Growth Chamber. The Glintfolk are the miners who stayed with the Sentinel, and they call the player "heir" after the Sentinel. Lumenite is Cerulon's trade gem.
  - Evidence: registry/ZGPlanetVillagers.java THEMES has cerulon=glintfolk; registry/ZGSolTrades.java covers only Lunari and Rustborn
- [ ] **Codex pages for Act II (The Quiet Mines)** (Progression)
  - Advancements for Cerulon, Cerulite and the Prism Sentinel exist, but the Codex book has only the prologue, Moon and Mars pages. Add Cerulon arrival and Sentinel pages.
  - **Lore:** Act II, The Quiet Mines: the Concord's peaceful mining world, and the Sentinel as a test. Echo only remembers Cerulon once the player has arrived. Story text needs approval before it ships.
  - Evidence: item/ConcordCodexItem.java pages: prologue, zerog_codex_moon, zerog_codex_mars
- [ ] **Make the Pulsar Lamp pulse** (Worlds)
  - The design calls it a pulsing light from Pulsar Dust; it is a fixed light-15 block. Cycle the light level or brightness with a block state.
  - Evidence: BlockInit.java: PULSAR_LAMP = new Block(... lightLevel(s -> 15))
- [ ] **Shardwood tap for Shardwood Syrup** (Worlds)
  - The syrup food exists, but there is no way to tap Shardwood logs for it.
  - Evidence: item/ZGFoods.java SHARDWOOD_SYRUP; no interaction in event/ZGInteractions
- [ ] **Deep Eel (ocean) and Sand Skitter (desert)** (Mobs)
  - These are the two wasteland food mobs from the design (Eel Fillet and Skin; Skitter Leg, Carapace and Venom Gland). Their models and animations are in the repo, but the entities aren't registered.
  - Evidence: assets geo/deep_eel.geo.json, sand_skitter.geo.json; not in EntityInit
- [ ] **Real block properties for Galaxy 2 blocks** (Systems)
  - Wasteland signature blocks (Vent Rock, Glacial Ice, Ruinstone, Meteorite Fragment, crystals) and many Cerulon families still use the generic stone props (2.5 hardness, stone sound). Give crystals the amethyst sound and ice the glass sound and friction.
  - Evidence: registry/BlockInit.java: props(MapColor.STONE, SoundType.STONE, 2.5F, 7.0F)
- [ ] **Readable names for wasteland slot blocks** (Polish)
  - Generated per-slot blocks show names like "G2 P1 Short Grass" and "G2 P1 Soil". Name them by type (for example "Kelp-Jungle Grass") or by the seeded planet name.
  - **Lore:** Wasteland names come from the seeded name pool with a class tag; never hand-write story names for wastelands.
  - Evidence: assets/zerog_tweaks/lang/en_us.json block.zerog_tweaks.g2_p1_*

## Done

- [x] **Working Alloy Forge, Crystal Growth Chamber and Salvage Station** (Machines): These are plain blocks. Add block entities, menus and FE, register the alloying, crystal_growth and salvaging recipe types, and move the pending recipe JSONs in. Liquid Starlight is meant to feed the Crystal Growth Chamber. Cyrrium casings should set speed and efficiency. Evidence: 15200c39: machine/ProcessingBlockEntity, ProcessingRecipe, ProcessingRegistry: Alloy Forge, Crystal Growth Chamber and Salvage Station with refining, alloying, crystal_growth and salvaging recipes; casing tiers Cyrrium to Astrium plus a Cryo Core slot
- [x] **Cerulon dimension with nine biomes** (Worlds): Azure Plains, Cerulean Peaks, Concord Quarries, Crystal Shores, Geode Depths, Glimmer Sea, Shardwood Grove, Starbloom Meadow and Starlight Caverns; gravity 0.9. Evidence: dimension/cerulon.json; ZGProgressionConfig cerulonGravity
- [x] **Cerulon terrain, plants and decor** (Worlds): Cerulean Stone, Crystal Sand, Azure Moss, Starbloom (light blue dye), Shardwood trees and wood set, Pulsar Lamp, Crystal Glass. Evidence: registry/BlockInit.java; recipe/light_blue_dye_from_starbloom.json
- [x] **All eight Cerulon ores and their mining gates** (Worlds): Nebulite (a fuel), Cobaltium, Cyrrium, Aurelion, Pulsar Dust, Starlite, Cerulite and Lumenite. Cobaltium needs an Olympium pick and Cerulite a Cyrrium pick. Evidence: worldgen/configured_feature/ore_*.json; tags/block/needs_olympium_tool, needs_cyrrium_tool; data_maps furnace_fuels has nebulite
- [x] **Geode-only Cerulite with budding growth** (Worlds): Cerulite grows in geodes from budding_cerulite, not in veins. Evidence: worldgen/configured_feature/cerulite_geode.json; ZGBuddingCrystalBlock
- [x] **Liquid Starlight** (Worlds): Light 12, Slow Falling and Night Vision while swimming. It turns water into Crystal Sand and lava into Prismstone. Evidence: registry/LiquidStarlightBlock.java, ZGFluids.java, ZGDimensionFluids.java
- [x] **Cerulon mobs with AI and spawns** (Mobs): Crystal Stag (shear for Starlite), Prismling (shatters), Mossback, Azure Fowl (glides, lays Blue Eggs) and Glimmerfish (glowing schools). Evidence: entity/*.java; biome_modifier/spawns_cerulon_*.json
- [x] **Prism Sentinel boss in the Concord Vault** (Progression): A phased fight in the Sentinel chamber, reached with keys from the vault's mine-style rooms. Drops Cerulite, the Cerulite template, the galaxy_3_gate_key and the Sentinel Prism. Lore: Built as a test chamber: "Are you Concord?" then "...you are Concord. Inherit." Keep that framing in any change. Evidence: entity/PrismSentinel.java, arena/*; worldgen/ConcordVaultStructure.java; loot_table/entities/prism_sentinel.json
- [x] **T3 gate shape and cost** (Gate & travel): Cerulite ring with eight pylons and two energy ports; 3M FE; reaches Galaxy 3. (The key requirement is a separate blocker.) Evidence: travel/SurvivalGateLayout.java tier 3; ZGProgressionConfig tier3FE
- [x] **Six wasteland slots and a moon with signature blocks** (Wastelands): g2_p1 to g2_p6 and g2_moons use the seven wasteland types. Brine Crystal, Ruinstone, Vent Rock, Frost Crystal, Prism Cluster, Meteorite Fragment and Acid lakes generate, and galaxy tinting works. Evidence: dimension/g2_*.json; worldgen/biome/wasteland_*.json; client/ZGBlockColors.java
- [x] **Glintfolk villagers on Cerulon** (Villagers): The species is registered with a renderer and placed in settlements. Lore: Concord hard hats and Cerulite shoulder spurs (filed down for luck) are canon. Evidence: registry/ZGPlanetVillagers.java
- [x] **Galaxy 2 tool tiers, Cobaltium worn model and Quick Hands** (Gear): All four Galaxy 2 sets have real tiers and smithing recipes. Cobaltium has its 3D shell and +10% mining speed. Evidence: registry/ZGToolTiers.java; item/ZGArmorItem.java; ZGArmorSetBonuses.java
- [x] **Act II advancements** (Progression): Cerulon, Cerulite and Prism Sentinel advancements exist. Evidence: advancement/codex/cerulon.json, cerulite.json, prism_sentinel.json
- [x] **Refracting Lens and Star Map Fragment sources** (Gate & travel): The Refracting Lens is craftable. Star Map Fragments drop from the Dune Burrower and Meteor Maw. Evidence: recipe/refracting_lens.json; loot_table/entities/dune_burrower.json, meteor_maw.json

## Wasteland reward map (design)

| Slot | Type | Signature block | Mob | Structure | Reward |
| --- | --- | --- | --- | --- | --- |
| g2_p1 | Ocean | Brine Crystal ✓ | Tidewraith (registered, no natural spawn) | Sunken Relay ✗ | Abyssal Pearl |
| g2_p2 | Desert | Ruinstone ✓ | Dune Burrower ✓ | Buried Observatory ✗ | Star Map Fragments |
| g2_p3 | Volcanic | Vent Rock ✓ | Ash Strider ✗ | Collapsed Forge ✗ | Heatproof Plating |
| g2_p4 | Frozen | Frost Crystal ✓ | Rime Stalker ✗ | Frozen Outpost ✗ | Cryo Core |
| g2_p5 | Toxic | Acid lakes ✓ | Bog Lurker ✗ | Sunken Lab ✗ | Neutralizer |
| g2_p6 | Crystal | Prism Cluster ✓ | Amethyst Stalker ✗ | Prism Spire ✗ | Refracting Lens + G2 templates |
| g2_moons | Barren | Meteorite Fragment ✓ | Crater Drifter ✗ | Impact Site ✗ | Stardust |

Slot types are the fixed defaults from `data-manifest.json` until the seeded galaxy generator replaces them.
