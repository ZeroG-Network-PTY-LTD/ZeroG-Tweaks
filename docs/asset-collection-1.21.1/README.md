# ZeroG — complete design collection for Minecraft 1.21.1

Open `showcases/ZeroG_Full_Collection_1_21_1.bbmodel` in Blockbench. The Outliner groups the collection by use. Each individual model remains available in its source folder; use those projects to play their original animation clips. The combined catalogue intentionally has no animation clips: playing hundreds of entity animations together would not be a meaningful fit test.

This is an **asset and documentation snapshot**, not a new compiled release. Existing gameplay source and release jars on `1.21.1-update` are unchanged. Catalogue geometry keeps authored dimensions; only positions are translated to arrange rows. The complete catalogue uses Blockbench's generic Free format, which supports multiple textures and per-texture UV sizes without Bedrock's single-texture limitation. Individual source entity projects retain their authored formats. The twenty-armour catalogue uses one packed atlas. Both approaches preserve texels and alpha; neither catalogue is an entity intended for runtime export. For a lighter review, open one category showcase instead of the texture-heavy full scene.

## Armour

Twenty sets now use the **user-approved green-box vanilla-fitting silhouette**, replacing the orange-box custom armour geometry. Minecraft 1.21.1 humanoid joint positions are head/body Y24, arms X±5/Y22 and legs X±1.9/Y12. Neutral arm rotations are zero. Open faces, exposed forearms and hands, and independently painted family palettes follow the supplied twenty-material lineup. Hidden medial leg-shell walls are trimmed to X±0.05 to prevent neutral-pose leg z-fighting without changing the outside silhouette. Eight sets include 12-frame animated PNG studies: Nullifite, Moonsteel, Cerulite, Wraithsteel, Eidolite, Astrium, Radiantine and Solvanite. Each loop is 2.4 seconds. Java worn-armour animation/emissive rendering still needs runtime support; a tall PNG plus mcmeta alone does not prove it works on equipment. No detached halo/effect geometry has been added; animated fire/aura treatments remain future work.

The actual vanilla netherite/Sentry/amethyst study is kept locally only. No extracted Mojang source, Steve texture or netherite reference atlas is published in this snapshot. Armour uses an independently painted procedural player reference. Orange-box revisions remain local backups and are excluded from this active collection.

## Bees, apiaries and genetics

The supplied complete non-bee stack contains 85 block models, 65 standalone item models, 85 block-inventory item views, 8 multiblock assemblies, 8 Apiarist/Cosmic wearable projects and separate animation/held-item studies. Frames are inventory inserts, tools use held-item views, armour uses player rigs and multiblocks retain their individual controller/casing layout. Machines, frame housing, jelly, serums, combs, tools, confinement coils and tier assemblies are included as designs.

**Bee entity models are not included.** The earlier rejected bee designs have not been restored. Accepted vanilla Bedrock-style bees with recoloured space textures, original wings/eyes and suitable emissive details remain future work. The Binnie material is a concept translation, not a claim that Binnie's code or artwork was imported.

## Materials, blocks and inventory items

Thirty-nine material families provide 94 blocks (39 ores, 16 raw-storage blocks, 39 processed-storage blocks) and 71 item models. Blocks are full six-faced cubes; materials use transparent front/back inventory geometry. Original 16×16 art is preserved and nearest-neighbour enlarged to 64×64. That enlargement is not claimed as newly painted HD detail. Textures are embedded in the Blockbench projects. Duplicate loose runtime resources are not included or installed by this update.

## Mobs, drops and eggs

The committed mob snapshot retains existing creature designs, Shattered Skies style variants, drop items, coordinated spawn-egg studies, auras and reference sheets. These files are existing committed work, not a claim that every creature has been rebuilt or newly approved. Historical Tidewraith studies are retained for provenance but excluded from the main showcase in favour of the approved pair.

The approved non-boss Tidewraith has the repaired face and body/head connection. The manta-mouth Tidewraith is the boss design, retaining its authored size rather than applying the earlier six-player-height rule. Boss variants retain the shared silhouette, mouth, eight-eye design, articulated tendrils and wing animation studies. Individual source projects retain their clips and palettes. The approved branch's runtime draft is an archive, **not a spawnable-entity implementation installed here**. No fresh jar was built or placed into CurseForge by this asset update.

## Validation and provenance

`catalog.json` lists every packaged file with SHA-256, the immutable mob/approved-Tidewraith source commits, and the exact models selected for the catalogue. The showcase builder checks embedded textures, texture references, atlas packing where used and UV bounds; it preserves authored cube geometry and bone hierarchy. It does not certify every legacy model's animation, symmetry or in-game renderer. Software previews are not GPU captures. Separate emissive textures in individual models remain authoritative; catalogue previews do not demonstrate engine emissive behaviour. No canonical GLB asset-admission certificate is claimed. Generic-format capability was verified against the official Blockbench source at https://github.com/JannisX11/blockbench/blob/v5.2.1/js/formats/generic.ts .

## Future updates — not yet completed

- Accepted vanilla-based space bee entities and Productive Bees compatibility for Minecraft 1.21.1.
- Registration and renderers for mob designs; real spawn eggs, AI, attributes, drops and boss mechanics.
- Controller/hatchery/menu bindings, frame/bee/genetic/comb slots, production outputs and export automation.
- Multiblock formation and interaction tests against the running mod, plus missing renderer/emissive bindings.
- Java wearable integration, first/third-person fit checks, trim support, animated texture frames and synchronised glow masks.
- Fresh higher-detail material painting where requested, rather than only texture enlargement.
- Client launch, multiplayer checks, recipe validation, packaging and tested release jars.

The existing branch build/install instructions still apply to the unchanged code. This collection must not be described as a working implementation of the future features above.

## Catalogue by use

### Armour — 20 fitted sets — 20 projects

astrium player fitted, aurelion player fitted, cerulite player fitted, cobaltium player fitted, cyrrium player fitted, eidolite player fitted, ferrox player fitted, moonsteel player fitted, nullifite player fitted, olympium player fitted, palladine player fitted, photium player fitted, pyrium player fitted, radiantine player fitted, ruskite player fitted, salvium player fitted, skarnite player fitted, solvanite player fitted, tectium player fitted, wraithsteel player fitted.

### Apiary blocks — 85 projects

controller, casing, frame housing, hatch, roof, controller, dryer, fan, heater, humidifier, casing, frame housing, glass, hatch, roof, controller, energy port, frame loader, honey port, input hatch, output hatch, casing, frame housing, glass, roof, controller, input hatch, output hatch, pressure port, rotor, vent, casing, frame housing, glass, roof, controller, energy port, input hatch, output hatch, stabilizer, casing, crown, frame housing, glass, roof, controller, energy port, fluid port, focus, input hatch, lens, output hatch, pylon, casing, frame housing, glass, roof, coil, controller, emitter, energy port, fluid port, input hatch, output hatch, casing, column, frame housing, glass, pillar, roof, zero g hive, apiary controller, centrifuge, frame assembler, frame component assembler, frame infusion altar, genetic splicer, geno station, gravitational centrifuge, infusion altar, silk weaver, stardust smelter, starmetal smelter, meteor comb block, nebula comb block.

### Apiary items and frames — 150 projects

astro honey, comet comb, cosmic jelly, lunar pollen, meteor comb, molten comb, nebula comb, pollen, royal jelly, solar comb, solar pollen, solidified royal jelly, stardust comb, void comb, void pollen, tier1 controller, tier1 casing, tier1 frame housing, tier1 hatch, tier1 roof, tier2 controller, tier2 dryer, tier2 fan, tier2 heater, tier2 humidifier, tier2 casing, tier2 frame housing, tier2 glass, tier2 hatch, tier2 roof, tier3 controller, tier3 energy port, tier3 frame loader, tier3 honey port, tier3 input hatch, tier3 output hatch, tier3 casing, tier3 frame housing, tier3 glass, tier3 roof, tier4 controller, tier4 input hatch, tier4 output hatch, tier4 pressure port, tier4 rotor, tier4 vent, tier4 casing, tier4 frame housing, tier4 glass, tier4 roof, tier5 controller, tier5 energy port, tier5 input hatch, tier5 output hatch, tier5 stabilizer, tier5 casing, tier5 crown, tier5 frame housing, tier5 glass, tier5 roof, tier6 controller, tier6 energy port, tier6 fluid port, tier6 focus, tier6 input hatch, tier6 lens, tier6 output hatch, tier6 pylon, tier6 casing, tier6 frame housing, tier6 glass, tier6 roof, tier7 coil, tier7 controller, tier7 emitter, tier7 energy port, tier7 fluid port, tier7 input hatch, tier7 output hatch, tier7 casing, tier7 column, tier7 frame housing, tier7 glass, tier7 pillar, tier7 roof, other zero g hive, apiary controller, frame component assembler, frame infusion altar, genetic splicer, geno station, gravitational centrifuge, other centrifuge, other frame assembler, other infusion altar, other silk weaver, other stardust smelter, other starmetal smelter, other meteor comb block, other nebula comb block, advanced circuit, confinement coil, fins component, silk thread, stardust, woven silk, aero frame, aero silk frame, chocolate frame, cryo frame, frame cosmic vigor, frame lunar, frame solar, frame swift mutation, frame void, healing frame, honeyed frame, impregnated frame, oblivion frame, proven frame, restraint frame, soul frame, starlit frame, starmetal frame, untreated frame, habitat locator, honey drop, portable beealyzer, serum vial, trait serum, aeronautic alloy, starmetal ingot, starmetal nugget, aeronautic scoop, alveary blueprint, apiarist wrench, basic scoop, bee smoker, copper grafter, diamond grafter, magnetic bee scoop, sturdy scoop, apiarist boots, apiarist chestplate, apiarist helmet, apiarist leggings, cosmic apiarist boots, cosmic apiarist chestplate, cosmic apiarist helmet, cosmic apiarist leggings.

### Apiary multiblocks — 8 projects

cosmic alveary, tier1 rustic alveary, tier2 controlled alveary, tier3 industrial alveary, tier4 aeronautic alveary, tier5 atm star alveary, tier6 nebula refractory, tier7 quantum queen chamber.

### Apiarist wearables — 8 projects

cosmic apiarist boots, cosmic apiarist chestplate, cosmic apiarist helmet, cosmic apiarist leggings, apiarist boots, apiarist chestplate, apiarist helmet, apiarist leggings.

### Material blocks — 94 projects

aresite ore, astrium ore, aurelion ore, cerulite ore, cinnabrite ore, cobaltium ore, coronite ore, cryocite ore, cyrrium ore, dawnstone ore, deepslate nullifite ore, eidolite ore, emberite ore, ferrox ore, fusion dust ore, lumenite ore, moonsteel ore, nebulite ore, nova pearl ore, olympium ore, palladine ore, photium ore, pulsar dust ore, pyrium ore, radiantine ore, regolith ore, remnant shard ore, rift opal ore, rimeglass ore, ruskite ore, salvium ore, selenite ore, skarnite ore, solvanite ore, spectral dust ore, starlite ore, tectium ore, tremor dust ore, wraithsteel ore, raw astrium block, raw aurelion block, raw cobaltium block, raw cyrrium block, raw ferrox block, raw moonsteel block, raw nullifite block, raw olympium block, raw palladine block, raw photium block, raw pyrium block, raw radiantine block, raw ruskite block, raw salvium block, raw tectium block, raw wraithsteel block, aresite block, astrium block, aurelion block, cerulite block, cinnabrite block, cobaltium block, coronite block, cryocite block, cyrrium block, dawnstone block, eidolite block, emberite block, ferrox block, fusion dust block, lumenite block, moonsteel block, nebulite block, nova pearl block, nullifite block, olympium block, palladine block, photium block, pulsar dust block, pyrium block, radiantine block, regolith block, remnant shard block, rift opal block, rimeglass block, ruskite block, salvium block, selenite block, skarnite block, solvanite block, spectral dust block, starlite block, tectium block, tremor dust block, wraithsteel block.

### Material items — 71 projects

cinnabrite, dawnstone, lumenite, rimeglass, selenite, fusion dust, pulsar dust, regolith, spectral dust, tremor dust, coronite, cryocite, emberite, nebulite, aresite, cerulite, eidolite, skarnite, solvanite, astrium ingot, aurelion ingot, cobaltium ingot, cyrrium ingot, ferrox ingot, moonsteel ingot, nullifite ingot, olympium ingot, palladine ingot, photium ingot, pyrium ingot, radiantine ingot, ruskite ingot, salvium ingot, tectium ingot, wraithsteel ingot, nova pearl, remnant shard, rift opal, starlite, astrium nugget, aurelion nugget, cobaltium nugget, cyrrium nugget, ferrox nugget, moonsteel nugget, nullifite nugget, olympium nugget, palladine nugget, photium nugget, pyrium nugget, radiantine nugget, ruskite nugget, salvium nugget, tectium nugget, wraithsteel nugget, raw astrium, raw aurelion, raw cobaltium, raw cyrrium, raw ferrox, raw moonsteel, raw nullifite, raw olympium, raw palladine, raw photium, raw pyrium, raw radiantine, raw ruskite, raw salvium, raw tectium, raw wraithsteel.

### Mobs — existing committed designs — 28 projects

ash strider, azure fowl, bog lurker, cinder hound, crater drifter, crystal stag, deep eel, dune burrower, dust grazer, dying star, eidolon captain, flare sprite, frost warden, frost yak, gildcrab, glimmerfish, ice leech, moon hopper, prism sentinel, prismling, regolith crawler, rift tyrant, rime stalker, rust beetle, sand skitter, scorch wyrmling, slag boar, sun colossus.

### Shattered Skies — style variants — 37 projects

amethyst stalker, amethyst stalker barded, amethyst stalker diamond, amethyst stalker echo, hollow sentinel, hollow sentinel drowned, hollow sentinel gilded, hollow sentinel stormbound, meteor maw, meteor maw comet, meteor maw ironfall, meteor maw voidstone, mossback, mossback autumn, mossback blossom, mossback ruinback, shardmother, shardmother ember, shardmother hollow, shardmother tidal, slagjaw, slagjaw crystal, slagjaw deepslate, slagjaw overgrown, splinter mite, splinter mite cinder, splinter mite moss, splinter mite reef, splinter wisp, splinter wisp ember, splinter wisp hollow, splinter wisp storm, splinter wisp tide, stormbitten wyvern, stormbitten wyvern galeborn, stormbitten wyvern stormcrown, stormbitten wyvern thunderhead.

### Mob drops — 65 projects

azure feather, beetle grub, blue egg, boar chop, boar tusk, burrower scale, burrower steak, captains lantern, cinder pelt, colossus core, cooked burrower steak, cooked eel, cooked gildcrab, cooked glimmerfish, cooked hopper, cooked venison, crawler leg, crispy lurker leg, cryo core, crystal hide, crystal shard, eel fillet, eel skin, fowl, frost milk, frost pelt, galaxy 3 gate key, galaxy 4 gate key, galaxy 5 gate key, gildcrab meat, gildcrab shell, glimmer scale, glimmerfish, grazer hide, grazer steak, grilled scorch tail, heart of solvane, heatproof plating, hopper fluff, hopper meat, leech gel, lurker leg, neutralizer, remnant shard, rift heart, roast fowl, roasted crawler leg, roasted skitter leg, rust shell, scorch scale, scorch tail, seared grazer steak, sentinel prism, skitter carapace, skitter leg, smoked boar chop, solar spark, stag venison, star map fragment, stardust, toasted grub, venom gland, yak meat, yak roast, yak wool.

### Spawn eggs — 38 projects

amethyst stalker spawn egg, ash strider spawn egg, azure fowl spawn egg, bog lurker spawn egg, cinder hound spawn egg, crater drifter spawn egg, crystal stag spawn egg, deep eel spawn egg, dune burrower spawn egg, dust grazer spawn egg, dying star spawn egg, eidolon captain spawn egg, flare sprite spawn egg, frost warden spawn egg, frost yak spawn egg, gildcrab spawn egg, glimmerfish spawn egg, hollow sentinel spawn egg, ice leech spawn egg, meteor maw spawn egg, moon hopper spawn egg, mossback spawn egg, prism sentinel spawn egg, prismling spawn egg, regolith crawler spawn egg, rift tyrant spawn egg, rime stalker spawn egg, rust beetle spawn egg, sand skitter spawn egg, scorch wyrmling spawn egg, shardmother spawn egg, slag boar spawn egg, slagjaw spawn egg, splinter mite spawn egg, splinter wisp spawn egg, stormbitten wyvern spawn egg, sun colossus spawn egg, tidewraith spawn egg.

### Approved Tidewraith — regular and boss palettes — 5 projects

tidewraith abyssal concept face, tidewraith concept, tidewraith concept abyssal, tidewraith concept pearl, tidewraith concept storm.

## Showcase files

- [showcases/ZeroG_Full_Collection_1_21_1.bbmodel](showcases/ZeroG_Full_Collection_1_21_1.bbmodel) — 609 projects
- [showcases/ZeroG_All_20_Armour.bbmodel](showcases/ZeroG_All_20_Armour.bbmodel) — 20 projects
- [showcases/Category_Apiary_blocks.bbmodel](showcases/Category_Apiary_blocks.bbmodel) — 85 projects
- [showcases/Category_Apiary_items_and_frames.bbmodel](showcases/Category_Apiary_items_and_frames.bbmodel) — 150 projects
- [showcases/Category_Apiary_multiblocks.bbmodel](showcases/Category_Apiary_multiblocks.bbmodel) — 8 projects
- [showcases/Category_Apiarist_wearables.bbmodel](showcases/Category_Apiarist_wearables.bbmodel) — 8 projects
- [showcases/Category_Material_blocks.bbmodel](showcases/Category_Material_blocks.bbmodel) — 94 projects
- [showcases/Category_Material_items.bbmodel](showcases/Category_Material_items.bbmodel) — 71 projects
- [showcases/Category_Mobs.bbmodel](showcases/Category_Mobs.bbmodel) — 28 projects
- [showcases/Category_Shattered_Skies.bbmodel](showcases/Category_Shattered_Skies.bbmodel) — 37 projects
- [showcases/Category_Mob_drops.bbmodel](showcases/Category_Mob_drops.bbmodel) — 65 projects
- [showcases/Category_Spawn_eggs.bbmodel](showcases/Category_Spawn_eggs.bbmodel) — 38 projects
- [showcases/Category_Approved_Tidewraith.bbmodel](showcases/Category_Approved_Tidewraith.bbmodel) — 5 projects
