# Sol workflow and verification ledger

This ledger incorporates the supplied Sol Build Tracker and the outstanding bee-machine work. It does not treat an asset, diagram or compiled class as proof of gameplay. The tracker described an older code snapshot; each item must be checked against the current source before implementation.

## Integrated rollout — current source, 2026-10-05

The lists below retain the supplied acceptance requirements. They are not all
still unimplemented. This section supersedes their earlier pending status.

| Area | Implemented runtime | Evidence / boundary |
| --- | --- | --- |
| Genetics | Five verified PB traits, analysis before sampling/splicing, real serums, FE, jelly catalysts, 4,000 mB registered honey support and recovery inventories | Server integration tests; no invented chromosomes or species mutation |
| Alveary | Separate 27-frame inventory; unlocks 3/4/6/8/12/18/27, migration, physical power/item/fluid ports, tier FE, honey/starlight tanks, real PB recipes/productivity, output pages, sort/eject and confirmed void controls | Formed-controller production with a live PB iron-bee recipe, component-preserving outputs and saved honey; ports reject stale/ambiguous/unloaded owners; unsupported native lifespan/tolerance bands stay labelled unavailable |
| Transport | Six tiers of energy/fluid/item lines and cells, ports, coal-powered generator, routing, face/signal rules, dangerous-fluid restrictions, template filters, upgrades, dye/cleaning and canonical shared Null Links | Conservation, simulation, persistence, filters, upgrades and stale-owner tests; no chunk-forcing for networks |
| Sol travel | Owned player-built tier shapes, FE/star chart/upgrades, ready countdown, first-arrival return platform, Recall/Group Anchors, pets and gravity | Cold home-gate footprint fix verified by two-player actual dimension travel; admin hub gates remain separate |
| Progression | Moon/Mars Codex arrival pages, Mars crash-site layouts/loot, Aresite shrine and signature professions | Runtime data/recipe/POI tests; sparse surface jigsaw structures use existing planetary blocks |
| Mobs | Regolith Crawler, Moon Hopper, Dust Grazer and Ironfall Meteor Maw; actual animations/renderers for Frost Yak, Rust Beetle and Dune Burrower | Factories, registered attributes, resolved eggs, breeding predicates and asset bindings tested; no additional mob library dependency |
| World detail | Higher bounded habitat density, varied cave flora, six kelp families, Sol biome signatures and Deep Dark Null Fluid pools with deepslate lining | Feature-local random only; kelp does not replace flowing water with new source blocks; detailed fresh-world report records observed content |
| Gear/blocks | Olympium worn shell and visual Dust Shield, no-damage Polar Frost, real Sol ice/sand/metal properties and all 164 real stair bases | Block/property checks; most other armor sets retain their matching vanilla UV fallback rather than claiming all shells approved |
| Art | 1,111 native PNG revisions: C equipment/materials, A/C vegetation, varied crop silhouettes, wood/leaves, vines, kelp, selective armor glow and 120 aligned trim overlays across 2,400 models; wet/dry soil retained | [Native gallery](images/full-art-rollout-v4/README.md), source/UV/hash manifests and 340 editable sprite sources; 2,432 retained textures are not claimed redrawn; not client captures |

### Known limits — do not mark these complete

- Client approval: both-hand Moonsteel/item-frame orientation, worn armor fit,
  menu readability/shift-click/output controls, particles, colored stars and Iris.
- The installed PB API does not expose the planned queen lifespan,
  temperature/humidity/gravity alleles, mutation/territory or full drone breeding
  rules. Planned rotor/coil/climate-module mechanics need authoritative rules;
  sealing unavailable displays is intentional, not simulated completion.
- Full parity with PB flower/territory and hive-upgrade simulation is not claimed.
  Product quantities/chances come from its actual current server recipes.
- Third-party claims/team adapters and the unspecified hidden-world pool for
  Star Map Fragment remain pending. Basic scoreboard co-op is implemented.
- Moving items/fluids inside transport pipes still need a client renderer and
  visual acceptance; transfers themselves are server-functional.
- Ironfall leap/slam and heat pulse are implemented. Its proposed Cinder Mite
  adds remain pending: no approved/registered Cinder Mite entity exists. Other
  authored death/emergence abilities are not fabricated by exporting their art.
- Frost Yak's shear/regrow data persists, but a separate approved shorn body
  model is not available. Hiding its current `wool` bone would hide the whole body.
- Other retained textures are counted explicitly, not claimed re-authored.

Final build, installation, world-refresh and branch receipts are recorded in
`sol-workflow-delivery-2026-10-05.json` after their respective checks succeed.

Delivered locally: the same-version production JAR passed a clean normal build
and has SHA256 `21764a8015e16c159c29136efe3047871d4038cbad33a8051710111ab6087c33`.
Its packaged audit checked 7,799 models, 1,498 blockstates, 3,785 PNGs, 96 animation
metadata files and 3,816 source-byte bindings with zero errors. The replaced JAR
is backed up outside `mods`; unrelated dependencies are unchanged. The selected
seed-0 save received 34 fresh planetary folders after a complete backup; all 50
protected hub/player/unrelated files remained byte-identical. See the
[delivery receipt](sol-workflow-delivery-2026-10-05.json) and
[production asset audit](sol-production-asset-audit-2026-10-05.json).

### Final isolated server verdicts

- **26/26** integrated workflow checks passed with Productive Bees and the
  orbital-bee companion installed: formation/ports, persisted frames/tanks,
  actual recipe products and productivity, transport conservation/security,
  genetics catalysts, generator power, Sol properties, mobs and tree fixtures.
- **2/2** optional-mod travel/startup checks passed without Productive Bees or
  the companion: actual two-player round trip, cold return footprint, home/Recall
  and owner-state handling.
- **4/4** genetics processing, menu and save/reload regressions passed with the
  installed Productive Bees integration.
- **7/7** fresh planetary hub/prologue checks passed; all 34 dimensions saved and
  shut down cleanly before the terrain survey and selected-save refresh.

These are 39 checks across four isolated test groups, not client visual approval.
Development runs include optional-target/refmap warnings and synthetic fixture
heightmap warnings; they completed with passing verdicts, successful builds and
clean server shutdown. The normal distributable excludes these test fixtures.

### Fresh terrain verification

The isolated seed-0 hub audit passed all seven checks: 34 destinations, 68 gate
routes, 34 distinct sampled terrain profiles and 60 nearby inspection settlements
with 480 designed planetary residents. Obsolete demonstration colonies are off.
This is a generated test environment, not evidence that natural villages or mobs
spawn at every location or that every boss behavior is visually approved.

A full saved-region survey found 543 actual log blocks across 108 tree-containing
chunks in 21 dimensions, including the correct tree family on all six named Sol
planets. These are chunks, not a count of trees. All four configured tree families
also passed direct growth tests on planetary grass. Thirteen ocean, glacier,
crater and acid-swamp slots had no trees observed in their saved samples; broader
natural ecology and shoreline coverage remains a player exploration check.

Read the [isolated hub report](sol-isolated-hub-report-2026-10-05.json) and the
[saved native-chunk survey](sol-native-terrain-survey-2026-10-05.json) for exact
per-dimension observations. Counts from the hub's single sampled chunk are not
the same scope as the wider saved-region survey.

The selected save's player data is preserved, including its current creative-mode
Moon location. If fresh terrain surrounds that position on first load, use
`/zerog hub` to return to the intact Overworld inspection hub.

## Verified genetics milestone

The current implementation uses the installed Productive Bees 13.14.0 cage/attachment API. Its real traits are productivity, endurance, temper, behavior and weather tolerance—not queen/princess chromosomes or invented fertility fields.

- Analysis, sampling and single-trait serum splicing are implemented server-side.
- Geno Station: 10,000 FE; analysis takes 100 powered ticks or 400 hand-cranked ticks; sampling takes 300 powered ticks or 1,200 hand-cranked ticks, at 20 FE/t when powered.
- Genetic Splicer: 40,000 FE; 400 powered ticks at 60 FE/t. Royal jelly gives 75% success; cosmic jelly gives 100%. Failed splicing returns the unchanged bee, not a lost specimen.
- Five operating slots plus eleven take-only legacy recovery slots preserve the existing sixteen-slot inventories. Wrong inputs, blocked outputs, changed inputs and remote button requests are rejected.
- Jobs and FE persist in the existing block entity. Only the selected trait is changed; other bee data stays intact.
- Four isolated integration tests passed with Productive Bees and the orbital-bee addon. Two further checks passed without either optional mod: startup safety and bounded/distinct habitat density rules. Genetics coverage includes processing, output safety, persistence, menu validation, automation filtering, FE capabilities and suppression of the old placeholder processing. Habitat-rule assertions are not a generated-world visual audit.
- Client layout/visual approval is still pending. The subsequent integrated rollout adds analysis research prerequisites and registered honey tank support. Item royal/cosmic jelly catalysts remain usable; nonexistent liquid-jelly IDs are not invented.

## Original bee-machine acceptance checklist

| Priority | Work | Acceptance evidence required |
| --- | --- | --- |
| Implemented with disclosed API limits | Alveary frame progression up to 27, real productivity and verified genome data, energy/fluid storage | Tier tests, insertion/output filters, persistence; unknown biological rules remain pending |
| Implemented backend/controls | Six-tier transport, ports, wrench, filters, energy cells and Null Links | Conservation, unloaded-owner safety, save/reload and no-duplication regressions |
| Native rollout complete, visual approval pending | Equipment/materials/plant and inventory artwork | Native PNG/UV/animation validation; gallery is not in-game proof |
| Gameplay | Controller interactions, output paging/sorting, shift-click, both-hand Moonsteel and Iris stars | Actual client review, not a headless test claim |

## Sol blockers from the supplied tracker — implemented acceptance requirements

1. Player-built T1 gate: 5×5 Nullifite frame, 3×3 pad, four short pylons, energy port and controller; tier formation and upgrade preview.
2. Gate block entity, star-chart menu and upgrade slots; T1 Moon/Mars routing, 500,000 FE base cost, within-galaxy discount and passenger cost. The test hub's existing unlimited T6 gates are not survival progression.
3. First-arrival landing platform and return charge using crystal cells, outside the test hub too.
4. Mars crash-site structure and loot wiring for Ferrox, Moonsteel and Olympium progression templates.
5. Working coal/charcoal combustion generator.

## High-priority Sol acceptance requirements

6. Planet gravity (Moon 0.5, Mars 0.7), reset when returning, configurable overrides.
7. Regolith Crawler and Moon Hopper entity/AI/spawn implementation instead of placeholder Moon spawns.
8. Dust Grazer entity/AI/spawns for Rust Plains and Oxide Badlands.
9. Meteor Maw / Ironfall registration or verified shared-library integration and debris-related lore.
10. Olympium wearable model and Dust Shield protection.
11. Polar Frost slow/chill, respecting the agreed non-damaging initial environmental effects.
12. Recall Anchor, home routing, charge and cooldown.
13. Null Fluid pools associated with Deep Dark / ancient-city terrain.

## Normal-priority Sol acceptance requirements

14. Distinct Moon/Mars biome features: crater ice, basalt mare, polar frost and oxide spires.
15. Lunari Regolith Refiner and Rustborn Rust Mechanic POIs/trades.
16. Mars Aresite-core shrine and advancement connection.
17. T2 Moonsteel-ring/low-arch/Selenite-lens gate progression.
18. Shared ore rarity, gate-cost and gravity configuration.
19. Sol block properties and stairs' correct base states.
20. Concord Codex Moon/Mars Act 1 pages unlocked on arrival.
21. Moonsteel hand-facing gameplay review.
22. Launch transition animation and cooperative ready check.
23. Update milestone checkboxes only when the corresponding behavior is verified.

## Approved artwork and texture policy

The user approved both equipment palettes and A/C vegetation on 2026-10-05. Equipment/materials use C magitech: readable enhanced-vanilla silhouettes, restrained energy accents and hue-shifted shadows/highlights. Vegetation blends natural A shading with C glowing buds/fruit. Dirt and farmland contain no ores/gems. Dry and wet farmland must remain distinct. Inventory and placed/worn artwork must match.

The approved concept sheet is not itself a game-ready atlas. The native rollout now supplies individual textures with transparency, animation metadata and matching runtime UV/resource layers. If a new appearance is not covered by the approved reference, request an example; unanswered changes remain pending rather than receiving an invented replacement.

The newly fetched Design commit `844a6d44` locks the gradient/depth study and
block-lighting/floating-item GIF references. Its [contributor art lock](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/art-direction-lock.md)
and exact six-tone named ramps are preserved; all newly generated native assets
must stay consistent with those sources. Reference animations are not a claim
that the same render has been captured inside the Minecraft client.

The subsequent request extends this direction to all armour/items/materials, farming plants, flowers, trees, vines, kelp and ocean vegetation. More cave life should use planet-matched hanging vines, mushrooms, rock formations and stalagmites, not identical lush decoration everywhere. Initial density changes reuse current registered vegetation: richer oasis/jungle/island/taiga patches, bounded 40–56 cave sample columns (previously 32), longer cave vines, taller dripstone, more wall vines/lichen and cave-pool kelp. Guards prevent vines/lichen from overwriting a just-placed stalagmite or mushroom. New texture variants and cave objects remain production tasks, not silently declared implemented.

## Selected world refresh

Selected save: `ZeroG_Planet_Showcase_1_0_9_Seed0`. Preserve its Overworld hub, players, Nether, End and unrelated dimensions. Back up the entire selected save before replacing any planetary files. The other showcase save is outside scope.

Refresh is not implied by genetics tests. The delivery receipt records its actual completion separately. Removing planet region files alone is unsafe: the ledger may refer to gates that no longer exist. The refresh tool takes a complete backup, verifies the isolated 34-planet source, stages replacements, merges only planetary gate/inspection records and proves protected hub/player/unrelated files unchanged. Failure restores old folders and ledger; old terrain is moved, never permanently deleted.

## Delivery order

1. Implement and test each gameplay milestone in disposable worlds.
2. Build the normal production JAR without GameTest classes; inspect assets and mod metadata.
3. With the client closed, back up and replace only the matching ZeroG JAR. Keep version 1.0.12-dev for these fixes.
4. Carry out the separately verified, backed-up selected-world refresh.
5. Publish separate commits: code on `1.21.x`, art/design on `Design`, documentation/images/JAR/checksums on `Docs`. Pull before each push. Never merge their unrelated histories or change `Released` directly.

No row above is silently completed just because a build succeeded.
