# Frame and infusion recipe discovery — 11 October 2026

Same-version 1.21.1 / NeoForge candidate, `1.0.12-dev`.

## Verified processing contracts

The installed orbital addon was inspected read-only. Its `ZeroGMachines.tick`
dispatches both Frame Assembler IDs to `ZeroGSlotFamilies.frame` and both
Infusion Altar IDs to `ZeroGSlotFamilies.infusion`. These are real processing
functions, not conclusions drawn from artwork or GUI profiles.

The recipe browser now enumerates accepted inputs and queries those installed
functions. Both ingredients are consumed, one of each, at the 201-call boundary.
The existing machines do not require FE and do not support upgrade cards; the
browser does not invent energy costs, sockets or effects.

| Machine | Slot 0 | Slot 1 | Result |
| --- | --- | --- | --- |
| Frame Assembler / Frame Component Assembler | Untreated Frame | Honeycomb | Impregnated Frame |
| Same | Untreated Frame | Starmetal Ingot | Starmetal Frame |
| Same | Untreated Frame | Woven Silk | Aero Silk Frame |
| Frame Infusion Altar / Infusion Altar | Impregnated Frame | Amethyst Shard | Proven Frame |
| Same | Impregnated Frame | Cosmic Jelly item | Cosmic Vigor Frame |
| Same | Impregnated Frame | Stardust | Starlit Frame |

Results occupy slot 2 except Frame Infusion Altar, which uses slot 3. Its unused
slot 2 remains recovery-only. Browsing does not execute recipes or move items.
The gravitational centrifuge alias now uses the actual centrifuge output
function without falsely advertising the ordinary centrifuge's FE/card support.

## Important remaining Stardust Smelter discrepancy

The installed `stardust` function ignores its second argument. `processTwo`
therefore permits empty fuel and consumes one item from an occupied fuel slot
on completion, rather than running a normal furnace burn-time budget. Meteor,
Nebula and Molten combs produce 2, 3 and 1 Stardust respectively.

Keep its recipe adapter pending until this fuel contract is repaired or approved.
Do not describe it as a working vanilla-fuel furnace from its profile text alone.
No fuel behavior or survival costs were changed in this read-only recipe batch.

## Verification and handoff

The added isolated test checks every combination on all four registered blocks,
output-blocked conservation, exact completion timing, quantities and alias
coverage. Existing ordinary centrifuge/smelter card and Weaver recipe tests are
included in the same namespace. All three required tests passed in
`20261010_235425_runWorkflowTests.log` (949.3 ms of GameTests; full run 1m26s).
Client layout, scrolling and cursor interaction remain
pending the owner's safely parked play-test; no save, hub, gate or weather reset.

Clean normal build passed in 50 seconds (`20261010_235556_clean.log`). The asset
audit found zero errors across 7,979 models, 1,529 blockstates, 3,963 PNGs and
130 animation metadata files; optional test classes/fixtures are excluded.
Runtime and Design Codex chapter bodies match. No new textures were needed.

Installed with client process count zero:
`ZeroG/mods/zerog-tweaks-1.21.1-1.0.12-dev.jar`.
SHA256: `ece8ec90d1c8d1423a34d8a288b1e9af37b9c028b6182ff98d15f1d1c6223500`.
Previous build retained under `ZeroG/zerog-mod-backups/20261011-000200-UTC/`.
Orbital addon, Productive Bees and GeckoLib hashes remain unchanged.
