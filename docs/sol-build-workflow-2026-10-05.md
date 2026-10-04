# Sol workflow and verification ledger

This ledger incorporates the supplied Sol Build Tracker and the outstanding bee-machine work. It does not treat an asset, diagram or compiled class as proof of gameplay. The tracker described an older code snapshot; each item must be checked against the current source before implementation.

## Verified genetics milestone

The current implementation uses the installed Productive Bees 13.14.0 cage/attachment API. Its real traits are productivity, endurance, temper, behavior and weather tolerance—not queen/princess chromosomes or invented fertility fields.

- Analysis, sampling and single-trait serum splicing are implemented server-side.
- Geno Station: 10,000 FE; analysis takes 100 powered ticks or 400 hand-cranked ticks; sampling takes 300 powered ticks or 1,200 hand-cranked ticks, at 20 FE/t when powered.
- Genetic Splicer: 40,000 FE; 400 powered ticks at 60 FE/t. Royal jelly gives 75% success; cosmic jelly gives 100%. Failed splicing returns the unchanged bee, not a lost specimen.
- Five operating slots plus eleven take-only legacy recovery slots preserve the existing sixteen-slot inventories. Wrong inputs, blocked outputs, changed inputs and remote button requests are rejected.
- Jobs and FE persist in the existing block entity. Only the selected trait is changed; other bee data stays intact.
- Four isolated integration tests passed with Productive Bees and the orbital-bee addon. Two further checks passed without either optional mod: startup safety and bounded/distinct habitat density rules. Genetics coverage includes processing, output safety, persistence, menu validation, automation filtering, FE capabilities and suppression of the old placeholder processing. Habitat-rule assertions are not a generated-world visual audit.
- Client layout/visual approval is still pending. Fluid catalyst tanks and research progression are not implemented by this milestone.

## Outstanding bee-machine work

| Priority | Work | Acceptance evidence required |
| --- | --- | --- |
| Next | Alveary frame progression up to 27, actual modifiers, tolerance/genome display, energy and fluid storage | Tier tests, insertion/output filters, persistence and multiplayer synchronization |
| Next | Six-tier transport, ports, wrench, filters, energy cells and Null Links | Conservation tests, unloaded-chunk safety, save/reload, no duplication |
| Art | Remaining equipment, materials, plant and inventory sprite audit | Native texture/UV validation and in-game approval; approved concept is not an installed atlas |
| Gameplay | Controller interactions, output paging/sorting, shift-click, both-hand Moonsteel and Iris stars | Actual client review, not a headless test claim |

## Sol blockers from the supplied tracker

1. Player-built T1 gate: 5×5 Nullifite frame, 3×3 pad, four short pylons, energy port and controller; tier formation and upgrade preview.
2. Gate block entity, star-chart menu and upgrade slots; T1 Moon/Mars routing, 500,000 FE base cost, within-galaxy discount and passenger cost. The test hub's existing unlimited T6 gates are not survival progression.
3. First-arrival landing platform and return charge using crystal cells, outside the test hub too.
4. Mars crash-site structure and loot wiring for Ferrox, Moonsteel and Olympium progression templates.
5. Working coal/charcoal combustion generator.

## High-priority Sol tasks

6. Planet gravity (Moon 0.5, Mars 0.7), reset when returning, configurable overrides.
7. Regolith Crawler and Moon Hopper entity/AI/spawn implementation instead of placeholder Moon spawns.
8. Dust Grazer entity/AI/spawns for Rust Plains and Oxide Badlands.
9. Meteor Maw / Ironfall registration or verified shared-library integration and debris-related lore.
10. Olympium wearable model and Dust Shield protection.
11. Polar Frost slow/chill, respecting the agreed non-damaging initial environmental effects.
12. Recall Anchor, home routing, charge and cooldown.
13. Null Fluid pools associated with Deep Dark / ancient-city terrain.

## Normal-priority Sol tasks

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

The new image is a concept sheet, not game-ready 32×32 textures. Individual native-resolution textures, transparency, animation metadata and UVs still need production and inspection. If a new texture's appearance is not covered by approved references, request an example; unanswered changes remain pending in this ledger instead of receiving an invented replacement.

The subsequent request extends this direction to all armour/items/materials, farming plants, flowers, trees, vines, kelp and ocean vegetation. More cave life should use planet-matched hanging vines, mushrooms, rock formations and stalagmites, not identical lush decoration everywhere. Initial density changes reuse current registered vegetation: richer oasis/jungle/island/taiga patches, bounded 40–56 cave sample columns (previously 32), longer cave vines, taller dripstone, more wall vines/lichen and cave-pool kelp. Guards prevent vines/lichen from overwriting a just-placed stalagmite or mushroom. New texture variants and cave objects remain production tasks, not silently declared implemented.

## Selected world refresh

Selected save: `ZeroG_Planet_Showcase_1_0_9_Seed0`. Preserve its Overworld hub, players, Nether, End and unrelated dimensions. Back up the entire selected save before replacing any planetary files. The other showcase save is outside scope.

Refresh is pending—not performed by the genetics tests. Removing planet region files alone is unsafe: the persisted gate ledger can still mark destinations prepared and refer to gates that no longer exist. Planet gate/inspection records must be refreshed alongside terrain, while retaining the hub records. Validate safe arrivals, structure/village placement, resident species, vegetation, ores and liquids before declaring the refreshed world ready.

## Delivery order

1. Implement and test each gameplay milestone in disposable worlds.
2. Build the normal production JAR without GameTest classes; inspect assets and mod metadata.
3. With the client closed, back up and replace only the matching ZeroG JAR. Keep version 1.0.12-dev for these fixes.
4. Carry out the separately verified, backed-up selected-world refresh.
5. Publish separate commits: code on `1.21.x`, art/design on `Design`, documentation/images/JAR/checksums on `Docs`. Pull before each push. Never merge their unrelated histories or change `Released` directly.

No row above is silently completed just because a build succeeded.
