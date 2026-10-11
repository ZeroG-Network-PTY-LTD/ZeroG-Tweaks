# Gas connection leaks — approved rules

The owner approved visible leaks and brief biological effects for incorrectly built gas connections. This supersedes the earlier no-gas-effects restriction in the Water Separator specification, without enabling weather damage or explosions.

## What counts as an incorrect connection

A Water Separator Hydrogen or Oxygen output connected directly to an enabled ZeroG **liquid pipe** vents gas. Use a **gas tube** instead. Disabled pipe faces, disabled separator outlets, open air, solid blocks, full receivers and correct gas tubes do not trigger leaks. This first implementation deliberately does not guess the safety of third-party pipes or apply hazards to unrelated machines.

- Default loss: up to **10 mB per second per incorrect outlet**, capped by the gas actually stored.
- Server configuration: `wrongLiquidPipeLeakMBPerSecond` in `zerog-gas-production-server.toml`, range 0–100; zero disables leaks.
- Hydrogen: cloud particles; survival/adventure players within two blocks and with an unobstructed view of the outlet receive three seconds of level-I nausea and weakness, refreshed only during an actual leak.
- Oxygen: bright vent particles, no harmful effects.
- Creative/spectator players are unaffected. Moving away stops refresh; existing effects expire normally. Effects from other sources are not removed.
- No explosions, fire, terrain damage, persistent contamination, physical pressure simulation or forced chunk loading.

Full tanks still pause production safely. Gas is lost only at an actual misconnection, not merely because storage is full.

## Player checks

All six gas-tube tiers already exist in Storage & Transport: **Copper → Nullifite → Cyrrium → Tectium → Wraithsteel → Astrium**. Their IDs are `zerog_tweaks:<material>_gas_tube`. They follow the existing transport-tier progression; this update verifies them rather than introducing duplicate gas pipes.

1. Supply water and FE to the Water Separator and produce gas.
2. Attach a gas tube to the configured Hydrogen face: gas transfers without a leak.
3. Replace it with a liquid pipe whose face permits input: stored hydrogen falls slowly and clouds appear.
4. Stand close in survival: brief nausea/weakness. Move away: they expire.
5. Disable the pipe input or separator outlet: venting stops.
6. Repeat on Oxygen: visible venting, no biological effects.
7. Fill a correctly connected output tank: production pauses without leaking.

Client particle appearance and comfort remain subject to play-test approval. Dedicated separator artwork, exact survival costs and undefined bee-research rules remain pending.

## Verification

All **16 required isolated server tests passed** in `20261011_141101_runWorkflowTests.log`: bounded wrong-pipe loss, disabled/unconnected outlets, all six registered gas-tube tiers remaining safe, actual survival hydrogen exposure, oxygen safety, shelter and distance protection, production conservation/full-tank pauses, container/pipe exchange and existing gate/transport regressions. The test harness initially used a creative-reporting mock player; the exposure test was corrected to use a normal survival player before the passing run. No client or existing save was used.

Clean production build passed (`20261011_141210_clean.log`); the packaged asset audit checked 8,023 models, 1,530 blockstates, 4,005 PNGs and 130 animation metadata files with zero errors. No GameTest classes ship in the production JAR.

Same-version `1.0.12-dev` installed with the client closed in `C:/Users/jakem/curseforge/minecraft/Instances/ZeroG/mods`. Previous JAR backed up under `ZeroG/zerog-mod-backups/20261011-141342-UTC`. Dependencies, hub, saves and disabled custom weather were preserved.

Archived build: [gas-leak JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-gas-leaks-20261011.jar). SHA256: `f67c74fa32b600d58dc0a5d55835d0add3e3eee4ae6ec435ff523a9d45d2cf70`. Reports: [assets](reports/gas-leaks-assets-20261011.json), [installation](reports/gas-leaks-install-20261011.json).
