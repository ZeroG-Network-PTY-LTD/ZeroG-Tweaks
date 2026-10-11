# Frozen Outpost: frozen wasteland placement repair

The prior natural audit confirmed a Frozen Outpost on Eidolon, but the runtime biome tag omitted the frozen wastelands named in the design. This repair adds the three existing Glaciers, Ice Spike Forest and Frozen Canyons biomes while retaining Hoarwood Taiga and Phantom Ice Sheets.

The shipped dimension definitions now provide biome eligibility in `g2_p4`, `g3_p1`, `g4_p5` and `g5_p2`. This is biome-driven, not a new dimension-ID check. Ocean and unrelated biomes remain excluded. Structure spacing/separation 40/20, salt, terrain checks, both templates, existing Cryo Core chest rewards and story text are unchanged.

Two source regressions check all five registered biomes, runtime/Design byte agreement, all four frozen dimension routes, ocean exclusion and the absence of guaranteed-placement bypasses. The structure graph still has nine configured structures and no missing references.

An ordinary fresh seed-zero server located the Outpost at X/Z 128/112 in `g2_p4`. Saved inspection confirms one natural jigsaw start in chunk 8/7, one intended unopened Outpost chest and 49 FULL chunks. Three additional mine chests use the existing Buried Observatory table; those do not establish a dedicated Observatory. Evidence: [natural placement report](reports/natural-frozen-wasteland-20261011.json). All temporary force loads were removed before save and normal shutdown; successful transcript `20261011_063349_runServer.log`, 2 minutes 12 seconds.

New placement eligibility applies to newly generated terrain; this batch does not reset the hub or existing planetary chunks. Broader seeds, every template variant, natural placement in the three later galaxy slots and client appearance remain pending.

Dedicated Sunken Relay, Buried Observatory, Sunken Lab and Impact Site remain unimplemented. Advanced research rules, undefined story/ending contracts and later survival cost balancing remain pending rather than being guessed.

Clean build passed (`20261011_063602_clean.log`, 41 seconds); asset audit checked 8021 models, 1529 blockstates, 4005 PNGs and 130 animation metadata files with zero errors. Three manufacturing source/JAR contracts also still pass. The initial packaging attempt hit a file-access error; the serial clean retry succeeded.

The same-version `1.0.12-dev` JAR was installed while the ZeroG client was closed, with the previous build backed up. [Installation receipt](reports/frozen-wasteland-install-20261011.json), [asset report](reports/frozen-wasteland-assets-20261011.json), and [published JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-frozen-wasteland-20261011.jar). SHA256: `2c096635983b4625855368b75c37d06011d820cfbae13a2bd9f13c98cc21af28`. Dependencies and saves were preserved.
