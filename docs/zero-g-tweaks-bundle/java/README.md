# ZeroG Tweaks Java helpers (NeoForge 1.21.1)

Package names (`net.zerog.tweaks...`) and registry classes (`ZGItems`, `ZGBlocks`, `ZGEntities`) are placeholders; rename to match your project.

- `ZGFoods.java`: every food's FoodProperties from the design table. Custom effects (Freeze Ward, slowness immunity) are marked TODO.
- `ZGFoodItems.java`: drink animation, Frost Milk (clears effects), raw Scorch Tail (sets you on fire).
- `ZGInteractions.java`: milking a Frost Yak and tapping Shardwood logs with a glass bottle; shearing notes for the Crystal Stag and Frost Yak.

Registration notes:
- Astronaut Ration: `new Item.Properties().food(ZGFoods.ASTRONAUT_RATION).stacksTo(16)`.
- Bowl dishes: `.stacksTo(1)` like vanilla stews.
- Crops: register `rust_tuber_crop` as a CropBlock (age 0-3) with Rust Tuber as its seed item, and `skyberry_bush` like SweetBerryBushBlock.
- Fluid: `acid_still.png` / `acid_flow.png` are the textures for the Acid fluid type.
- Emissive blocks: models with a second element carrying `neoforge_data` (block_light 15) render the `_emissive.png` overlay full-bright. Verify in game.

## Added (gaps closed)
- `effect/ZGEffects.java`: Freeze Ward (freeze immunity) and Surefoot (Slowness immunity), with the events that enforce them. `ZGFoods` now uses them.
- `fluid/ZGFluids.java`: all six liquids (Acid, Liquid Starlight, Magma Slag, Cryo Fluid, Solar Plasma, Null Fluid): types, source/flowing fluids, blocks with their effects, buckets and mixing rules.
- `client/ZGClientExtensions.java`: textures and underwater fog colours for all six liquids.
- `client/ZGBlockColors.java`: tints the 308 grayscale wasteland blocks by wasteland type x galaxy (galaxy read from dimension ids like `g3_p2`).
- `client/ZGGeoEntities.java`: one generic GeckoLib model + renderer for all 28 mobs (glowmask layer included).
- `item/ZGGeoArmorItem.java`: armor that renders each set's GeckoLib model with its 3D extras.

Dependencies: GeckoLib 4.x for NeoForge 1.21.1. Model paths follow GeckoLib 4.5+ (`geckolib/models`, `geckolib/animations`).

- `item/ZGSpawnEggs.java`: spawn eggs for all 28 mobs (DeferredSpawnEggItem, colours from each palette).
