# Stardust Smelter fuel repair — 11 October 2026

Minecraft 1.21.1 / NeoForge, same candidate version `1.0.12-dev`.

## Reproduction and cause

An isolated real-addon test placed a Meteor Comb into a fresh Stardust Smelter,
left fuel empty and called its actual processing entry point 201 times.
It failed with **Stardust processed without fuel**. The other three recipe tests
passed. Evidence: `20261011_000410_runWorkflowTests.log`.

The installed recipe ignores its second input. The generic `processTwo` runner
neither checks nor tracks fire; it shrinks the second input once at completion.
Fresh machine reproduction rules out old saved progress. Stardust was not handled
by a replacement runtime before this repair. No third-party code/art is copied.

## Repair contract

- Use the existing installed comb-to-Stardust function: Meteor 2, Nebula 3,
  Molten 1. No new materials, yields or survival crafting costs.
- Require a saved hot-tick budget from Minecraft/NeoForge smelting fuel durations.
  Consume one fuel item at ignition, not every finished comb. Preserve container
  remainders, including the empty lava bucket. Reject invalid fuel through menu
  and automation filters; old invalid contents remain removable.
- Keep the existing 201-tick completion boundary. One coal's 1,600 ticks cover
  seven continuous jobs plus 193 ticks. Already-lit fire decays while idle/blocked;
  a cold blocked job does not ignite. No comb is consumed until its complete output
  fits. Loss of heat resets incomplete work without consuming inputs.
- Save remaining fire and progress. Reset work on changed comb identity/components.
- No FE, cards, gas or fluid machinery is invented. Existing side controls remain.
- Read-only Items/Recipes/Upgrades pages show exact comb outputs, duration and
  selected fuel budget; fuels are a shared fire budget, not per-recipe catalysts.
  Matching runtime/Design Codex chapter documents these rules.

## Verification

All five required isolated tests passed in `20261011_000636_runWorkflowTests.log`
(985.3 ms of GameTests; 51-second full run). The original fuel-free reproduction
is now green. All three outputs were checked across two jobs each, exact coal
burn accounting and mid-job reload; invalid automation inputs, blocked cold
ignition, lit blocked burn decay and lava-bucket remainder were verified. Previous
frame/infusion, centrifuge/smelter cards and Weaver regressions also passed.
Clean production build passed in 49 seconds (`20261011_000755_clean.log`). Asset
audit: 7,979 models, 1,529 blockstates, 3,963 PNGs, 130 animation metadata files,
zero errors and no optional test classes/fixtures. Runtime/Design Codex bodies
match. No textures or IDs were changed.

Installed with Minecraft closed at the existing ZeroG mods path. SHA256:
`75e38ea43cbf256689ef619307c47b1bc3d4671fef4270caec2fccb791b7313c`.
The previous build is retained under `ZeroG/zerog-mod-backups/20261011-000935-UTC/`.
Other installed dependencies retain their hashes. No debug instrumentation remains.
This bug would have been caught by a fuel-empty real processing test; that
regression now ships only in the opt-in test source set, not the production JAR.
Client layout/cursor and graphical machine activity
remain pending the owner's play-test. No hub, save, gate or weather changes.
