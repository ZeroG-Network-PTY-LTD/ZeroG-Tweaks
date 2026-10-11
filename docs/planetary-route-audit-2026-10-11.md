# Planetary structure and ecology follow-up — 11 October 2026

This is a read-only shipped-source audit, not a new terrain-generation run or client approval. Runtime reviewed: `c128a2dd`; Design source: `e1daa347`. The current installed same-version JAR remains the Stardust repair build, SHA256 `75e38ea43cbf256689ef619307c47b1bc3d4671fef4270caec2fccb791b7313c`.

## Results

The reproducible jigsaw graph audit found five configured structures and **zero missing pool/template references**. Its full evidence is [structure-routes-20261011.json](reports/structure-routes-20261011.json). A valid graph proves references exist, not that every room generates, rewards are obtainable, or rarity is balanced.

Eight chest tables have no dedicated reachable jigsaw binding: Buried Observatory, Collapsed Forge, Derelict Wreck, Frozen Outpost, Impact Site, Solar Shrine, Sunken Lab and Sunken Relay. This must not be reported as eight universally unobtainable loot tables: `PlanetMineshaftFeature` explicitly binds Buried Observatory loot in Java. Other Java-driven story placement needs its own inspection; the graph cannot certify its absence.

Ash Strider, Rime Stalker, Bog Lurker and Crater Drifter still have spawn-egg definitions but no matching registrations in `EntityInit`. An egg or preview does not implement its creature. Do not mark their natural ecology complete.

Previously verified generation evidence remains valid and separate: [9 October workflow](planetary-generation-workflow-2026-10-09.md) records seven focused passing tests and a structures-enabled seed-zero survey with 294 saved FULL chunks across six Sol planets, 13 mine loot chests and one Skarn settlement with eight Ashwrights. This follow-up does not rerun those tests or extend that sample.

## Next acceptance work

1. Sample additional seeds and habitat regions in disposable servers. Check actual village terrain blending, local doors/farms, mine chests, cave flora and suitable populations. Record negative samples as sample results, not worldwide absence.
2. Reconcile each pending structure against its approved Design geometry, biome and reward specification before implementation. Verify ordinary natural starts and actual chest contents after implementation.
3. Implement the four missing signature entities only from their verified model, behavior and habitat specifications; test real spawn placement and drops separately from spawn eggs.
4. Audit guardian-key/template first acquisition and Frozen Fleet/endgame routes through actual interactions. Existing four-key controller behavior and approved gates are not to be redesigned.

Advanced biology/research rules, seven-wide alveary specifications and exact survival costs remain pending. No player saves, hub, dimensions, gates, textures or weather were changed. No unchanged JAR was rebuilt or reinstalled for this documentation-only audit. Client appearance and natural hostile population coverage remain outstanding.
