# ZeroG Tweaks — Design Doc

Sep 28, 2026 · @MrWhiteFlamesYT

**Design locked: v1.2 (Sep 29, 2026; adds gear stats and abilities, and the six liquids).** Every section below is final for the first build; changes from here go in as v1.1 revisions.

**v1.3 (Oct 1, 2026):** mining ladder (Nullifite needs netherite; each ore needs the pickaxe before it) and gear stats rebalanced so every set is above netherite.

## Overview

ZeroG Tweaks is an Allthemodium-style progression mod for NeoForge 1.21.1, space-themed through exploration rather than survival mechanics like oxygen. Players travel between galaxies with a tiered teleporter, and each galaxy supplies the materials for the next tier.

- **Theme:** space flavor without competing with Galacticraft or Ad Astra; extra content only when those mods are loaded.
- **Visual identity:** a "shattered void" look carries through the whole mod, set by Nullifite.
- **Name (locked):** ZeroG Tweaks (`zerog_tweaks`).

**Phase plan**

1. Dimensions and travel (this doc)
2. What players find: blocks, ores, mobs, structures, plants
3. What players do with it: tools, armor, machine upgrades, tweaks
4. Optional compatibility with other space mods

## Universe structure and naming

The universe has up to 5 galaxies; each galaxy is one progression tier.

| Level | Count | Notes |
| --- | --- | --- |
| Galaxy | Up to 5 | Galaxy 1 is Sol |
| Planet | 5–8 per galaxy | One Resource planet and one key world per galaxy |
| Moon | 0–3 per planet | Rolled from a smaller moon pool |

**Naming convention** follows real planet catalogs: `ZG-[galaxy number] [planet letter] "Name"` plus a class tag. Moons add a Roman numeral.

- ZG-855 b "Cerulon" — Resource World
- ZG-855 b I "Cinder" — first moon of Cerulon
- ZG-855 d "Vorrhex" — a seeded wasteland name

Planet letters start at b, following the real convention where "a" is the star. Class tags: Resource, Hostile, Stellar, Frozen, Derelict and similar.

## Galaxy generation rules

Sol is fixed in every world; Galaxies 2–5 are rolled from the world seed with fixed rules so progression stays fair.

**Sol (Galaxy 1, fixed):** Earth (the Overworld), the Moon and Mars.

**Galaxies 2–5 (seeded), every galaxy always has:**

- Exactly one Resource planet, whose ore builds the next teleporter tier
- One key world holding the gate or item that unlocks the next galaxy
- 3–6 wasteland planets rolled from the pool below
- 0–3 moons per planet

**The seed decides:** catalog numbers, planet names (from a name pool), planet types, moon counts and which slot holds the Resource planet.

**Wasteland pool**

| Type | Terrain |
| --- | --- |
| Ocean | All water, rare islands |
| Desert | Dunes and buried ruins |
| Volcanic | Lava plains and ash storms |
| Frozen | Ice sheets and cryo caves |
| Toxic | Acid swamps, poison atmosphere |
| Crystal | Geode fields |
| Barren | Empty, cratered rock |

Every wasteland gives one small reward (a plant, mob drop or ruin) so players don't skip them.

**Resource planets (fixed names, locked):** Resource planet names never change between seeds, so ores, lore and wiki pages always match. Only wasteland and moon names come from the seeded name pool. Each planet's rare gem can be named after it (e.g. Cerulon → Cerulite).

| Galaxy | Resource planet | Theme |
| --- | --- | --- |
| 2 | Cerulon | Blue, crystalline |
| 3 | Skarn | Fractured, hostile |
| 4 | Eidolon | Frozen, derelict |
| 5 | Solvane | Stellar endgame, fading sun |

## Technical approach for dimensions

Use fixed slot dimensions with a seeded chunk generator. In NeoForge 1.21.1, dimensions are locked in at world load, so per-seed dimensions need a workaround.

- Register slot dimensions such as `zerog:g2_p1` through `zerog:g2_p8` (plus moon slots).
- A custom chunk generator reads the world seed, decides the slot's type (for example, "ocean world"), and builds matching terrain.
- Registry IDs stay stable; only content changes per seed. Unused slots never appear on the star chart.
- Sol uses stable readable IDs (e.g. `zerog:moon`, `zerog:mars`); catalog codes are display-only (names, tooltips, lore, teleporter screen).

**Alternative:** runtime dimensions via a library like Commoble's Infiniverse. More flexible, but more complex and fragile.

**Release scope (locked):** all 5 galaxies with the full 5–8 planets each ship at first release. To keep memory use manageable, moons can share one dimension with different biomes.

**Gravity (locked): per-world values**, applied with the vanilla gravity attribute when a player enters a dimension. Starting values for playtesting:

| World | Gravity |
| --- | --- |
| Moon | 0.5× |
| Mars | 0.7× |
| Cerulon | 0.9× |
| Eidolon | 0.8× |
| Skarn | 1.2× |
| Solvane | 1.3× |
| Wastelands | Rolled per seed, 0.6–1.3× |

## Tiered teleporter

A massive multiblock teleporter is the only way to travel. Materials from galaxy N build the tier that reaches galaxy N+1.

| Tier | Built from | Reaches | Capacity | Size (rough) |
| --- | --- | --- | --- | --- |
| T1 | Rare Overworld ore | Moon, Mars | 2 players + pets | 5×5 |
| T2 | Sol materials (Moon, Mars) | Galaxy 2 | 2 players + pets | — |
| T3 | Galaxy 2 Resource ore | Galaxy 3 | 4 players | \~9×9 with pylons |
| T4 | Galaxy 3 materials | Galaxy 4 | 4 players | — |
| T5 | Galaxy 4 materials | Galaxy 5 | 8 players | — |
| T6 | Galaxy 5 materials | Anywhere, including a specific moon | 8 players | 15×15+ with arch |

- **T1 ore:** as rare as Allthemodium in the Overworld, custom named. Nullifite (locked), deep deepslate only, more common near ancient cities.
- **Secondary ingredients:** wasteland crystals and drops become lenses, coils and focus crystals.
- **Upgrade in place:** the T1 core stays; each tier adds rings, pylons or taller frames.
- **Controller:** a star-chart screen lists only destinations the current tier can reach, by catalog name.
- **Arrival:** the first visit to a planet generates a small landing platform, which is the way home.

**Multiblock design — locked**

The gate grows in concentric rings: each tier adds an outer ring of that tier's material, so a T6 gate shows the whole journey from Nullifite at the center to Solvane outside.

| Part | Role |
| --- | --- |
| Gate Controller | Front edge of the frame; star chart screen, FE buffer, upgrade slots |
| Pad Plates | Center floor where players stand; size sets capacity |
| Frame Rings | One ring per tier, in that tier's metal |
| Pylons | Corner towers; count and height grow with tier; light up while charging |
| Energy Ports | FE inputs built into the frame |
| Lens Housing | On the arch above the pad; holds the focus crystal |

| Tier | Footprint | Pad | Adds |
| --- | --- | --- | --- |
| T1 | 5×5 | 3×3 | Nullifite frame, 4 short pylons, 1 energy port |
| T2 | 7×7 | 3×3 | Moonsteel ring, low arch with Selenite lens |
| T3 | 9×9 | 5×5 | Cerulon ring, 8 pylons, 2 energy ports |
| T4 | 11×11 | 5×5 | Skarn ring, taller half-arch |
| T5 | 13×13 | 7×7 | Eidolon ring, full arch, 4 energy ports |
| T6 | 15×15 | 7×7 | Solvane ring, full standing ring gate with crown |

Height grows from about 3 blocks at T1 to about 12 at T6.

- **Building:** the controller projects a ghost preview of the next tier; the structure forms automatically when complete. Breaking a part drops the gate back a tier until repaired.
- **Upgrade slots:** 1 at T1, 2 at T3, 3 at T5, 4 at T6.

| Upgrade | Effect |
| --- | --- |
| Refracting Lens | Lowers FE cost |
| Cryo Core | Charges faster |
| Star Map Fragments | Reveal hidden planets as destinations |
| Capacity Coil | +2 passengers |

## Energy, charging and launch animation

Each jump costs FE and requires a full charge first. Cost scales with tier, with distance (inter-galaxy costs more) and with passenger count.

**Cost per jump (locked, moderate):** listed costs are for a jump to the tier's farthest galaxy; jumps within the current galaxy cost 25%. Each extra passenger adds 10%.

| Tier | FE per jump |
| --- | --- |
| T1 | 500k |
| T2 | 1M |
| T3 | 3M |
| T4 | 8M |
| T5 | 20M |
| T6 | 50M |

**Charging**

- Each tier has its own FE buffer.
- Pylons light up one at a time, the ring spins faster, and a hum rises in pitch as the buffer fills.
- The controller shows a charge bar; "Engage" unlocks at full charge.

**Launch sequence (about 5 seconds)**

1. Lock-on: particle streams spiral from the pylons into the core.
2. Rift: a shattered-void crack opens in the center of the gate.
3. Lift: players float up as the view stretches and blurs.
4. Flash: white-out, then a custom loading screen zooming from the galaxy to the target planet.
5. Arrival: players drift down onto the landing platform with slow fall.

**Tech notes:** GeckoLib for the animated ring and pylons. Confirm the NeoForge 1.21.1 event for custom dimension transition screens during implementation.

## Returning home and co-op trips

The teleporter carries everyone standing on the pad, up to the tier's capacity; the landing platform brings the group home.

**Coming back**

- **Landing platform:** charges slowly from a small local source (solar or a crystal cell); free, but you wait. Sends everyone standing on it home together.
- **Recall Anchor:** crafted and bound to the home gate. Pulls the holder home instantly from the home buffer, with a cooldown and extra cost.
- **Group Anchor:** higher-tier version that pulls back teammates within a small radius, at a high energy cost.
- Dying on a planet sends the player to their normal respawn point.
- The return plays the launch animation in reverse at the home gate.

**Co-op launch**

- The pad zone glows when a player or tamed pet steps on it.
- The owner hits "Engage"; everyone on the pad gets a ready-check with a short countdown and can step off to back out.
- Tamed pets and leashed mobs travel; hostile mobs and dropped items do not.

**Permissions**

- Only the owner or their team/claim members can activate a gate, via FTB Teams or Open Parties and Claims.
- Optional public mode for a spawn hub gate.

## Ores

Each Resource planet has 8 ores that mirror the 8 vanilla Overworld ores, so players know each ore's job at a glance. Sol keeps vanilla ores plus Nullifite, the T1 ore, and the Moon and Mars add the T2 materials; each rare gem is named after its planet and builds the next teleporter tier.

**Role template**

| Vanilla ore | Role | Used for |
| --- | --- | --- |
| Coal | Fuel | Smelting, generators |
| Copper | Common metal | Basic parts, wiring |
| Iron | Standard metal | Frames, machines |
| Gold | Precious metal | Circuits, upgrades |
| Redstone | Energy dust | Teleporter coils, power |
| Lapis | Lore gem | Enchanting, star charts |
| Diamond | Rare gem | Next teleporter tier |
| Emerald | Trade gem | Currency for alien traders |

**Moon and Mars (Sol) — locked**

The T2 recipe needs both worlds: Moonsteel frames, a Selenite lens and an Aresite core.

| World | Material | Notes |
| --- | --- | --- |
| Moon | Regolith Dust | Common; smelts into lunar glass |
| Moon | Moonsteel | Metal for T2 frames |
| Moon | Selenite | Pale crystal; T2 focus lens |
| Mars | Ferrox | Rust-red iron-oxide metal |
| Mars | Olympium | Heavy metal, after Olympus Mons |
| Mars | Aresite | Red gem; T2 core |

**Cerulon (Galaxy 2) — locked**

| Role | Ore | Notes |
| --- | --- | --- |
| Fuel | Nebulite | Dark blue coal, burns twice as long |
| Common metal | Cobaltium | Basic parts and wiring |
| Standard metal | Cyrrium | Frames and machine casings |
| Precious metal | Aurelion | Circuits and upgrades |
| Energy dust | Pulsar Dust | Glows and pulses; teleporter coils |
| Lore gem | Starlite | Star charts and enchanting |
| Rare gem | Cerulite | Key T3 teleporter material |
| Trade gem | Lumenite | Currency for alien traders |

**Skarn (Galaxy 3) — locked**

Dark rock with ember-orange cracks, after real skarn (where magma meets limestone).

| Role | Ore | Notes |
| --- | --- | --- |
| Fuel | Emberite | Coal with glowing seams |
| Common metal | Ruskite | Rust-red basic metal |
| Standard metal | Tectium | Heavy plate metal |
| Precious metal | Pyrium | Fire-gold for high-tier circuits |
| Energy dust | Tremor Dust | Crackles and sparks |
| Lore gem | Rift Opal | Faint void swirls; lore and enchanting |
| Rare gem | Skarnite | Key T4 teleporter material |
| Trade gem | Cinnabrite | Red crystal, after cinnabar |

**Eidolon (Galaxy 4) — locked**

Frozen graveyard of old wrecks: pale ice-white and ghostly cyan; some ores are salvaged rather than natural.

| Role | Ore | Notes |
| --- | --- | --- |
| Fuel | Cryocite | Frozen fuel crystals, burn cold and blue |
| Common metal | Salvium | Scrap metal salvaged from wrecks |
| Standard metal | Wraithsteel | Pale, ghostly steel |
| Precious metal | Palladine | White precious metal |
| Energy dust | Spectral Dust | Faint ghostly glow |
| Lore gem | Remnant Shard | Memory fragments; main lore source |
| Rare gem | Eidolite | Key T5 teleporter material |
| Trade gem | Rimeglass | Frost crystal valued by traders |

**Solvane (Galaxy 5) — locked**

Endgame world around a fading sun: molten gold, white-hot and deep crimson; ores feel like pieces of a dying star.

| Role | Ore | Notes |
| --- | --- | --- |
| Fuel | Coronite | Frozen solar plasma; strongest fuel in the mod |
| Common metal | Photium | Light metal that faintly glows |
| Standard metal | Astrium | Star-forged steel for endgame frames |
| Precious metal | Radiantine | Gold that gives off light |
| Energy dust | Fusion Dust | Top-tier energy dust; powers T6 |
| Lore gem | Nova Pearl | Holds the final chapter of the lore |
| Rare gem | Solvanite | Key T6 teleporter material |
| Trade gem | Dawnstone | Rarest trade currency |

## Item forms and textures

Every role has the same item set on every planet, drawn from one template per role and recolored per planet.

| Role | Ore drops | Items | Blocks |
| --- | --- | --- | --- |
| Fuel | Fuel item | Fuel | Fuel block |
| Common, standard, precious metals | Raw ore | Raw, ingot, nugget | Ingot block, raw block |
| Energy dust | 4–5 dust | Dust | Dust block |
| Lore gem | 4–8 gems | Gem | Gem block |
| Rare gem | 1 gem | Gem | Gem block |
| Trade gem | 1 gem | Gem | Gem block |

- One ore block per planet, set in that planet's own stone; no deepslate-style second variant.
- Nullifite comes in deepslate only and drops raw ore.
- About 33 textures per planet, around 150 in total including Sol.

**Texture rules**

- One base shape per role (8 shapes total), recolored per planet so the role is recognizable on sight.
- Each planet has a 4–5 color palette:

| World | Palette |
| --- | --- |
| Nullifite | Near-black with violet-white fracture lines |
| Moon | Grey-white |
| Mars | Rust red and ochre |
| Cerulon | Deep blue and cyan |
| Skarn | Charcoal and ember orange |
| Eidolon | Ice white and ghostly cyan |
| Solvane | Molten gold, white-hot and crimson |

- Energy dusts, Emberite seams and Nullifite cracks use emissive overlays, plus a slow pulse via animated `.mcmeta` textures.
- Nullifite's pulsing "shattered void" cracks set the visual language for the whole mod.

## Ore generation

Each role spawns like its vanilla counterpart so mining instincts carry over, with one twist per planet. Numbers are starting points for playtesting; planets use vanilla height (Y -64 to 320).

| Role | Y range | Per chunk | Vein size |
| --- | --- | --- | --- |
| Fuel | 0 to 192 | \~20 | Large (\~15) |
| Common metal | -16 to 112 | \~16 | Large (\~10) |
| Standard metal | -24 to 56 | \~10 | Medium (\~9) |
| Precious metal | -64 to 32 | \~4 | Medium (\~8) |
| Energy dust | -64 to 16 | \~6 | Medium (\~8) |
| Lore gem | -32 to 32 | \~2 | Small (\~6) |
| Rare gem | -64 to 16 | \~1 | Tiny (2–4), reduced when exposed to air |
| Trade gem | One terrain type per planet | Rare | Single blocks |

**Per-planet twists**

- Cerulon: Cerulite grows in crystal geodes instead of veins.
- Skarn: ores cluster where lava meets stone; better loot, more danger.
- Eidolon: Salvium comes mostly from wrecks, with only small veins.
- Solvane: ores sit near molten surface flows, adding heat hazards.

**Sol**

- Nullifite: Y -64 to -40, deepslate only, veins of 1–2, rarer than diamond; more common in the Deep Dark.
- Moon: Regolith Dust on the surface, Moonsteel mid-depth, Selenite in deep geodes.
- Mars: Ferrox common, Olympium deep, Aresite rare and deep.

**Implementation:** all Java. Ore features are defined in code and written as registry data via datagen (`DatapackBuiltinEntriesProvider`), so server owners can still override rates with a datapack. Optional `ModConfigSpec` setting for a global rarity multiplier.

## Blocks

Every world gets its own custom terrain blocks; each base stone also gets a building set (polished, bricks, chiseled, plus stairs, slab and wall for the bricks).

**Moon and Mars (Sol) — locked**

Realistic and barren, as the first step off Earth.

| World | Block | Notes |
| --- | --- | --- |
| Moon | Lunar Stone | Base stone; light grey building set |
| Moon | Regolith | Grey surface dust; falls like sand |
| Moon | Mare Basalt | Dark volcanic plains; dark grey building set |
| Moon | Crater Ice | Ice in permanently shadowed craters |
| Moon | Lunar Lichen | Sparse ground cover |
| Moon | Selenite Lamp | Pale, soft light |
| Mars | Martian Stone | Rust-red base stone; full building set |
| Mars | Rustsand | Red surface dust; falls like sand |
| Mars | Oxide Crust | Cracked, iron-rich surface layer |
| Mars | Polar Frost | Dry-ice caps at the poles; slows and chills |
| Mars | Rust Lichen | Hardy red ground cover |
| Mars | Olympium Plating | Heavy metal decor; first industrial palette |

**Cerulon (Galaxy 2) — locked**

| Type | Block | Notes |
| --- | --- | --- |
| Terrain | Cerulean Stone | Base stone; holds all Cerulon ores |
| Terrain | Crystal Sand | Surface sand; smelts into Crystal Glass |
| Terrain | Azure Moss | Blue grass-like surface cover |
| Terrain | Cerulean Geode set | Geode Shell, Budding Crystal, glowing Crystal Clusters; Cerulite inside |
| Plant | Starbloom | Glowing flower, dye source |
| Plant | Shardwood tree | Crystalline leaves; full wood set |
| Decor | Pulsar Lamp | Pulsing light from Pulsar Dust |

**Skarn (Galaxy 3) — locked**

Dark rock against pale marble, after real skarn (where magma meets limestone). Skarn Rock and Scorched Marble both get full building sets.

| Type | Block | Notes |
| --- | --- | --- |
| Terrain | Skarn Rock | Dark base stone; holds all Skarn ores |
| Terrain | Scorched Marble | Pale stone with orange veins, in contact zones |
| Terrain | Slag | Loose, gravel-like surface layer |
| Terrain | Ember Crust | Glowing surface; hurts to stand on |
| Terrain | Rift Glass | Void-cracked crystal around fracture zones; signature block |
| Plant | Emberthorn | Dry thorn bush; damages on contact |
| Plant | Cinder Cap | Glowing cave fungus |
| Plant | Charwood tree | Burnt, blackened tree; full wood set |
| Decor | Tremor Lamp | Flickering light from Tremor Dust |

**Eidolon (Galaxy 4) — locked**

Natural ice terrain plus salvageable wrecks. Permafrost gets a stone building set; Hull Plating gets a sci-fi industrial set, the mod's first metal-style palette.

| Type | Block | Notes |
| --- | --- | --- |
| Terrain | Permafrost | Base stone; holds all Eidolon ores |
| Terrain | Frozen Regolith | Frosty surface layer |
| Terrain | Phantom Ice | Translucent ice that glows faintly; signature block |
| Derelict | Hull Plating, Corroded Hull | Wreck walls and floors |
| Derelict | Broken Console | Lore block; gives Remnant Shards and story fragments |
| Derelict | Cryo Pod | Wreck decor that can hold loot |
| Plant | Frostfern | Hardy ground cover |
| Plant | Ghostbloom | Pale glowing flower near wrecks |
| Plant | Hoarwood tree | Frost-covered tree; full wood set |
| Decor | Spectral Lantern | Ghostly light from Spectral Dust |

**Solvane (Galaxy 5) — locked**

The most dangerous world and the best to build with. Solar Stone gets a full building set, plus Radiant Bricks as the endgame luxury block.

| Type | Block | Notes |
| --- | --- | --- |
| Terrain | Solar Stone | Base stone; holds all Solvane ores |
| Terrain | Corona Crust | White-hot glowing surface; burns |
| Terrain | Sunspot Rock | Cooled patches that are safe to stand on |
| Terrain | Slag Glass | Glassy layer where old flows cooled |
| Terrain | Flare Vent | Erupts fire geysers on a timer; signature block |
| Plant | Solflower | Heat-proof flower that turns toward the sun |
| Plant | Pyrevine | Glowing vines hanging in caves |
| Plant | Gildwood tree | Gold-barked tree; full wood set |
| Decor | Radiant Bricks | Gold-trimmed bricks that glow softly |
| Decor | Fusion Lamp | Brightest light in the mod, from Fusion Dust |

**Wasteland generation — locked**

Wastelands use Terralith-style terrain built with custom blocks. Each type has its own noise settings and density functions for dramatic shapes (canyons, spires, craters, trenches) and 3–5 biomes with surface rules, all in Java via datagen. Galaxies are told apart by per-galaxy sky, fog and water colors, plus block color tinting so one grayscale texture can be recolored per galaxy.

| Wasteland | Biomes | Custom blocks |
| --- | --- | --- |
| Ocean | Deep trenches, kelp jungles, island chains | Abyssal Stone, Tidesand, Brine Crystal, Glowkelp |
| Desert | Dune seas, mesa canyons, salt flats | Sunbaked Stone, Dunesand, Salt Crust, Ruinstone |
| Volcanic | Basalt fields, ash plains, lava lakes | Scoria, Ashfall layer, Vent Rock (smokes, burns), Glassy Obsidian |
| Frozen | Glaciers, ice-spike forests, frozen canyons | Frostrock, Snowpack layer, Glacial Ice (slippery), Frost Crystal |
| Toxic | Acid swamps, mud flats, moss bogs | Sludgestone, Acid fluid, Toxic Mud, Blightmoss |
| Crystal | Prism fields, crystal caverns | Prismstone, Prism Cluster (budding), Shimmer Sand, Refracting Glass |
| Barren | Cratered plains, badlands, canyon scars | Craterstone, Dust layer, Meteorite Fragment (drops small loot) |

**Wasteland signature content — locked**

Every wasteland reward feeds an upgrade system, so each type is worth visiting.

| Wasteland | Signature block | Mob | Structure | Reward |
| --- | --- | --- | --- | --- |
| Ocean | Brine Crystal | Tidewraith | Sunken Relay | Abyssal Pearl: water-breathing armor upgrade |
| Desert | Ruinstone | Dune Burrower | Buried Observatory | Star Map Fragments: reveal hidden planets on the star chart |
| Volcanic | Vent Rock | Ash Strider | Collapsed Forge | Heatproof Plating: fire-resistance armor upgrade |
| Frozen | Frost Crystal | Rime Stalker | Frozen Outpost | Cryo Core: machine speed upgrade |
| Toxic | Acid fluid | Bog Lurker | Sunken Lab | Neutralizer: poison-immunity armor upgrade |
| Crystal | Prism Cluster | Amethyst Stalker | Prism Spire | Refracting Lens: teleporter upgrade that cuts FE cost |
| Barren | Meteorite Fragment | Crater Drifter | Impact Site | Stardust: universal crafting catalyst |

**Stone families**

All 15 stones (8 planet stones and 7 wasteland stones) get a full family, like vanilla stone plus blackstone. Wasteland families stay grayscale and are tinted per galaxy.

| Variant | How it's made |
| --- | --- |
| Base stone | Drops cobbled; Silk Touch keeps it |
| Cobbled | Mining the base stone |
| Smooth | Smelt the base stone |
| Polished | 4 base stone |
| Bricks | 4 polished |
| Cracked bricks | Smelt bricks |
| Chiseled | 2 polished slabs |
| Polished black | 8 polished + 1 Nullifite nugget |
| Polished black bricks | 4 polished black |
| Chiseled polished black | 2 polished black slabs |

Every variant, including cracked and chiseled, gets stairs, a slab and a wall (30 shape blocks per family). Hull Plating, Corroded Hull, Radiant Bricks, Olympium Plating, Sunspot Rock, Oxide Crust, Ruinstone, Salt Crust, Slag and Frozen Regolith also get stairs, slabs and walls.

Cobbled smelts back into the base stone, and the stonecutter makes every variant and shape. Every sand smelts into its own glass (Lunar, Rust, Crystal, Frost, Tide, Dune, Shimmer), and the four woods get stairs and slabs.

## Mobs

Every world gets an ambient or neutral mob and a threat; each galaxy's key world has a guardian boss whose defeat unlocks the next tier's gate item. Eight mobs come from the existing Shattered Skies roster, and their three style variants map to galaxies (e.g. Meteor Maw: Ironfall in Sol, Comet in Galaxy 2, Voidstone deeper).

| World | Mob | Role | Source |
| --- | --- | --- | --- |
| Moon | Meteor Maw | Threat during meteor events | Shattered Skies |
| Moon | Regolith Crawler | Burrows under dust and ambushes | New |
| Mars | Rust Beetle | Neutral; drops Ferrox bits | New |
| Mars | Stormbitten Wyvern | Threat during dust storms | Shattered Skies |
| Cerulon | Mossback | Roams Azure Moss plains | Shattered Skies |
| Cerulon | Crystal Stag | Passive; shear antlers for Starlite | New |
| Cerulon | Prismling (renamed; Shardling is a Shattered Skies minion) | Small crystal mob that shatters when hit | New |
| Crystal wasteland | Amethyst Stalker | Crystal predator | Shattered Skies |
| Skarn | Slagjaw | Stone golem with ore teeth | Shattered Skies |
| Skarn | Shardmother | Broodmother in rift zones | Shattered Skies |
| Skarn | Cinder Hound | Hunts in packs on Ember Crust | New |
| Eidolon | Hollow Sentinel | Haunts wrecks | Shattered Skies |
| Eidolon | Frost Warden | Mini-boss guarding big wrecks | New |
| Solvane | Flare Sprite | Flying fire spirit near Flare Vents | New |
| Solvane | Sun Colossus | Slow giant mini-boss of Solar Stone | New |
| Ocean wasteland | Tidewraith | Coral and kelp flyer | Shattered Skies |

**Boss adds:** Splinter Mite (melee crystal beetle) and Splinter Wisp (floating shard that must die to drop a boss shield), from Shattered Skies.

**Guardian bosses**

| Galaxy | Boss | Concept |
| --- | --- | --- |
| 2 | Prism Sentinel | Crystal construct |
| 3 | Rift Tyrant | Tears the arena apart |
| 4 | Eidolon Captain | Ghost of the fleet commander |
| 5 | The Dying Star | Final boss; Archon Vael fused with Solvane's dying sun |

Each wasteland type's mob is listed with its signature content under Blocks.

**Food and utility mobs**

Eleven more mobs make food a reason to explore every world: six passive, one neutral and four hostile. All stats are proposals for playtesting.

| World | Mob | Type | Drops |
| --- | --- | --- | --- |
| Moon | Moon Hopper | Passive; hops 4 blocks high | Hopper Meat, Hopper Fluff |
| Mars | Dust Grazer | Passive herd; stampedes when hit | Grazer Steak, Grazer Hide |
| Cerulon | Azure Fowl | Passive; glides, lays Blue Eggs | Raw Fowl, Azure Feather |
| Cerulon | Glimmerfish | Passive schools; lights the water | Glimmerfish, Glimmer Scale |
| Skarn | Slag Boar | Neutral; charges when provoked | Boar Chop, Boar Tusk |
| Skarn | Scorch Wyrmling | Hostile; spits fire bolts | Scorch Tail, Scorch Scale |
| Eidolon | Frost Yak | Passive; shear for wool, milk for Frost Milk | Yak Meat, Yak Wool |
| Eidolon | Ice Leech | Hostile; latches on and drains hunger | Leech Gel |
| Solvane | Gildcrab | Passive; pinches when attacked | Gildcrab Meat, Gildcrab Shell |
| Ocean wasteland | Deep Eel | Hostile in water | Eel Fillet, Eel Skin |
| Desert wasteland | Sand Skitter | Hostile; poison sting | Skitter Leg, Skitter Carapace, Venom Gland |

Existing mobs also drop food now: Regolith Crawler (Crawler Leg), Rust Beetle (Beetle Grub), Crystal Stag (Stag Venison), Dune Burrower (Burrower Steak) and Bog Lurker (Lurker Leg, Venom Gland).

## Food

Every hunted mob drops a raw meat that cooks in a furnace, smoker or campfire; mobs killed while on fire drop it cooked. Dishes combine ingredients from several worlds for long effects.

| Dish | Ingredients | Hunger | Effect |
| --- | --- | --- | --- |
| Astronaut Ration | Baked Tuber, Seared Grazer Steak, Lichen Crisps | 10 | Stacks to 16; eaten twice as fast |
| Orbit Burger | Bread, Seared Grazer Steak, Skyberries | 10 | None |
| Nebula Pie | Skyberries, Blue Egg, Shardwood Syrup, sugar | 8 | Night Vision 60 s |
| Ember Chili | Smoked Boar Chop, Grilled Scorch Tail, Cinder Cap, bowl | 10 | Fire Resistance 3 min, Strength I 30 s |
| Cryo Chowder | Yak Roast, Frost Milk, Frostfern, bowl | 10 | Freeze immunity 3 min, Resistance I 30 s |
| Starfall Feast | Cooked Gildcrab, Pyrefruit, Roasted Solflower Seeds, bowl | 12 | Regeneration II 10 s, Absorption II 2 min |
| Low-G Jelly | Leech Gel, Stardust, sugar | 3 | Slow Falling and Jump Boost II 60 s |
| Ration Pack | Wreck loot, or Yak Roast + Baked Tuber + Salvium nugget | 6 | Never spoils |

- **Meats (15 raw, 15 cooked):** Crawler Leg, Hopper Meat, Grazer Steak, Beetle Grub, Stag Venison, Raw Fowl, Glimmerfish, Boar Chop, Scorch Tail, Yak Meat, Gildcrab Meat, Eel Fillet, Burrower Steak, Lurker Leg and Skitter Leg. Cooked meats give 5–8 hunger; a few carry effects (Grilled Scorch Tail: Fire Resistance; Cooked Glimmerfish: Night Vision; Cooked Hopper: Jump Boost; Cooked Gildcrab: Absorption).
- **Crops and forage:** Rust Tuber (Mars crop), Lichen Crisps, Skyberries, Shardwood Syrup, Cinder Cap Stew, Frostfern Tea, Frost Milk, Blue Egg, Pyrefruit and Solflower Seeds.
- **Other drops:** Hopper Fluff, Grazer Hide, Azure Feather, Glimmer Scale, Boar Tusk, Scorch Scale, Yak Wool, Leech Gel, Gildcrab Shell, Eel Skin, Skitter Carapace and Venom Gland, plus the wasteland rewards, boss trophies and gate keys as items.

## Gear

Each armor and tool set also protects against the next world's hazards. Every set includes the 5 vanilla tools (sword, pickaxe, axe, shovel, hoe).

| Set | Made from | Strength | Set bonus |
| --- | --- | --- | --- |
| Nullifite | Nullifite ingots | Level 5: just above netherite | Null Step: no fall damage |
| Olympium | Olympium + Moonsteel | Level 8: well above netherite | Dust Shield: immune to storm and dust effects |
| Cerulite | Cerulite + Cyrrium | Level 11: well above netherite | Crystal Sight: night vision; nearby ores glow faintly |
| Skarnite | Skarnite + Tectium | Level 14: far above netherite | Ember Walk: fire immunity; safe on Ember Crust and lava |
| Eidolite | Eidolite + Wraithsteel | Level 17: far above netherite | Phantom Veil: freeze immunity; invisible while sneaking |
| Solvanite | Solvanite + Astrium | Level 20: endgame | Starborne: creative flight; immune to every planet hazard |

**Progression rules**

- Mining gates: see the Mining ladder below. Nullifite needs netherite; each later ore needs the pickaxe before it.
- Upgrade path (v1.3): like netherite, every set after Nullifite is made at the smithing table from the previous set on the mining ladder: template + previous piece + the new set's ingot or gem; enchantments and trims carry over. Nullifite is crafted from ingots, like diamond. The chain is Nullifite → Ferrox → Moonsteel → Olympium → Cobaltium → Cyrrium → Cerulite → Ruskite → Tectium → Skarnite → Salvium → Wraithsteel → Eidolite → Photium → Astrium → Solvanite; the precious sets branch off their world's entry set (Aurelion from Olympium, Pyrium from Cerulite, Palladine from Skarnite, Radiantine from Eidolite). Templates are found in their tier's structure (Mars Crash Site, Prism Spire, Collapsed Forge, Derelict Wreck, Solar Shrine) and copied with 7 of the base set's material + the template + that place's stone. See pending-data/upgrade-templates and sheets/gear/upgrade_chain.png.
- Hazard gates: Skarn's burning ground needs fire protection; Solvane's heat needs Skarnite gear or Heatproof Plating.



**Mining ladder (v1.3, locked)**

Allthemodium-style: every ZeroG pickaxe out-mines netherite, and every ZeroG ore needs at least a netherite pickaxe. Nullifite, the first ZeroG ore, needs netherite; after that, each world's first metal needs the best pickaxe from the world before, and inside a world the order is common metal, then standard metal, then the rare gem. Precious (gold-style) picks share their world's common level but mine faster. Fuels and energy dusts only need an iron pickaxe, so power is never blocked.

| Level | Pickaxe | World | Opens these ores | Mining speed | Lore |
| --- | --- | --- | --- | --- | --- |
| 4 | Netherite (vanilla) | Overworld | Nullifite | 9 | The entry ticket to space. |
| 5 | Nullifite | Sol (Overworld) | Ferrox | 9.5 | Void-glass edge: the first pick that can bite into off-world rock. |
| 6 | Ferrox | Mars | Moonsteel | 10 | Rust-hardened iron oxide; tough enough for lunar metal. |
| 7 | Moonsteel | Moon | Selenite, Olympium | 10.5 | Forged in low gravity, so its edge holds against crystal and Olympus basalt. |
| 8 | Olympium | Mars | Aresite, Cobaltium | 11 | Heavy Olympus metal alloyed with Moonsteel; opens the T2 gate materials. |
| 9 | Cobaltium / Aurelion | Cerulon | Aurelion, Starlite, Lumenite, Cyrrium | 11.5, 15.5 (gold-style) | Cerulon's workhorse metals. Aurelion is gold-style: same level, faster, fragile. |
| 10 | Cyrrium | Cerulon | Cerulite | 12 | Tempered casing steel; cuts the Cerulite geodes. |
| 11 | Cerulite | Cerulon | Ruskite | 12.5 | Crystal edge (T3). The only pick that survives Skarn heat. |
| 12 | Ruskite / Pyrium | Skarn | Pyrium, Rift Opal, Cinnabrite, Tectium | 13, 17 (gold-style) | Heat-scaled metals. Pyrium is gold-style: same level, faster, fragile. |
| 13 | Tectium | Skarn | Skarnite | 13.5 | Plate metal heavy enough to crack Skarnite seams. |
| 14 | Skarnite | Skarn | Salvium | 14 | Ember gem edge (T4); stays sharp in Eidolon's cold. |
| 15 | Salvium / Palladine | Eidolon | Palladine, Remnant Shard, Rimeglass, Wraithsteel | 14.5, 18.5 (gold-style) | Salvaged wreck steel. Palladine is gold-style: same level, faster, fragile. |
| 16 | Wraithsteel | Eidolon | Eidolite | 15 | Ghost-pale steel that reaches Eidolite through permafrost. |
| 17 | Eidolite | Eidolon | Photium | 15.5 | Phantom gem edge (T5); does not melt near a dying star. |
| 18 | Photium / Radiantine | Solvane | Radiantine, Nova Pearl, Dawnstone, Astrium | 16, 20 (gold-style) | Light metals of the fading sun. Radiantine is gold-style: same level, faster, fragile. |
| 19 | Astrium | Solvane | Solvanite | 16.5 | Star-forged steel; the last step before the heart of Solvane. |
| 20 | Solvanite | Solvane | everything | 17 | Endgame (T6). Mines everything in the mod. |

| Ore | Needs | Why |
| --- | --- | --- |
| Deepslate Nullifite Ore | Netherite pickaxe or better | Deep Overworld void veins; diamond shatters on them, so netherite is the minimum. |
| Ferrox Ore | Nullifite pickaxe or better | First Mars metal; needs the Nullifite pick you came with. |
| Moonsteel Ore | Ferrox pickaxe or better | Lunar steel is harder than Martian rust; mine it with Ferrox. |
| Selenite Ore | Moonsteel pickaxe or better | Pale lens crystal splinters under anything weaker than Moonsteel. |
| Olympium Ore | Moonsteel pickaxe or better | Olympus basalt needs a low-gravity Moonsteel edge. |
| Aresite Ore | Olympium pickaxe or better | The red T2 core grows inside Olympium veins; mine it with Olympium. |
| Cobaltium Ore | Olympium pickaxe or better | First Cerulon metal; needs the Olympium pick from Sol. |
| Aurelion Ore | Cobaltium pickaxe or better | Soft precious metal in hard blue stone; Cobaltium or better. |
| Starlite Ore | Cobaltium pickaxe or better | Lore gem; Cobaltium or better. |
| Lumenite Ore | Cobaltium pickaxe or better | Trade gem; Cobaltium or better. |
| Cyrrium Ore | Cobaltium pickaxe or better | Casing steel; Cobaltium or better. |
| Cerulite Ore | Cyrrium pickaxe or better | Crystal geodes need a tempered Cyrrium pick. |
| Ruskite Ore | Cerulite pickaxe or better | First Skarn metal; only Cerulite survives the heat. |
| Pyrium Ore | Ruskite pickaxe or better | Fire-gold; Ruskite or better. |
| Rift Opal Ore | Ruskite pickaxe or better | Lore gem; Ruskite or better. |
| Cinnabrite Ore | Ruskite pickaxe or better | Trade gem; Ruskite or better. |
| Tectium Ore | Ruskite pickaxe or better | Heavy plate metal; Ruskite or better. |
| Skarnite Ore | Tectium pickaxe or better | Ember seams crack only under Tectium. |
| Salvium Ore | Skarnite pickaxe or better | First Eidolon metal (wreck scrap); needs the Skarnite pick. |
| Palladine Ore | Salvium pickaxe or better | White precious metal; Salvium or better. |
| Remnant Shard Ore | Salvium pickaxe or better | Lore gem; Salvium or better. |
| Rimeglass Ore | Salvium pickaxe or better | Trade gem; Salvium or better. |
| Wraithsteel Ore | Salvium pickaxe or better | Ghost steel; Salvium or better. |
| Eidolite Ore | Wraithsteel pickaxe or better | Phantom gem deep in permafrost; Wraithsteel only. |
| Photium Ore | Eidolite pickaxe or better | First Solvane metal; needs the Eidolite pick. |
| Radiantine Ore | Photium pickaxe or better | Light-gold; Photium or better. |
| Nova Pearl Ore | Photium pickaxe or better | Lore gem; Photium or better. |
| Dawnstone Ore | Photium pickaxe or better | Trade gem; Photium or better. |
| Astrium Ore | Photium pickaxe or better | Star-forged steel; Photium or better. |
| Solvanite Ore | Astrium pickaxe or better | Dying-star gem; Astrium only. |

Code: each set's `SimpleTier` uses `zerog_tweaks:incorrect_for_<set>_tool`; ores are in `zerog_tweaks:needs_<pick>_tool`, and the vanilla `incorrect_for_*_tool` tags lock wood to netherite out of everything above them. The tags are generated in `pending-data/mining-tags/` (copy `data/` onto `src/main/resources/data/`).

**Armor upgrades** (smithing table, stored as data components). One slot per piece for Nullifite to Cerulite; two from Skarnite onward.

| Piece | Upgrade | Effect |
| --- | --- | --- |
| Helmet | Abyssal Pearl | Water breathing |
| Chestplate | Heatproof Plating | Fire resistance |
| Leggings | Neutralizer | Poison immunity |
| Boots | Grav Boots (from Stardust) | Adjust how gravity affects you |

**Metal gear sets**

Every metal also gets a full set (5 tools + 4 armor pieces), sitting between the main gem sets. Common metals are cheap and sturdy, standard metals are the solid workhorse, and precious metals play like gold: fast and highly enchantable, but fragile. Every set is above netherite; exact numbers are in the stats table below and are starting points for playtesting.

| Set | World | Metal role | Strength | Full-set perk |
| --- | --- | --- | --- | --- |
| Ferrox | Sol (Mars) | Common | Level 6: just above netherite | Sturdy: +1 armor toughness |
| Moonsteel | Sol (Moon) | Standard | Level 7: well above netherite | Lunar Stride: 50% less fall damage |
| Cobaltium | Cerulon | Common | Level 9: well above netherite | Quick Hands: +10% mining speed |
| Cyrrium | Cerulon | Standard | Level 10: well above netherite | Tempered: +20% durability |
| Aurelion | Cerulon | Precious | Level 9: well above netherite; gold-style | Silver Tongue: better alien trader prices |
| Ruskite | Skarn | Common | Level 12: far above netherite | Heat Scale: 25% less fire damage |
| Tectium | Skarn | Standard | Level 13: far above netherite | Anchored: knockback resistance |
| Pyrium | Skarn | Precious | Level 12: far above netherite; gold-style | Kindled: tools auto-smelt ores 20% of the time |
| Salvium | Eidolon | Common | Level 15: far above netherite | Scrapper: extra Salvium from wreck blocks |
| Wraithsteel | Eidolon | Standard | Level 16: far above netherite | Chill Guard: slowness immunity |
| Palladine | Eidolon | Precious | Level 15: far above netherite; gold-style | Lucky: +1 Fortune and Looting |
| Photium | Solvane | Common | Level 18: near endgame | Glow: lights the area around the player |
| Astrium | Solvane | Standard | Level 19: near endgame | Star Forged: +2 max health |
| Radiantine | Solvane | Precious | Level 18: near endgame; gold-style | Radiant: +20% damage to undead and Splinter creatures |

**Gear stats and abilities (v1.3, locked)**

Every set is above netherite and gets stronger with its mining-ladder level. Netherite reference: armor 3/8/6/3 (20), toughness 3, 10% knockback resistance, 1.3× diamond durability, sword damage 8. Armor stays at or under 30 points because Minecraft caps armor at 30; higher sets grow mostly in toughness. Durability is relative to diamond. Gold-style sets (Aurelion, Pyrium, Palladine, Radiantine) trade armor, toughness and durability for speed and enchantability.

| Set | Tier | Level | Armor (helm/chest/legs/boots) | Toughness | Knockback resist | Durability | Sword damage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *Netherite (vanilla)* | | 4 | 3/8/6/3 (20) | 3 | 10% | 1.3× | 8 |
| Nullifite | T1 | 5 | 4/8/6/3 (21) | 3.5 | 11% | 1.4× | 8.5 |
| Olympium | T2 | 8 | 4/8/6/4 (22) | 5 | 14% | 1.7× | 10 |
| Cerulite | T3 | 11 | 4/9/7/4 (24) | 6.5 | 17% | 2× | 11.5 |
| Skarnite | T4 | 14 | 5/9/7/4 (25) | 8 | 20% | 2.3× | 13 |
| Eidolite | T5 | 17 | 5/10/7/5 (27) | 9.5 | 23% | 2.6× | 14.5 |
| Solvanite | T6 | 20 | 6/10/8/6 (30) | 11 | 26% | 2.9× | 16 |
| Ferrox | Metal | 6 | 4/8/6/3 (21) | 4 | 12% | 1.5× | 9 |
| Moonsteel | Metal | 7 | 4/8/6/4 (22) | 4.5 | 13% | 1.6× | 9.5 |
| Cobaltium | Metal | 9 | 4/9/6/4 (23) | 5.5 | 15% | 1.8× | 10.5 |
| Cyrrium | Metal | 10 | 4/9/6/4 (23) | 6 | 16% | 1.9× | 11 |
| Aurelion | Precious | 9 | 4/8/6/4 (22) | 4.5 | 10% | 1.35× | 10.5 (faster swing) |
| Ruskite | Metal | 12 | 4/9/7/4 (24) | 7 | 18% | 2.1× | 12 |
| Tectium | Metal | 13 | 5/9/7/4 (25) | 7.5 | 19% | 2.2× | 12.5 (slower swing) |
| Pyrium | Precious | 12 | 4/9/6/4 (23) | 6 | 10% | 1.6× | 12 (faster swing) |
| Salvium | Metal | 15 | 5/9/7/5 (26) | 8.5 | 21% | 2.4× | 13.5 |
| Wraithsteel | Metal | 16 | 5/9/7/5 (26) | 9 | 22% | 2.5× | 14 |
| Palladine | Precious | 15 | 5/9/7/4 (25) | 7.5 | 10% | 1.8× | 13.5 (faster swing) |
| Photium | Metal | 18 | 5/10/7/5 (27) | 10 | 24% | 2.7× | 15 |
| Astrium | Metal | 19 | 5/10/8/5 (28) | 10.5 | 25% | 2.8× | 15.5 |
| Radiantine | Precious | 18 | 5/9/7/5 (26) | 9 | 10% | 2.05× | 15 (faster swing) |

Precious sets (Aurelion, Pyrium, Palladine, Radiantine) have enchantability 25 and mine and swing faster, like gold.

**Tool and weapon abilities (T3 and up)**

| Set | Pickaxe and shovel | Axe and hoe | Sword |
| --- | --- | --- | --- |
| Cerulite | Ore Sense: nearby ores glow through walls while sneaking | None | Crystal Edge: 15% chance per hit to burst into shards (3 damage nearby) |
| Skarnite | Ember Touch: toggleable auto-smelt | Axe sets targets on fire | Hits ignite; critical hits leave an ember burst |
| Eidolite | 3×3 mining while sneaking | None | Frostbite: Slowness II and freezing on hit |
| Solvanite | 3×3 mining with auto-smelt | Axe fells whole trees; hoe tills and harvests 5×5 | Solar Flare: hold 2 s to fire a cone of fire (12 damage, 20 s cooldown) |

Area mining, tree felling and 5×5 farming toggle with a keybind, and every ability use costs extra durability.

## Machines

A compact, themed set that makes planet materials useful, runs on FE and works alongside Create and Mekanism.

| Machine | Type | What it does |
| --- | --- | --- |
| Combustion Generator | Power | Burns planet fuels (Nebulite, Emberite, Cryocite, Coronite, each hotter) |
| Solar Array | Power | Output depends on the world: weak on Eidolon, huge near Solvane |
| Fusion Reactor | Power | Endgame generator fed with Fusion Dust; powers T6 jumps |
| Ore Refinery | Processing | Doubles ore output; triples with upgrades |
| Alloy Forge | Processing | Combines metals; rare recipes use Stardust as a catalyst |
| Crystal Growth Chamber | Processing | Slowly grows gems from clusters and energy dust |
| Salvage Station | Processing | Breaks wreck blocks into Salvium and lore items |

- **Casing tiers:** Cyrrium, Tectium, Wraithsteel, Astrium; better casings mean faster, more efficient machines.
- **Upgrades:** Cryo Core for speed; energy dusts (Pulsar, Tremor, Spectral, Fusion) for increasing efficiency.
- **Compatibility:** all FE; Create and Mekanism processors also accept ZeroG ores when installed.

## Lore: The Splintered Concord

The mod's story runs like a campaign in five acts, with a guide, a recurring villain and a choice at the end.

**Hook (approved Prologue revision, Oct 4, 2026):** Nullifite comes from the
Pathfinder's shattered gate core deep beneath Earth. First Raw Nullifite pickup
triggers the Moon relay's Courier reply the next night. Its chest holds Echo's
Dormant Wisp and the Concord Codex; the Broken Console asks refugees to rebuild
the gate. A Dormant Wisp is required to craft the Gate Controller. Echo wakes
asking how long she has been asleep. Existing ore placement and registry IDs
are retained. See [Prologue: The Signal](briefs/prologue_the_signal.md) for the
complete lore and recovery requirements. This replaces the older coincidental
meteor hook without rewriting the five existing acts.

**Characters**

| Character | Role |
| --- | --- |
| Echo | Friendly Splinter Wisp, remnant of the Concord's chief navigator; guides the player through the Codex; remembers each world only after the player reaches it |
| Archon Vael | Concord leader who ordered the null experiments; recurring villain in logs and rift whispers, always one world ahead |
| The Keepers | Guardian constructs still following the Concord's orders |
| The Hollow Fleet | Ghost crew waiting for a rescue that never came |

**Acts**

1. **The Falling Star (Sol):** Meteor Maws bring Concord debris to the Moon. Echo wakes and asks to go home but can't remember where it is. Mars holds the first sign of the Concord: a hand-cut Aresite core.
2. **The Quiet Mines (Cerulon):** the Concord's peaceful mining world. The Prism Sentinel is a test, not a hunt; it asks whether you are Concord, fights in light-refracting phases, and once beaten accepts you as an heir.
3. **The Wound (Skarn):** where Vael tore space open. The Rift Tyrant, his lieutenant fused into the rift, pulls pieces of the arena into the void. Afterward Echo remembers she plotted the course here.
4. **The Frozen Fleet (Eidolon):** the survivors fled here and froze. The Eidolon Captain can be fought, or shown the crew's final log with enough Remnant Shards; then he yields the key and a unique reward.
5. **The Last Light (Solvane):** the Nova Pearl reveals Vael fused himself with the dying sun; the Dying Star is Vael. The Splinter creatures are the Concord, who shattered themselves to hold him back. Earth was meant to be their refuge, so the player has been finishing their migration.

**Ending choice** (per player, using the Heart of Solvane)

| Choice | Outcome |
| --- | --- |
| Rekindle the star | Solvane burns bright; radiant T6 gate crown; Echo stays as a companion |
| Let it fade | Concord remnants go free; void-themed crown; Echo says goodbye in a final Codex entry |

**Side quests:** Sunken Relay (a distress signal still broadcasting), Buried Observatory (leads to a hidden planet), Collapsed Forge (the smith who built the first gate).

**Delivery:** the Codex fills one chapter per galaxy, unlocked through advancements; Echo's lines appear as Codex pages and advancement toasts, so no dialogue system is needed. Starlite, Remnant Shards, Broken Consoles, Star Map Fragments and the Nova Pearl carry the entries.

## Build order

Each milestone leaves something playable to test, even though everything ships together at release.

| Milestone | Scope |
| --- | --- |
| M0 Foundation | Project setup, registries, datagen, config; a material system that registers ore, items, blocks, tags and loot from one definition |
| M1 Sol materials | Nullifite ore and worldgen, Moon and Mars materials, tool tiers and mining gates, Nullifite gear |
| M2 Teleporter core | T1–T2 multiblock with ghost preview, controller, FE buffer, basic star chart, simple teleport, landing platform and return |
| M3 Sol dimensions | Moon and Mars terrain, ores, gravity, hazards (Polar Frost, dust storms); Olympium gear |
| M4 Machines | Generators and processing machines, before T3 energy costs |
| M5 Galaxy system | Slot dimensions, seeded generator, catalog names, star chart listing; tested with 2–3 wasteland types |
| M6 Galaxy 2 | Cerulon blocks, ores and mobs; all 7 wasteland types; Cerulite gear, T3, Prism Sentinel |
| M7–M9 Galaxies 3–5 | One each for Skarn, Eidolon, Solvane: blocks, ores, mobs, boss, gear, next gate tier |
| M10 Travel polish | Launch animation, transition screen, co-op trips, Recall Anchors, gate upgrades |
| M11 Lore | Codex, Echo's lines, advancements, ending choice |
| M12 Balance and compatibility | Create and Mekanism recipes, optional Galacticraft and Ad Astra content, performance testing |

The shared Splinter mobs can live in a small shared library mod that both ZeroG Tweaks and Shattered Skies depend on.

## Liquids

Each world has its own liquid, used in exploration and machines. All six have animated textures (16 frames), a bucket, an underwater fog colour and mixing rules.

| Liquid | Where | In the world | Mixing | Used for |
| --- | --- | --- | --- | --- |
| Acid | Toxic wastelands | Poison II; corrodes armor unless you have the Neutralizer; dissolves dropped items after 5 s | Water: Sludgestone. Lava: Toxic Mud | Bog Lurker habitat; Neutralizer crafting |
| Liquid Starlight | Cerulon crystal caves | Light 12; Slow Falling and Night Vision while swimming | Water: Crystal Sand. Lava: Prismstone | Crystal Growth Chamber input |
| Magma Slag | Skarn lava fields | Slow, thick lava; sets you on fire; flows 3 blocks | Water: Slag. Liquid Starlight: Rift Glass | Alloy Forge heat; Skarn lava lakes |
| Cryo Fluid | Eidolon, frozen wastelands | Slowness II and freezing (Freeze Ward blocks it); freezes water it touches | Water: Glacial Ice. Lava: Frostrock | Machine coolant; Frost Warden arena moat |
| Solar Plasma | Solvane flows | Light 15; burns through Fire Resistance unless you wear Heatproof Plating or Skarnite+ armor | Water: Slag Glass. Cryo Fluid: Sunspot Rock | Fusion Reactor fuel |
| Null Fluid | Deep Dark pools (Earth), Moon craters | Low gravity: you slowly float upward; Nullifite glows brighter nearby | Lava: Deepslate Nullifite Ore | Teleporter coolant; early Nullifite hint |

## Rendering and technical systems

The pieces that make the art work in game, all included in the package.

| System | How it works |
| --- | --- |
| Custom effects | Freeze Ward (freeze immunity; Frostfern Tea, Cryo Chowder) and Surefoot (Slowness immunity; Frost Milk) |
| Acid fluid | Swimmable, slow, poisons anything inside; animated textures, bucket, green underwater fog |
| Wasteland tinting | 308 grayscale blocks tinted by wasteland type × galaxy colour, read from the dimension id (e.g. g3\_p2 = Galaxy 3) |
| Mob models | GeckoLib geo.json, texture, glow mask and idle/walk animations for all 28 mobs; editable in Blockbench |
| Armor models | GeckoLib armor per set: the worn layers plus real 3D extras (horns, crests, halos, pauldrons, wings, fins, spikes) |

Spawn eggs: all 28 mobs, bosses included, using the vanilla egg template with two colours per mob.

Dependency: GeckoLib 4.x for NeoForge 1.21.1.

## Open questions and next phase

Next up is Phase 2: blocks and ores for each galaxy.

- [x] Mod name: ZeroG Tweaks
- [x] T1 Overworld ore named Nullifite
- [x] Ore sets for all four Resource planets
- [x] FE cost per tier and per passenger
- [x] Gravity: per-world values
- [x] Release scope: all 5 galaxies, 5–8 planets each
- [x] Signature block, mob, structure and reward per wasteland type

* [x] Shattered Skies mobs are shared between both projects
