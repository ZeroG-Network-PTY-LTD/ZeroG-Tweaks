# Native terrain checkpoint — 13 October 2026

Scope: inspect current runtime generation, not activate experimental landforms or
reset any player world. Existing hub, weather pause and installed gas build remain
untouched.

## Harness boundary

The default GameTest preset loads no custom planets. The lore preset loads only
Moon/Mars plus a flat story-test Solvane. Those two failed attempts are harness
setup failures, not evidence that production planetary generation is broken.

`tools/generate_native_ecology_fixture.py` copies all34 current dimension
definitions into an opt-in test preset, with an ordinary plains flat test
Overworld. `-PworkflowNativePlanetPreset` enables it. It never uses the hub biome,
exports a save or modifies player worlds. Regenerate the fixture after dimension
definitions change.

Run from the code checkout:

```sh
python3 tools/generate_native_ecology_fixture.py
./gradlew runWorkflowTests -PworkflowTests -PworkflowNativePlanetPreset \
  -PworkflowTestNamespaces=zerog_native_ecology \
  -PworkflowTestDirectory=run-native-ecology-fresh
```

Use a new disposable directory. Never enable the lore/hub preset alongside this
fixture. Rebuild normally afterward: production must exclude the test classes
and `data/minecraft/worldgen/world_preset/flat.json`.

## Checks

- Eight source contracts passed for dimension isolation, terrain composition and
  settlement placement.
- Three source ore checks passed: common-to-rare configured vein sizes decrease,
  added metal veins exceed their paired rare gems, and Nullifite retains its small
  story deposit. These do not measure connected natural vein sizes.
- The native survey checks25 sampled ground columns per dimension at two seeds,
  plus neighbouring16-block height differences. It reports sample variation and
  distinctness; this does not certify aesthetically realistic terrain.
- The Sol ecology survey counts actual custom blocks in18 generated chunks per
  planet and reports loaded biome features/spawn settings separately.
- GameTestServer disables structure generation. Natural village/ruin placement and
  mob population density need an ordinary isolated server, not these fixtures.

## Recorded result

Both required native tests passed (`20261013_014925_runWorkflowTests.log`).
68 heightmap rows cover34 dimensions at seeds0 and20261012. Sample heights range
from-48 to188; the largest sampled16-block change is65 blocks. These steep
changes warrant terrain review rather than an unqualified realism claim.
The Sol survey generated108 chunks and observed ores in every sampled planet.
Clean production build passed afterward; archive inspection found neither the
test classes nor the test flat preset. Installed gameplay JAR remains unchanged.

Reports: [heightmaps](reports/planet-heightmap-survey-2026-10-13.json) and
[Sol ecology](reports/native-planet-ecology-2026-10-13.json).

## Remaining work

Experimental surface-relief profiles remain opt-in/local and unactivated. Broader
slope/biome/ore-deposit evidence, realistic terrain changes, natural structure/mob
checks and a fresh playable world/export remain separate outstanding tasks.
No runtime JAR replacement is needed for a test-only checkpoint.
