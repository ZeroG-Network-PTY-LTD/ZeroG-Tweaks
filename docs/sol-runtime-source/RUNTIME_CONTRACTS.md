# Sol runtime source contracts — 2026-10-05

This is a preservation note for source generators, not game code or a claim that
every Sol content family is complete. The live implementation is on `1.21.x`
under `src/main/java/net/zerog/tweaks/`. Do not regenerate Java registrations from
an older generic stone template and silently discard these reviewed behaviours.

## Base blocks and stairs

Verified `registry/BlockInit.java` base registrations:

| ID | Runtime properties / class |
| --- | --- |
| `lunar_stone` | Stone map/sound, hardness 1.8, resistance 6 |
| `mare_basalt` | Black map, basalt sound, hardness 1.8, resistance 6 |
| `martian_stone` | Orange terracotta map, stone sound, hardness 2, resistance 6 |
| `olympium_plating` | Metal map/sound, hardness 5, resistance 9 |
| `oxide_crust` | Red terracotta map, tuff sound, hardness 1.5, resistance 6 |
| `crater_ice` | Actual `IceBlock`, `Properties.ofFullCopy(Blocks.ICE)` |
| `regolith`, `rustsand` | Actual `ColoredFallingBlock`, not immovable generic blocks |
| `polar_frost` | Actual `worldgen/PolarFrostBlock`; brief server-side Slowness I on stepping, no damage or freezing accumulation; flying players excluded |

The corrected staircase base is the matching material's actual default block
state, and its properties are copied from that material, for example:
`new StairBlock(LUNAR_STONE.get().defaultBlockState(),
Properties.ofFullCopy(LUNAR_STONE.get()))`. Wood stairs reference **planks**, and
`*_brick_stairs` reference the existing **bricks** registration. Definitions must
come after their bases are registered. Never restore `Blocks.STONE` as every
stair's base, introduce circular suppliers, or derive nonexistent singular IDs.
`repair_stair_bases.py` documents the verified mapping repair. Other decorative
families still need independent property review; these base fixes do not certify
all 742 families.

## Live species mechanics and authored art

`entity/AnimatedPlanetAnimal.java` supplies vanilla-style floating, panic,
breeding, temptation, following parents, wandering and looking, plus GeckoLib
controllers and periodic blinking. It does not replace species-specific
appearance or server AI. Keep the approved geometry/assets and authored sizes.

- **Moon Hopper:** `hop` locomotion clip, Lunar Lichen temptation/breeding, 16-tick
  movement-driven hop cadence. Moon gravity attribute is 0.04 rather than 0.08;
  hop impulse is 0.55 rather than 0.35. No fall damage.
- **Dust Grazer:** Rust Tuber temptation/breeding. An attack makes nearby herd
  members within 12 blocks navigate away at 1.6 speed; they do not become a
  permanently hostile generic monster.
- **Rust Beetle:** Rust Lichen food, retaliation target goal and melee attack,
  4 attack damage, authored attack animation triggered after a successful hit.
- **Dune Burrower:** Animated animal with Rust Tuber breeding and sand ambient
  sound. Its current source does **not** implement an actual underground burrow
  state machine; do not describe the species name as proof of that mechanic.
- **Frost Yak:** Lichen Crisps breeding. Adult unsheared animals give 1–2 Yak Wool;
  wool regrows after 6,000 ticks. Synced sheared state and remaining regrowth ticks
  persist in NBT. Do not remove this state on save/reload.
- **Meteor Maw / Ironfall:** Monster with persistent encounter and boss bar,
  authored `meteor_maw_ironfall` assets, server-side leap/slam and heat pulse,
  attack/blink/ability controllers. Current health 200, attack 8, armour 8;
  slam damage 6 within four blocks and pulse damage 4 within five blocks with
  line-of-sight. Creative/spectator players excluded. No blanket six-times-player
  scale should be added: this boss keeps the approved authored size.

Exact loot tables and balancing live on the code branch and are separately
reviewed; this note does not freeze a temporary drop list during integration.

## Six paired planetary kelp families

`registry/ZGPlanetAquatic.java` defines `moon`, `mars`, `cerulon`, `skarn`,
`eidolon` and `solvane` families, each with `*_kelp` heads and `*_kelp_plant`
bodies. Each head's `getBodyBlock()` returns its **own theme's body**, and each
body's `getHeadBlock()` returns that theme's head. Do not leave inherited methods
pointing to the generic `glowkelp` family after source regeneration.

These extend `ZGKelpBlock`/`ZGKelpPlantBlock`: upward, permanently waterlogged
source-water growth, 0.14 head growth chance, no attachment to magma, vanilla
head/body conversion and bone-meal growth. Bodies drop the collectible head item;
only heads have registered inventory items. Six palettes use light level 4 and
native animated head/body textures, matching inventory sprites, crossed-plane
models and smelting/smoking into vanilla dried kelp. They are water plants, not
plants promised to grow inside every custom liquid.

## Ore configured-feature type and thread ownership

Planetary ore configurations using the configurable rarity multiplier must use
`"type": "zerog_tweaks:configured_planet_ore"`, registered by
`registry/ZGEcologyFeatures.java`, rather than reverting to `minecraft:ore`.
`worldgen/ConfiguredPlanetOreFeature.java` preserves `OreConfiguration.CODEC`
and delegates actual vein placement to `OreFeature`. Its attempts are sampled
from `1 / ZGProgressionConfig.ORE_MULTIPLIER`; extra attempts stay in the owning
chunk at the configured height. This affects ZeroG configured ores only, not
vanilla ore generation. Preserve each feature's existing size, targets, height
and air-exposure settings unless a separate worldgen change is approved.

Use the feature context's random source on its owning thread. Do not introduce
asynchronous access to a ServerLevel's shared `LegacyRandomSource`, or perform
world mutation on worker threads. Earlier shared-random threading crashes are
not a reason to remove the new feature type or change all vanilla generation.

## Generator order and evidence

Run the authoritative `docs/full-art-rollout-v4/generate.py` last after older
art generators. Its native output is not a texture-upscaling pass. Preserve live
Java/data fixes first, then validate asset references, build, isolated gameplay
tests and client appearance separately. A contact sheet is not an in-game test.
