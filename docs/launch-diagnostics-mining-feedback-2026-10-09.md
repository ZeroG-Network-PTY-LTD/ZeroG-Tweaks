# Launch diagnostics and mining feedback — 9 October 2026

Minecraft Java 1.21.1 / NeoForge; same mod version `1.0.12-dev`.

## What this changes

- Inventory tooltips on ZeroG blocks show the requirement from the loaded mining tags.
- An insufficient survival mining tool triggers a red actionbar requirement. It does not prevent breaking, change drops, or lower the ore ladder.
- Moonsteel requires Ferrox or better. Netherite opens Nullifite; Nullifite opens Ferrox; Ferrox opens Moonsteel. Stone and fuel requirements remain independent.
- A passenger-group cancellation logs one scoped `[ZeroG-launch-diagnostic]` record: gate tier, elapsed countdown, pad bounds, readiness counts, source/destination, anonymous passenger-relative positions and movement, lift/levitation status, alive/spectator state and extra-passenger count. No names, UUIDs or launcher/account arguments are recorded.

## Important unresolved issue

The installed-client launch still cancels after the prior lifted-position mock passed. This build instruments that failure; it does **not** claim another teleport fix. Gate movement, fees, transition behavior and arrival generation remain unchanged. Do not enlarge the launch bounds again without inspecting the captured failure.

## Player checks

1. Hover Moonsteel Ore: expect a Ferrox-pickaxe requirement.
2. In survival, try Nullifite: expect the red requirement and no ore drop. Then mine a different Moonsteel Ore with Ferrox: expect Raw Moonsteel (or the ore with Silk Touch).
3. Charge the Tier 1 Gate Energy Port to at least100,000FE, select Moon/Mars, stand on the pad and Engage. Do not walk while charging.
4. If it cancels again, report the attempt. The local `logs/latest.log` contains the scoped launch diagnostics; preserve it before another launch overwrites the log. There is no need to export launcher startup arguments.

## Verification

The isolated `zerog_blockers` suite ran14 required tests; all passed, including the new mining requirement/drop test. Disposable world: `run-local-mining-feedback-20261009`. Transcript: `20261008_234232_runWorkflowTests.log` (host-generated filename; player-facing date above is Bangkok).

Client tooltip appearance and the actual launch cause await player review. Existing hub, saves, custom-weather pause and other installed mods are retained. Exact survival crafting costs and undefined biology remain pending.

Clean production build passed; asset audit reports zero errors across7,979 models,
1,529 blockstates,3,963 PNGs and130 animation metadata files. No GameTest classes
or fixtures ship in the production JAR.

Installed and published binary SHA256:
`447ba39df288c43eb8de92f8fd4f863274d15327605761befa7b455fc027ac14`.
Archive: `docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-launch-mining-diagnostics-20261009.jar`.
The installed main JAR was replaced only after client closure, with its prior
`59a37824` build backed up outside mods. Other mods and saves were not changed.
