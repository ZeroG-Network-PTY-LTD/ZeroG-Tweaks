# Planet generation: independent seed-17 survey

An ordinary NeoForge 1.21.1 server generated a fresh disposable world with seed **17**, structures enabled and runtime `c128a2dd`. No GameTest fixtures, showcase preset, manually placed settlements or player saves were used. Productive Bees and the orbital addon were absent; this is native ZeroG generation evidence, not full-modpack compatibility approval.

The six natural settlement candidates below were calculated with the existing `PlanetSettlementFeature.candidate` rule. Each was surrounded by a temporary seven-by-seven chunk load. Inspection covered **294 saved FULL chunks** (49 per planet); generation dependencies may save additional chunks outside the inspected rectangles.

| Planet | Centre chunk | Mine loot chests | Ore IDs observed | Cave-flora IDs below Y32 | Settlements |
| --- | --- | --- | --- | --- | --- |
| Moon | 27,23 | 2 | 4 | 5 | 0 |
| Mars | 31,17 | 4 | 4 | 5 | 0 |
| Cerulon | 31,33 | 1 | 9 | 6 | 0 |
| Skarn | 24,28 | 2 | 9 | 5 | 1 |
| Eidolon | 33,29 | 1 | 10 | 3 | 0 |
| Solvane | 30,33 | 2 | 10 | 7 | 0 |

The 12 unopened mine chests bind `zerog_tweaks:chests/buried_observatory`. Hoarwood supports appeared on Moon/Eidolon, Charwood on Mars/Skarn, Shardwood on Cerulon and Gildwood on Solvane. This confirms local timber and a live loot binding, not a dedicated Buried Observatory structure or a check of every possible chest roll.

## Actual settlement and inhabitants

Skarn generated a layout-3 settlement anchored at **392,67,456**, with six ordinary residents and two specialists, all eight saved as Ashwrights. Live commands confirmed Charwood doors and `skarn_farmland[moisture=7]` at the expected farm. No vanilla villagers were observed in these six sampled sites. The other five candidate sites produced no settlement; a rejected site is not proof villages are absent planet-wide, and this sample does not measure rarity statistically.

Final saved populations included Moon Hoppers/Midnight Bees, Mars Dust Grazer/Rust Beetle, Skarn Rust Beetle/Ashwrights/Magma Bee, Eidolon Frost Yaks and a Solvane Gold Dust Bee. An earlier live-save inspection also observed Solvane Glowbugs; they are not present in the final entity snapshot. No natural hostile-population conclusion is possible without players and their normal spawning distances. Cerulon's empty saved entity sample is not a confirmed spawning bug.

## Cleanup and limitations

All six temporary force-load sets were explicitly removed, followed by `save-all flush` and normal server stop. Gradle completed successfully; transcript `20261011_014011_runServer.log` records normal shutdown. No fatal/error-level event or LegacyRandomSource threading exception was observed. A 3.227-second overload warning occurred during the multi-dimension generation burst; this is not evidence of installed-client latency. Optional-addon mixin class warnings were expected in this addon-free run.

[Saved-chunk report](reports/planet-generation-seed17-20261011.json) records seed, exact sites, counts, entities and structure starts. Earlier seed-zero evidence is retained in [the previous generation workflow](planetary-generation-workflow-2026-10-09.md).

Still pending: additional habitat/biome and galaxy-slot samples, ordinary player-distance hostile spawning, client navigation/appearance, missing dedicated ruins/signature entities and progression-reward gameplay checks. Approved gates, weather pause, installed JAR and all player saves remain unchanged. No replacement JAR is needed for this audit-only batch.
