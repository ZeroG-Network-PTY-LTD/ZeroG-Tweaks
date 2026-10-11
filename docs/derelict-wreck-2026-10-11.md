# Eidolon: small Hollow Fleet wrecks

This batch adds two original 19×9×27 damaged ship layouts to the Frozen Graveyard biome. Existing Hull Plating, Corroded Hull, Cryo Pods, Broken Consoles and Spectral Lanterns surround an open corridor and accessible salvage chest. No new console logs, boss encounters or artwork are invented.

The chest uses the existing Derelict Wreck loot table, including chances for Salvium, Palladine, Wraithsteel and Eidolite templates. A template is not guaranteed in every chest. Initial placement uses dry-land terrain checks, 40-chunk spacing and 20-chunk separation; these are initial settings, not final rarity balance.

## Verification boundaries

The focused tests check both layouts in all four orientations, chest lid clearance, corridor access, actual loaded loot and native Eidolon terrain generation. Ordinary-world discovery and client visual review are separate checks; a passing template test must not be presented as proof of those.

Both required focused tests passed in `20261011_041047_runWorkflowTests.log`; the disposable server saved and stopped normally. The earlier broader run passed nine of eleven tests before the wreck bounds assertion was corrected. Its separate Moon gate reload assertion still requires investigation.

The broader suite also exposed an existing Moon gate-access reload assertion failure. Its fixture constructs a detached controller, so the cause needs a focused loaded-controller persistence investigation. It remains unresolved; approved gate behavior has not been changed in this batch.

An initial wreck bounds assertion compared the terrain-blending reference box with the authored ship bounds. Minecraft expands that reference box by 12 blocks on each side. The test now checks the actual structure piece and the blending margin separately; the ship geometry was not enlarged.

## Still outstanding

- Collapsed Forge and Solar Shrine generation/rewards.
- Larger wrecks, Eidolon Captain encounter and peaceful route.
- Natural wreck discovery and client visual approval.
- The separate gate-access reload regression investigation.
- Exact survival costs and undefined bee research/biology rules remain deferred.

Existing saves and the approved hub are unchanged. Newly generated Frozen Graveyard terrain is required for natural wreck placement.

## Same-version delivery

Clean build passed in 45 seconds (`20261011_041230_clean.log`). Asset audit checked 7,979 models, 1,529 blockstates, 3,963 PNGs and 130 animation metadata files with zero errors. The release JAR includes both ship templates and excludes the isolated test class/fixture.

Installed while the ZeroG client was closed: `zerog-tweaks-1.21.1-1.0.12-dev.jar`. SHA256: `f08daf0fb897043d3b89206e3769a875d35e6bc9f01673b689d9cf37cf2fdeb3`. The previous JAR is recoverable under `zerog-mod-backups/20261011-041343-UTC`; dependencies, saves and weather settings were untouched. Installation and asset receipts are in `docs/reports/derelict-wreck-install-20261011.json` and `derelict-wreck-assets-20261011.json`.
