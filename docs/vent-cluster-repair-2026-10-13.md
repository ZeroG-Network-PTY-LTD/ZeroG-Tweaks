# Vent field count repair

Owner requested3–6 naturally blended vent blocks per field. Actual world-placement
regression reproduced only2 distinct vents on the flat Skarn seed11 fixture.
The old loop regenerated its limit and sampled repeated coordinates. Hot cones
could independently replace all nine central top cells with vents.

## Implemented locally

- Pick target3–6 once per field.
- Gather unique legal columns, shuffle using the feature's RandomSource.
- Ordinary fields preserve terrain heights within2 blocks of the centre and
  require the existing local surface, air overhead and no block entity.
- Skip before writing if fewer than the requested number can fit.
- Hot extinct cones retain their whole-footprint protection and place3–6 top
  apertures instead of all nine. Cache surveyed columns before any cone writes.
- Unknown themes safely skip. No worker-level shared RNG, forced chunks,
  ambient weather enablement, hazards or new registries.

## Evidence

Red:13 tests ran, the count fixture failed on Skarn seed11 with2vents.
Green: all14required zerog_planet_generation tests pass. The count fixture runs
32seeds for each of Moon/Skarn; a separate32seed sparse-site check proves two
usable positions and an existing chest remain unchanged. Existing settlement,
mining footprint and buried-controller regressions remain green.

This is bounded gameplay placement evidence, not natural density measurement or
client visual approval. Black faceted cone models/textures are still pending.
The repair is NOT in installed JAR4212a8bf; hold it for the next combined delivery.
Existing worlds and showcase save were not edited. Test servers shut down normally.

Follow-up14October: repair included in the backed-up compressor JAR4fcff84a.
Already-generated fields remain unchanged; new generation uses the corrected
count logic. Cone artwork is still pending.
