# Forge, Wreck and Shrine: natural generation audit

An ordinary disposable NeoForge 1.21.1 server using runtime `7723225c` generated a fresh seed-zero world with structures enabled. No GameTest structures, hub preset, `/place` command or player saves were used. The optional orbital addon and Productive Bees were absent: this is native ZeroG world-generation evidence, not full-modpack compatibility approval.

The normal `/locate structure` command found each site from dimension origin. A temporary 7×7 chunk load around each site then generated the physical structures. Saved-region inspection confirms one valid jigsaw piece and one unopened chest bearing the intended loot table at each site.

| Dimension | Structure | Located X/Z | Start chunk | Inspected FULL chunks | Intended chest |
| --- | --- | --- | --- | --- | --- |
| Skarn | Collapsed Forge | 240 / 240 | 15 / 15 | 49 | `zerog_tweaks:chests/collapsed_forge` |
| Eidolon | Derelict Wreck | 928 / 96 | 58 / 6 | 49 | `zerog_tweaks:chests/derelict_wreck` |
| Solvane | Solar Shrine | 48 / 304 | 3 / 19 | 49 | `zerog_tweaks:chests/solar_shrine` |

The rectangles also contain six naturally generated mine chests using the existing Buried Observatory loot table (one Skarn, two Eidolon, three Solvane). No settlement anchors occurred in these three rectangles; this is not evidence that villages are absent planet-wide.

Reports retain seed, saved FULL-chunk counts, valid starts, piece IDs and chest loot bindings:

- [Collapsed Forge](reports/natural-collapsed-forge-20261011.json)
- [Derelict Wreck](reports/natural-derelict-wreck-20261011.json)
- [Solar Shrine](reports/natural-solar-shrine-20261011.json)

## What this closes—and what remains

The earlier “ordinary natural generation unverified” gap is now closed for **one site per ruin in seed zero**. It does not establish statistical rarity, every habitat or variant, client walkability/appearance, actual player loot rolls, boss completion or a full survival journey. Earlier focused tests cover template loot rolls and rotated placement independently; do not conflate those with this natural-world inspection.

Missing dedicated Sunken Relay, Buried Observatory, Frozen Outpost, Sunken Lab and Impact Site structures remain TODO. Observatory loot in mines does not make a dedicated Observatory exist. Missing signature mobs, boss encounters, exact survival costs and the deferred advanced bee research mapping remain separate.

All three force-load sets were explicitly removed before `save-all flush` and normal server shutdown. The ordinary server run completed successfully in 1 minute 47 seconds; transcript `20261011_051831_runServer.log`. The installed same-version JAR, player saves and hub are unchanged. This audit-only batch needs no replacement JAR or Design changes.

Artwork and original source descriptions: [Collapsed Forge](collapsed-forge-2026-10-11.md), [Derelict Wreck](derelict-wreck-2026-10-11.md), [Solar Shrine](solar-shrine-2026-10-11.md).
