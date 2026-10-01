# Minecraft 1.21.1 animation references

Checked the local client version metadata (`1.21.1`) and mapped NeoForge Minecraft sources for all 82 mob IDs supplied by the user. These are references, not additional ZeroG entity registrations.

## Applied to the original ZeroG rigs

- QuadrupedModel: diagonal leg pairs move together; opposite pairs counter-swing. Child shins/feet inherit the phase of their own upper leg.
- RabbitModel: left/right hind limbs push together while forelegs tuck; Moon Hopper now has limb motion in its hop clip instead of root bob alone.
- ChickenModel: opposite leg phases, mirrored wing movement and head-linked facial parts. Azure Fowl retains its original anatomy.
- SpiderModel: mirrored lateral leg movement and staggered phases. The Shardmother lower-leg phase now matches its corresponding numbered upper leg.
- PhantomModel: mirrored wing chains; its tail flex runs at twice wing frequency. Tidewraith fly/glide drafts now use this relationship.
- SilverfishModel: low articulated segments with phase-offset lateral sway; Dune Burrower is now an original low sand-coloured arthropod with segment movement, replacing the upright worm concept.
- BatModel / BatAnimation: distinct resting and flight states and articulated wings; reference only, not copied as universal animation for every flyer.
- Armadillo, Camel, Sniffer, Frog, Warden and Breeze use authored state/animation definitions. Bogged uses its skeleton-family locomotion. These demonstrate why separate runtime state controllers are required.

The current assets contain editable, original animation drafts. Locomotion speed, head tracking, randomized blinking, attack transitions, aura/emissive layers and particle/sound events still need Java/GeckoLib controllers and client testing. The vanilla code does not make these custom clips run automatically.

## Inventory

| Mob ID | Model / renderer source | Animation entry points |
| --- | --- | --- |
| `minecraft:allay` | `AllayModel.java` | setupAnim |
| `minecraft:armadillo` | `ArmadilloModel.java` | animate, animateWalk, setupAnim |
| `minecraft:axolotl` | `AxolotlModel.java` | setupAnim |
| `minecraft:bat` | `BatModel.java` | animate, setupAnim |
| `minecraft:camel` | `CamelModel.java` | animate, animateWalk, setupAnim |
| `minecraft:cat` | `CatModel.java` | prepareMobModel, setupAnim |
| `minecraft:chicken` | `ChickenModel.java` | setupAnim |
| `minecraft:cod` | `CodModel.java` | setupAnim |
| `minecraft:cow` | `CowModel.java` | Inherited / renderer-driven |
| `minecraft:donkey` | `ChestedHorseModel.java` | setupAnim |
| `minecraft:fox` | `FoxModel.java` | prepareMobModel, setupAnim |
| `minecraft:frog` | `FrogModel.java` | animate, animateWalk, setupAnim |
| `minecraft:glow_squid` | `SquidModel.java` | setupAnim |
| `minecraft:horse` | `HorseModel.java` | prepareMobModel, setupAnim |
| `minecraft:mooshroom` | `CowModel.java` | Inherited / renderer-driven |
| `minecraft:mule` | `ChestedHorseModel.java` | setupAnim |
| `minecraft:ocelot` | `OcelotModel.java` | prepareMobModel, setupAnim |
| `minecraft:parrot` | `ParrotModel.java` | prepareMobModel, setupAnim |
| `minecraft:pig` | `PigModel.java` | Inherited / renderer-driven |
| `minecraft:pufferfish` | `PufferfishBigModel.java` | setupAnim |
| `minecraft:rabbit` | `RabbitModel.java` | prepareMobModel, setupAnim |
| `minecraft:salmon` | `SalmonModel.java` | setupAnim |
| `minecraft:sheep` | `SheepModel.java` | prepareMobModel, setupAnim |
| `minecraft:skeleton_horse` | `HorseModel.java` | prepareMobModel, setupAnim |
| `minecraft:sniffer` | `SnifferModel.java` | animate, animateWalk, applyStatic, setupAnim |
| `minecraft:snow_golem` | `SnowGolemModel.java` | setupAnim |
| `minecraft:squid` | `SquidModel.java` | setupAnim |
| `minecraft:strider` | `StriderModel.java` | setupAnim |
| `minecraft:tadpole` | `TadpoleModel.java` | setupAnim |
| `minecraft:tropical_fish` | `TropicalFishModelA.java` | setupAnim |
| `minecraft:turtle` | `TurtleModel.java` | setupAnim |
| `minecraft:villager` | `VillagerModel.java` | setupAnim |
| `minecraft:wandering_trader` | `VillagerModel.java` | setupAnim |
| `minecraft:zombie_horse` | `HorseModel.java` | prepareMobModel, setupAnim |
| `minecraft:bee` | `BeeModel.java` | prepareMobModel, setupAnim |
| `minecraft:cave_spider` | `SpiderModel.java` | setupAnim |
| `minecraft:dolphin` | `DolphinModel.java` | setupAnim |
| `minecraft:enderman` | `EndermanModel.java` | setupAnim |
| `minecraft:goat` | `GoatModel.java` | setupAnim |
| `minecraft:iron_golem` | `IronGolemModel.java` | prepareMobModel, setupAnim |
| `minecraft:llama` | `LlamaModel.java` | setupAnim |
| `minecraft:panda` | `PandaModel.java` | prepareMobModel, setupAnim |
| `minecraft:piglin` | `PiglinModel.java` | setupAnim |
| `minecraft:polar_bear` | `PolarBearModel.java` | setupAnim |
| `minecraft:spider` | `SpiderModel.java` | setupAnim |
| `minecraft:trader_llama` | `LlamaModel.java` | setupAnim |
| `minecraft:wolf` | `WolfModel.java` | prepareMobModel, setupAnim |
| `minecraft:zombified_piglin` | `PiglinModel.java` | setupAnim |
| `minecraft:blaze` | `BlazeModel.java` | setupAnim |
| `minecraft:bogged` | `BoggedModel.java` | prepareMobModel |
| `minecraft:breeze` | `BreezeModel.java` | animate, setupAnim |
| `minecraft:creeper` | `CreeperModel.java` | setupAnim |
| `minecraft:drowned` | `DrownedModel.java` | prepareMobModel, setupAnim |
| `minecraft:elder_guardian` | `GuardianModel.java` | setupAnim |
| `minecraft:endermite` | `EndermiteModel.java` | setupAnim |
| `minecraft:evoker` | `IllagerModel.java` | setupAnim |
| `minecraft:ghast` | `GhastModel.java` | setupAnim |
| `minecraft:giant` | `GiantZombieModel.java` | Inherited / renderer-driven |
| `minecraft:guardian` | `GuardianModel.java` | setupAnim |
| `minecraft:hoglin` | `HoglinModel.java` | setupAnim |
| `minecraft:husk` | `ZombieModel.java` | Inherited / renderer-driven |
| `minecraft:illusioner` | `IllagerModel.java` | setupAnim |
| `minecraft:magma_cube` | `LavaSlimeModel.java` | prepareMobModel, setupAnim |
| `minecraft:phantom` | `PhantomModel.java` | setupAnim |
| `minecraft:piglin_brute` | `PiglinModel.java` | setupAnim |
| `minecraft:pillager` | `IllagerModel.java` | setupAnim |
| `minecraft:ravager` | `RavagerModel.java` | prepareMobModel, setupAnim |
| `minecraft:shulker` | `ShulkerModel.java` | setupAnim |
| `minecraft:silverfish` | `SilverfishModel.java` | setupAnim |
| `minecraft:skeleton` | `SkeletonModel.java` | prepareMobModel, setupAnim |
| `minecraft:slime` | `SlimeModel.java` | setupAnim |
| `minecraft:stray` | `SkeletonModel.java` | prepareMobModel, setupAnim |
| `minecraft:vex` | `VexModel.java` | setupAnim |
| `minecraft:vindicator` | `IllagerModel.java` | setupAnim |
| `minecraft:warden` | `WardenModel.java` | animate, animateWalk, setupAnim |
| `minecraft:witch` | `WitchModel.java` | setupAnim |
| `minecraft:wither_skeleton` | `SkeletonModel.java` | prepareMobModel, setupAnim |
| `minecraft:zoglin` | `HoglinModel.java` | setupAnim |
| `minecraft:zombie` | `ZombieModel.java` | Inherited / renderer-driven |
| `minecraft:zombie_villager` | `ZombieVillagerModel.java` | setupAnim |
| `minecraft:ender_dragon` | `EnderDragonRenderer.java` | prepareMobModel, setupAnim |
| `minecraft:wither` | `WitherBossModel.java` | prepareMobModel, setupAnim |

## Guides inspected

- [Minecraft style guide](https://blockbench.net/wiki/guides/minecraft-style-guide/): deliberate pixel clusters, restrained palettes, planes and consistent UV density.
- [Overview and tips](https://blockbench.net/wiki/guides/blockbench-overview-tips/): proximal-to-distal parenting and pivots at anatomical joints.
- [Animation expressions](https://blockbench.net/wiki/guides/animation-expressions/): expression exports and GeckoLib support; implementation still requires matching controllers.
- [Emissive renders](https://blockbench.net/wiki/guides/emissive-textures-renders/): Blender/Sketchfab rendering workflow, not automatic Minecraft lighting.
- [Particles and sounds](https://blockbench.net/wiki/guides/minecraft-particles-sounds/): Bedrock-specific effects; Java needs its own registration and event handling.

The two purple-eyed face images were inspected directly. Optical decals use a deliberate rectangular three-cell design, darker centres and lighter ends, adapted to each creature. Natural and emissive eyes keep different colour treatments. The project remains custom HD art rather than strict vanilla texel density.
