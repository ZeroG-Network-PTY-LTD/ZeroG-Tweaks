# Legacy processor power and recipe repair

Same-version candidate: **1.0.12-dev**, Minecraft Java1.21.1 / NeoForge.

Installed to the ZeroG CurseForge mods folder after confirming the client closed.
SHA256: `4e9021850f2121cfe860c7fd22d801f962a3f1b688ba2b13ba0e1e7e1d4f0772`.
Old JAR is recoverable under `zerog-mod-backups/20261011-223156-UTC`.
Receipts: `reports/legacy-power-install-20261012.json` and
`reports/legacy-power-assets-20261012.json`. Asset audit found zero errors;
normal clean build passed in50seconds, and zero GameTest classes ship.
Archive: `jars/zerog-tweaks-1.21.1-1.0.12-dev-legacy-power-20261012.jar`.

## Confirmed causes

The previous power allow-list registered only Centrifuge and Starmetal Smelter.
Silk Weaver, Gravitational Centrifuge, Frame Assembler, Frame Component Assembler,
Frame Infusion Altar and Infusion Altar therefore had no electric capability.
Earlier tests repeated that allow-list as their expected contract and did not
prove every processor had power. The owner explicitly requested this repair.

Recipe pages already existed, but the358px workbench/side-control layout disabled
the Recipes button when fewer than120px remained for a sidebar. This could look
like missing recipes at normal GUI scales.

## Runtime changes

All eight electric addon processors now receive FE through their independently
configurable six faces. Existing inputs, outputs, unused-slot recovery, catalysts
and inventory indices remain intact. Blocked/unpowered jobs do not consume inputs
or processing energy. Default work costs:20FE/t for weaving/frame/infusion and
centrifuges,80FE/t for Starmetal. New `legacyProcessorFEPerWorkTick` is configurable.
Silk completes after200 work calls (4,000FE base); frame/infusion after201
(4,020FE base). Acceleration/Energy Coil cards use existing2.5x/30% caps with exact
whole-job rounding and correct input fingerprints. Compact/Void are not invented.
The Stardust Smelter deliberately retains its separate furnace-fuel contract.
Generators produce FE rather than receiving it as processing input.

Workbench Recipes opens an in-menu read-only view with Items/Recipes/Upgrades;
Back/Escape returns to the machine. It neither closes the server container nor
routes clicks, drags or hotbar keys to hidden inventory slots. This fixes the
legacy workbench recipe accessibility; other screen families are not silently
claimed visually approved. Native processors already have their electric inputs.

## Evidence

Final addon-present run: **all8 required tests passed** in
`20261011_222837_runWorkflowTests.log` (UTC date,12October locally). This includes
actual copper conduit/cell charging of all eight processors, eleven-machine face
coverage, every loaded combination across card tiers0–6 with exact output/FE/time,
unpowered checks, blocked frame outputs, Stardust fuel preservation and GuideME
page parsing. Disposable server stopped normally. Client rendering/layout remains
for owner approval, not inferred from headless tests. No saves/hub/weather changed.

The runtime frame guide and Design `docs/codex-guide-v1/write_guide.py` agree.
Survival costs, advanced biology and unrelated lore proposals remain inactive.

## Player check

Connect a generator/cell through an energy conduit to an enabled power face.
Open the machine: its stored FE should rise. Silk Thread goes in Weaver slot0;
Woven Silk comes out of slot3. Frame recipes use slots0/1, output2 (Frame Infusion
Altar output3). Click Recipes, select an item or combination and inspect quantities,
outputs, FE/time and supported cards. Back/Escape should preserve the open machine
and any carried item. Review these layouts at your usual GUI scale.
