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
