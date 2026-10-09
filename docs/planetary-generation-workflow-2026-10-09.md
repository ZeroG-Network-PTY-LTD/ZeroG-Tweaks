# Planetary generation workflow

## Accepted by the owner

On 9 October the owner approved the installed gates, power, pipes, Flux Wrench
and transitions. Their previous pending visual approval is superseded by this
confirmation. Historical tests and diagnostic notes remain useful evidence.
Unrelated machine functionality and planetary ecology are not implicitly approved.

## Source review and current implementation

Reviewed the locally cached mapped Minecraft **1.21.1** `MineshaftPieces` source
and ZeroG's `PlanetMineshaftFeature`, `PlanetSettlementFeature`,
`PlanetEcologyProfile` and `PlanetCaveEcologyFeature`.

- Vanilla mineshafts distinguish rail and spider corridors and build segmented
  support structures. Further review must cover intersections, stairs and bounds.
- Vanilla has **no Nether mineshaft structure**. Hot-world mines can use
  Nether-inspired materials and atmosphere, but must be original ZeroG layouts.
- Existing ZeroG mines excavate a fixed crossing with hull supports, rails and
  a chest using the Buried Observatory loot table. This is not a complete
  vanilla-style branching mine or a dedicated observatory structure.
- Settlements already select charwood, hoarwood, gildwood or shardwood planks
  and matching doors from the planet theme. Farms and surface integration still
  require actual generated-world checks.
- Cave generation already includes ceiling vines, themed berries, mushrooms,
  dripstone, wall vegetation and water kelp. More density alone is not proof of
  suitable ecology; verify support, fluids, habitat and underground spawn rules.

## Ordered implementation and verification

1. Review vanilla village template pools, terrain adaptation and mineshaft pieces.
   Record which patterns are reused conceptually; use existing ZeroG blocks.
2. Replace repetitive mine crossings with bounded corridor/intersection variants,
   planet-local support materials, occasional rails and lore-appropriate rewards.
   Keep chunk bounds, dry-terrain checks and arrival protection intact. Do not
   excavate player machines or force-load chunks during generation.
3. Verify rare settlements sit at local ground level, with matching dirt,
   farmland, doors and crops. Preserve spacing; do not add showcase colonies.
4. Audit underground vegetation against each planet's existing habitat rules.
   Test ceiling/floor attachment, water-only kelp and supported growth states.
5. Audit cave mob registrations and spawn predicates. Do not mark missing mobs
   complete merely because model files or spawn eggs exist. New creature art
   needs its own approval, not a placeholder substituted as a finished mob.
6. Run ordinary isolated-server generation surveys: biome/seed/location,
   structure starts and blocks, loot, villagers, ores and underground plants.
   GameTest servers disable natural structures, so use them only for targeted
   placement/safety tests, not as natural-generation evidence.
7. Build and inspect the production JAR after tests. No save reset or hub
   replacement is part of this workflow without a separate explicit request.

## Still pending after this priority

- Remaining machine recipe/combination pages and upgrade compatibility.
- Concord Codex trait research mapping and undefined advanced alveary biology.
- Larger seven-wide alveary layouts and their approved module rules.
- Guardian keys, templates, structure rewards and missing boss mechanics audit.
- Gas production recipes and solar-plasma/cooling specifications.
- One shared ground-level arrival pad per dimension: multiplayer return routing
  remains undecided; retain existing bound return gates until specified.
- Small Moon impact wrecks; do not add Broken Consoles to Meteor Maw loot.
- Exact survival crafting costs remain deferred until owner-provided balance.

## Implementation in this batch

- Mines now use a seeded spine with two to four staggered branches, local
  wood/fence supports and axis-correct rails. The existing chest reward is kept.
  Preflight rejects wet terrain, largely unsupported cavern/sky footprints,
  protected gateways, containers and constructed blocks before writing.
- Settlement candidate spacing is unchanged. Ground sampling ignores crowns;
  the entire graded footprint is checked for ravines, water and excessive slope.
  Container protection includes all five foundation layers. Existing local doors,
  wet farmland, native transition edges and the Rustborn shrine are retained.
- Cave kelp uses source water only and has a head even when a flowing-water
  boundary shortens it. Wall vines form bounded descending supported strands
  without crossing containers or other obstacles.
- Existing Prismlings can use covered Starlight Caverns/Geode Depths above the
  deep-spawn cutoff. This does not add surface encounters in those cave biomes.
  Moon/Mars surface creatures are not arbitrarily reassigned underground.
- Prismling, Rust Beetle, Dune Burrower, Dust Grazer and Regolith Crawler PNG
  sizes match their geometry declarations; all have visible pixels and animation
  files. This source check is not a rendered-client appearance test.

Verification and distribution are recorded below when complete. Existing player
saves are not reset by this batch; generation changes affect newly created chunks.

## Verification evidence

- All **7 required isolated tests passed**, transcript
  `20261009_003116_runWorkflowTests.log`. These cover 128 repeatable bounded mine
  plans, rare spacing including negative regions, actual mine placement and gate
  obstruction safety, village doors/farmland/shrine and buried-machine/ravine
  refusal, all six kelp families, vine obstacles and the real Prismling predicate.
- Ordinary Minecraft/NeoForge server, seed 0, natural structures enabled: **294
  saved FULL chunks**, 49 per Sol planet, around seed-selected village candidates.
  Temporary loading tickets were released and the server exited normally.
- Saved mine loot chests: Moon 3, Mars 2, Cerulon 2, Skarn 3, Eidolon 2, Solvane 1.
  These total **13** in the surveyed areas. This is observed feature placement,
  not a claim that every mine is a vanilla structure start.
- Ores and below-Y32 cave flora were observed on all six planets. One natural
  Skarn settlement at **392, 47, 360** had eight saved Ashwrights, matching Charwood
  doors and supports, plus Skarn farmland with Cinder Pepper crops. Other selected village candidates were not accepted; a
  candidate is not a guarantee of suitable terrain.
- Additional saved entities included Moon Hoppers, Dust Grazers, Frost Yaks,
  Rust Beetles, Crimson Bees and planetary glowbugs. No claim is made that the
  no-player survey observes every hostile cave-mob population.
- Production `clean build` passed: `20261009_003610_clean.log`. The native survey
  report is archived alongside this guide; player saves and hub are unchanged.

## Installed build

The owner authorized installation with an old-JAR backup; the Java client was
verified closed before replacement. Installed file remains
`zerog-tweaks-1.21.1-1.0.12-dev.jar`, SHA256
`ff8e85725e82a8b128fa96f8aabd6b1e5f3a9907cf4536cdee2ea17b5bd2f874`.
The former build is recoverable under the instance's
`zerog-mod-backups/20261009-003901-UTC/` folder, outside `mods`.
Productive Bees, GeckoLib and the orbital addon were preserved byte-for-byte.

[Archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-planet-ecology-20261009.jar),
[natural survey](reports/planet-generation-natural-20261009.json),
[packaged asset audit](reports/planet-generation-assets-20261009.json).
No optional test classes or generation fixtures are packaged in the JAR.

Remaining review: client appearance, additional seeds/biomes and actual natural
hostile-spawn populations. Undefined lore species are not substituted or marked
finished. Exact survival costs and advanced biology rules remain deferred.
