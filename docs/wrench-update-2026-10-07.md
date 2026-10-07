# Latest contributor changes and transport verification

Installed contributor runtime commit `523033eb` in the existing Minecraft
1.21.1 / NeoForge `1.0.12-dev` JAR. No version bump, client launch, hub rebuild
or save modification. The previous installed JAR was backed up outside `mods`.

## What changed

- Pipe hitboxes follow their narrow cores, connected arms and machine plates.
- Flux Wrench has Configure and Wrench modes, selected with shift-scroll.
- Configure reads a side; shift-click cycles its routing state. Arm clicks target
  the arm direction. Wrench mode shift-click retrieves blocks with their contents.
- Tanks use the same mode distinction.

## Verified boundaries

Production build `20261007_161240_clean.log` passed. The packaged asset audit
checked7977 models,1528 blockstates,3962 PNGs and129 animation metadata files
with zero errors. This is not graphical approval.

Isolated run `20261007_161531_runWorkflowTests.log` passed all19 required tests.
The new regression checks all six arm directions, centre-click fallback and
core/connected-arm hitboxes for energy, liquid, gas and item lines. Existing
gas conservation, committed/blocked visual payload and mixed-tier hazardous
fluid safety tests were rerun. Inventory pickup contents, client shift-scroll,
GPU visuals and actual click feel still require further tests/client review;
do not imply the new geometry test covers those interactions.

Startup took longer than prior runs; a read-only thread snapshot showed active
compilation/chunk work, and the test completed without intervention. No gameplay
performance fix was inferred or applied from startup duration alone.

## Next work

Tracker reconciliation: the older `per-machine-upgrade-contracts` entry's
"genetics/legacy compatibility pending" wording is stale. Acceleration and
Energy Coil support for Geno Station, Genetic Splicer, Centrifuge and Starmetal
Smelter was already delivered and tested in the genetics/legacy cards batch.
Compact/Void support for those machines remains distinct and undefined; this
update does not add it. The historical68-gate service-hub description likewise
does not describe the current compact six-tier hub. Preserve historical delivery
records, but use the newer compact-hub notes for current behavior.

1. Ordinary disposable-server natural structure and village verification.
   Vanilla GameTest disables natural structures and cannot certify this.
2. Remaining wrench pickup/preservation and actual interaction boundaries.
3. Reconcile higher-galaxy progression and missing signature mobs/structures.
4. Client GUI, transport and artwork approval.

Keep undefined per-trait research milestones, seven-wide layout/module rules,
cooling quantities and exact survival costs pending. Remaining machine recipe
combination pages stay deferred by owner direction. Preserve all earlier notes.

The usage-reset follow-up was paused after handling today's reset; it will not
repeat this workflow daily.
