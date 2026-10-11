# Frozen Outpost: natural generation audit

An ordinary disposable NeoForge 1.21.1 server running code `3e5bb712` generated a fresh seed-zero world with structures enabled. No hub preset, GameTest placement, manual structure placement or player saves were used.

The normal locator found a Frozen Outpost on Eidolon at X/Z **-416 / -560**, start chunk **-26 / -35**. Saved-region inspection of a temporary 7×7 chunk area confirms **49 FULL chunks**, one valid natural jigsaw structure piece, and one unopened chest bound to `zerog_tweaks:chests/frozen_outpost`.

Evidence: [saved-region report](reports/natural-frozen-outpost-20261011.json). Earlier focused placement tests separately verified both templates in four rotations and the guaranteed Cryo Core loot roll; this ordinary audit did not open the chest or repeat that loot test.

This closes natural generation verification for one site in one seed only. Both variants across broader seeds, terrain blending, statistical rarity and client appearance remain pending. The approved story text and missing dedicated Sunken Relay, Buried Observatory, Sunken Lab and Impact Site also remain separate TODOs.

The server saved and stopped normally, with a successful run in 2 minutes 26 seconds; transcript `20261011_055819_runServer.log`. The temporary force-load tickets remain only in this stopped disposable audit world; no player world was changed. The installed JAR already contains this structure and needs no replacement for this documentation-only audit.
