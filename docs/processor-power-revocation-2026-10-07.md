# Processor power-face revocation

Minecraft 1.21.1 / NeoForge; same-version 1.0.12-dev repair. No hub, save, recipe or artwork changes.

## Reproduced issue

The Alloy Forge, Ore Refinery, Crystal Growth Chamber and Salvage Station checked whether a power face was currently disabled, but did not permanently revoke its cached handler. Switching Off, then Input, allowed an old connection to receive power again. Item-face controls already used revocation generations; this repair applies the same boundary to power.

The isolated regression reproduced `Re-enabled face revived a stale handler` in `20261007_013414_runWorkflowTests.log`. An earlier launch selected no tests because its fixture namespace was wrong; that launch is not passing test evidence.

## Repair

Each changed power face advances its connection generation. Old handlers remain unable to receive FE after re-enabling; freshly acquired handlers work normally. Changing an already-identical setting does not revoke a valid handler. Loading saved settings also invalidates old sided handles. Existing unsided internal access, capacities, recipe costs and persisted face masks remain unchanged.

The regression exercises actual registered energy capabilities on all six faces of all four machines, including disabled/re-enabled access, fresh acquisition, simulation without mutation and exact accepted energy. Final production-build, regression and installation evidence is recorded in [the delivery receipt](processor-power-revocation-delivery-2026-10-07.json). Server checks are not client visual approval.

The wider suite caught one older test that explicitly expected the cached handler to revive. Its expectation was updated to require a fresh capability after re-enabling, while retaining distant-player denial, saved disabled settings and post-removal denial. The runtime was not weakened to satisfy the obsolete expectation.

All **110 required tests passed** in `20261007_013737_runWorkflowTests.log`. Clean production build: `20261007_013851_clean.log`. The asset audit found zero errors across 7,977 models, 1,528 blockstates, 3,943 PNGs and 120 animation metadata files. The same-version JAR was installed with an old-JAR backup before publication; no saves changed. SHA256: `730f70911b1c5eb62ff5035849bd4dd0e469d52c3a131839d0b398b77c810fd5`. [Archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-power-revocation-20261007.jar).

## Next approved upgrade contract

The owner approved Acceleration and Energy Coil cards for the Geno Station, Genetic Splicer, Centrifuge and Starmetal Smelter using the existing configurable caps: maximum 2.5× speed and 30% total-job FE saving. This is **approved for implementation, not included in this power repair**.

- Add two dedicated card sockets without moving existing operating/recovery/player inventory indices.
- Keep bee specimens, serums, jelly, smelting flux and recipe catalysts separate from upgrades.
- Preserve existing unpowered Geno Station slow analysis unless separately changed; no free powered operation or stronger splicing chance from cards.
- Charge upgraded jobs conservatively over their actual shortened duration, with integer rounding that never grants unpaid products.
- Test valid/invalid card families, bounds, blocked outputs, removal during processing, reload, menu transfers and break refunds.
- Keep Compact and Void deferred for these four machines until their own storage/output rules are defined. Other legacy machines without approved powered contracts remain unchanged.
- Artwork, client GUI approval and exact survival crafting costs remain separately tracked.
