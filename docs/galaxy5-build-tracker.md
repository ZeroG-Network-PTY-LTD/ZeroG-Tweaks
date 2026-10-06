# Galaxy 5 (Solvane) build tracker

What is left before players can reach Solvane on a T5 gate, survive the heat, climb the Photium → Astrium → Solvanite ladder, defeat the Dying Star, make the ending choice and build the T6 gate.

- **Audited against:** `1.21.x` at `5273b965` on 5 Oct 2026; updated for `15200c39` (machines and power) on 6 Oct 2026.
- **Scope:** Solvane, wasteland slots `g5_p1` to `g5_p6`, the moon slot `g5_moons`, the T6 gate, the endgame gear, the Fusion Reactor, and the ending. Reaching Galaxy 5 in survival depends on the Galaxy 2 to 4 blockers.
- **Live tracker:** the Galaxy 5 Build Tracker artifact (tick items there).
- **HTML copy:** [`galaxy5-build-tracker.html`](galaxy5-build-tracker.html), a static snapshot. Download it, or open it from a local clone, to view it in a browser.
- **Rule:** an item is done only when the code exists. Headless tests are not client approval.
- **Lore:** follow [`lore/README.md`](lore/README.md). Items with a **Lore** note must match it; don't invent new canon, flag gaps as "lore needed".

**15 open, 10 done.** Solvane's world is built: terrain, eight ores, Solar Plasma, Gildwood trees and the T6 ring. The endgame isn't. There is no Dying Star, no Solar Shrine and no ending, so the Photium, Astrium and Radiantine templates can't be found and the Heart of Solvane does nothing. Solvane's own mobs are missing too, though their models exist.

## Lore: Act V: The Last Light (Solvane) and the ending

- The Nova Pearl reveals that Vael fused himself with the dying sun: the Dying Star is Vael.
- The Splinter creatures are the Concord, who shattered themselves to hold him back. Earth was meant to be their refuge, so the player has been finishing their migration.
- Ending choice with the Heart of Solvane, per player. Rekindle the star: Solvane burns bright, a radiant T6 crown, and Echo stays as a companion. Let it fade: the Concord remnants go free, a void-themed crown, and Echo says goodbye in a final Codex entry.

Rules for everything on this list:

- Keep the approved Prologue and the five acts. Don't invent new coordinates, factions, characters or registry IDs.
- Echo remembers a world only after the player reaches it. Her lines arrive as Codex pages and advancement toasts; there is no dialogue system.
- Archon Vael is the villain, always one world ahead: he appears in logs and rift whispers, and is only revealed as the Dying Star in Act V.
- The Keepers are guardian constructs still following Concord orders. Don't reveal that the Splinter creatures are the Concord before Act V.
- Put player-facing story text in lang keys (en_us.json), not hardcoded strings.

Full guide: [`lore/README.md`](lore/README.md). Don't invent new canon; flag gaps as "lore needed".

## Open: Blockers

- [ ] **The Dying Star final boss and arena** (Progression)
  - The final boss doesn't exist in game. Its GeckoLib model and animations are in the repo, and its loot table is ready (Heart of Solvane, Solvanite and the Solvanite template). Missing: the entity, its phases, the arena and how players reach it. Act V, The Last Light: Archon Vael fused with Solvane's dying sun.
  - **Lore:** Act V, The Last Light: the Nova Pearl reveals that Vael fused himself with the dying sun, so the Dying Star is Vael. Here the player learns the Splinter creatures are the Concord, and that Earth was their refuge.
  - Evidence: assets geo/dying_star.geo.json; loot_table/entities/dying_star.json; not in EntityInit; no arena structure
- [ ] **Solar Shrine structure (the Photium, Astrium and Radiantine templates)** (Progression)
  - The Photium, Astrium and Radiantine templates only drop from the Solar Shrine chest, and the Solar Shrine doesn't exist, so the gear ladder stops at Eidolite. The Solvanite template also comes from the Shrine, the Dying Star or the Sun Colossus, and none of them exist.
  - **Lore:** The Sunwardens kept their oaths and burn the old hymns into gildwood; a shrine fits them. Its story isn't written yet. Story text needs approval before it ships.
  - Evidence: loot_table/chests/solar_shrine.json; entities/dying_star.json, sun_colossus.json; worldgen/structure has no solar_shrine
- [ ] **Heart of Solvane ending choice** (Progression)
  - The Heart of Solvane is a plain item that only the Dying Star drops. Build the per-player choice. Rekindle the star: Solvane burns bright, a radiant T6 gate crown, and Echo stays as a companion. Let it fade: the Concord remnants go free, a void-themed crown, and Echo says goodbye in a final Codex entry.
  - **Lore:** Per player, with the Heart of Solvane. Rekindle the star: Solvane burns bright, radiant T6 crown, Echo stays as a companion. Let it fade: Concord remnants go free, void-themed crown, Echo says goodbye in a final Codex entry.
  - Evidence: ItemInit.java: HEART_OF_SOLVANE = registerSimpleItem; advancement/codex/heart_of_solvane.json

## Open: High

- [ ] **Solvane mobs** (Mobs)
  - Solvane has none of its own. Its biomes borrow Cerulon's Azure Fowl and Crystal Stag, plus Nova Blazes and glowbugs. Flare Sprite (flying fire spirit near Flare Vents), Sun Colossus (slow Solar Stone mini-boss, which also drops the Solvanite template) and Gildcrab (passive, pinches when hit) all have models and animations in the repo. Gildcrab's loot and cooking recipes are ready too.
  - **Lore:** Canon roles: Flare Sprites are fire spirits near Flare Vents; the Sun Colossus is a slow giant of Solar Stone; the Gildcrab is passive.
  - Evidence: assets geo/flare_sprite, sun_colossus, gildcrab .geo.json; loot_table/entities/gildcrab.json; biome_modifier/expanded_habitat_solvane_*.json spawn azure_fowl and crystal_stag
- [ ] **Corona Crust, Flare Vent and Sunspot Rock (needs your call)** (Worlds)
  - The design makes Solvane the most dangerous world: Corona Crust burns, Flare Vents erupt fire geysers on a timer, and Sunspot Rock is the safe ground. All three are plain stone blocks. This sits against the agreed non-damaging rule, so decide whether Solvane is the exception (the design's hazard gate says its heat needs Skarnite gear or Heatproof Plating). Solar Plasma already burns.
  - Evidence: registry/BlockInit.java: CORONA_CRUST, FLARE_VENT, SUNSPOT_ROCK = new Block(props(STONE...)); ZGDimensionFluids case solar_plasma
- [ ] **Photium, Radiantine and Solvanite set bonuses, and the Solvanite tool perks** (Gear)
  - Astrium (Star Forged, +2 max health) works. Missing: Photium Glow (lights the area), Radiantine Radiant (+20% damage to undead and Splinter creatures), the Solvanite set bonus, and the Solvanite tools: 3x3 mining with auto-smelt, tree-felling axe, 5x5 hoe and the Solar Flare sword cone.
  - Evidence: item/ZGArmorSetBonuses.java has astrium only for Galaxy 5
- [ ] **3D worn models for Photium, Radiantine and Solvanite armor** (Gear)
  - Astrium uses a GeckoLib shell. The other three, including the endgame Solvanite set, fall back to vanilla layers.
  - Evidence: item/ZGArmorItem.java IMPLEMENTED set
- [ ] **Play the Galaxy 5 loop and the ending in a real client** (Polish)
  - Arrive on Solvane, survive the heat and Solar Plasma, climb to Solvanite, beat the Dying Star, make the ending choice and build the T6 gate to a moon. Check gravity (1.3) on screen.
  - **Lore:** Play both endings and check the Nova Pearl reveal, Echo staying or leaving, and the matching gate crown.
  - Evidence: Docs ledger: headless tests only

## Open: Normal

- [ ] **Give each Solvane biome its own features** (Worlds)
  - Corona Flats, Sunspot Plateaus and Gildwood Oasis share one feature list (Flare Vents, Gildwood trees, plasma lakes, Solflowers, Pyrevine, Slag Glass). Make the Flats dense with Corona Crust and vents, the Plateaus Sunspot Rock, and the Oasis a Gildwood grove. The design also puts the ores near molten flows.
  - Evidence: worldgen/biome/corona_flats.json, sunspot_plateaus.json, gildwood_oasis.json
- [ ] **Let every Skarnite-or-better set walk through Solar Plasma** (Gear)
  - The design says Heatproof Plating or Skarnite+ armor. The code exempts Skarnite, Eidolite and Solvanite only, so Photium, Astrium and Radiantine wearers still burn, and Heatproof Plating doesn't exist yet.
  - Evidence: registry/ZGDimensionFluids.java heatproofSet()
- [ ] **Sunwarden signature profession and Dawnstone trading** (Villagers)
  - Solvane's villagers have vanilla jobs only. Add their signature profession and use Dawnstone as the trade gem.
  - **Lore:** Canon signature profession: Sun Keeper, job site Solar Array. The Sunwardens tended the star before it began to die and kept their oaths; their attitude to the player follows the ending. Dawnstone is Solvane's trade gem.
  - Evidence: registry/ZGPlanetVillagers.java THEMES solvane=sunwarden
- [ ] **Codex pages for Act V (The Last Light) and the finale** (Progression)
  - Add Solvane arrival pages, the Nova Pearl reveal (Vael is the Dying Star; the Splinter creatures are the Concord) and the two ending entries.
  - **Lore:** Act V and the two ending entries (Echo stays, or Echo's goodbye). Story text needs approval before it ships.
  - Evidence: item/ConcordCodexItem.java has no Solvane pages
- [ ] **Solflower turns toward the sun; Radiant Bricks glow** (Worlds)
  - Solflower is a standard flower (Fire Resistance stew) without the sun-facing behaviour. Radiant Bricks should glow softly but use the generic stone props with no light.
  - Evidence: BlockInit.java: SOLFLOWER = ZGFlowerBlock; RADIANT_BRICKS = new Block(props(STONE...))
- [ ] **T6 standing ring and crown** (Gate & travel)
  - The T6 layout adds the Solvanite ring. The design's full standing ring gate with a crown, and the ending-dependent radiant or void crown, are not built.
  - **Lore:** The crown follows the ending: radiant if the star is rekindled, void-themed if it fades.
  - Evidence: travel/SurvivalGateLayout.java
- [ ] **Galaxy 5 wasteland content (shared with Galaxy 2)** (Wastelands)
  - g5_p1 to g5_p6 reuse the shared wasteland biomes, so the Galaxy 2 wasteland tasks cover them. Default order here: volcanic, frozen, toxic, crystal, barren, ocean; moons barren. T6 can reach every moon.
  - Evidence: dimension/g5_*.json; data-manifest galaxy_slots_default_type

## Done

- [x] **Fusion Reactor and the Solar Array on Solvane** (Machines): A T6 jump costs 50M FE. The design powers it with a Fusion Reactor fed with Fusion Dust or Solar Plasma, and a Solar Array that is huge near Solvane. Both are plain blocks. Astrium is the top casing tier. Evidence: 15200c39: power/PowerBlockEntity.java: Fusion Reactor burns Fusion Dust at 1,000 FE/t for 2,000 ticks (2M FE each, so a 50M T6 jump is about 25 dust); Solar Array x8 on Solvane; Astrium casing tier
- [x] **Solvane dimension** (Worlds): Corona Flats, Sunspot Plateaus and Gildwood Oasis; gravity 1.3. Evidence: dimension/solvane.json; ZGProgressionConfig solvaneGravity
- [x] **Solvane terrain, plants and decor blocks** (Worlds): Solar Stone, Corona Crust, Sunspot Rock, Slag Glass and Flare Vent are registered and generate. Solflower, Pyrevine, Gildwood trees with a full wood set, Radiant Bricks and the Fusion Lamp. Evidence: registry/BlockInit.java; worldgen flare_vent_scatter, gildwood_trees, patch_solflower, pyrevine
- [x] **All eight Solvane ores and their mining gates** (Worlds): Coronite, Photium, Astrium, Radiantine, Fusion Dust, Nova Pearl, Solvanite and Dawnstone. Photium needs an Eidolite pick, the others need Photium, and Solvanite needs Astrium. Evidence: tags/block/needs_eidolite_tool, needs_photium_tool, needs_astrium_tool
- [x] **Solar Plasma** (Worlds): Burns and deals plasma damage, except to full Skarnite, Eidolite or Solvanite. Water turns it into Slag Glass and Cryo Fluid into Sunspot Rock. Lakes generate. Evidence: registry/ZGDimensionFluids.java case solar_plasma; worldgen lake_solar_plasma_surface
- [x] **Galaxy 5 tool tiers and Astrium armor** (Gear): All four Solvane sets have real tiers and smithing recipes. Astrium has its 3D shell and Star Forged (+2 max health). Evidence: registry/ZGToolTiers.java; item/ZGArmorItem.java; ZGArmorSetBonuses.java
- [x] **T6 gate ring and cost** (Gate & travel): Solvanite outer ring; 50M FE; reaches every galaxy and the moon slots. Evidence: travel/SurvivalGateLayout.java tier 6; SurvivalGateBlockEntity.canReach()
- [x] **Sunwarden villagers on Solvane** (Villagers): The species is registered and placed in settlements. Lore: Corona halos are grown, a gift of the star; they are not jewellery. Evidence: registry/ZGPlanetVillagers.java
- [x] **Gildcrab food chain data** (Mobs): Cooked Gildcrab and the Starfall Feast recipes are ready for when the Gildcrab exists. Evidence: recipe/cooked_gildcrab*.json, starfall_feast.json
- [x] **Six wasteland slots and a moon** (Wastelands): g5_p1 to g5_p6 and g5_moons generate with the shared wasteland biomes and the Galaxy 5 tint. Evidence: dimension/g5_*.json; client/ZGBlockColors.java

## Mining ladder through Galaxy 5

| Ore | Needs | Template source | Status |
| --- | --- | --- | --- |
| Photium | Eidolite pick | Solar Shrine | ✗ structure missing |
| Radiantine, Nova Pearl, Dawnstone, Astrium | Photium pick | Solar Shrine | ✗ structure missing |
| Solvanite | Astrium pick | Solar Shrine, Dying Star or Sun Colossus | ✗ all missing |

