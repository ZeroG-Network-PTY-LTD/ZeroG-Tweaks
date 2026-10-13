# Fresh workshop and planetary structure test world

Status: five isolated hub/structure checks passed; normal build passed; new save
exported independently and same-version JAR installed with backup while client
was closed. Client visual approval remains pending.
Same mod version1.0.12-dev. Existing worlds are preserved; new save name:
`ZeroG_Workshop_Structures_20261013_Seed0`.

## Hub layout

- North: six admin and six finite-powered player gate builds, tiers1–6.
- West:15 supplied machine stations, including the new Water Separator and
  Industrial Compressor; rear power connections, recipe ingredients/catalysts.
- South: existing hub-approved apiary/alveary shells and service ports.
- Existing transport demonstrations and essential multiblock exhibits retained.
- No giant landing-pad floor, automatic background dimension sweep or permanent
  hub chunk tickets. No old save replacement.

## Planetary test structures

Three49x64x49 native templates translate the approved silhouettes into Minecraft
blocks: Cerulon Water Bio-Habitat, Skarn Hot Ring Monolith, Eidolon Ice Spire Outpost.
Each has local grass/soil, arches or supported ring, towers, galleries, two supply
chests and one hostile spawner. First translation, not pixel-identical image or
approved client appearance. Dark cone vent models are NOT included in this batch.

Test origin512,90,512. Surface layer102, galleries94..98. Visit in Creative:

```mcfunction
/execute in zerog_tweaks:cerulon run tp @s 536 106 570 180 0
/execute in zerog_tweaks:skarn run tp @s 536 106 570 180 0
/execute in zerog_tweaks:eidolon run tp @s 536 106 570 180 0
/execute in minecraft:overworld run tp @s 0 65 0
```

Inspect entrances, stair clearances, room accessibility, palette and silhouettes.
Spawner tests validate placement/metadata, not balanced natural mob encounters;
initial enemies are drowned, magma cubes and strays respectively. Ordinary basic
supplies only: iron/copper/string/torches, no story keys/templates/Console rewards.

These are explicit isolated test-region builds, not natural-generated ruins.
Do not claim they blend into every terrain: full natural siting/rotations and
spawning integration remain pending. Region1,1 is copied for those three planets;
all other planetary terrain generates on visits. No pregen50 completion claim
follows from the compact export. Existing broader village reliability remains open.

## Evidence to record before installation

- Hub gate/supply/exhibit tests pass with local optional bee addons.
- All three templates place, six chest inventories generate supplies, three
  spawners exist and central underground passages are clear.
- Normal build excludes GameTest classes/fixtures.
- Verified JAR installed with an old-JAR backup only while client is closed.
- New save exported separately; old worlds and unrelated mods unchanged.

Installed JAR SHA256:
`4212a8bf51b0433a45f2d122f623343e7d0932cfa5f426a57e00b4efb87938c7`.
No test classes/fixtures in the normal archive; three templates and matching loot
tables are present. All five required tests passed in the addon-enabled hub run.
The test run also prepared50chunks/dimension, but this compact export intentionally
copies only three structure test regions, not that full pre-generation result.
