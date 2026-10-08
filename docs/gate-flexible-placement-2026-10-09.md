# Flexible Concord gate service blocks

Minecraft 1.21.1 · same-version 1.0.12-dev · repository candidate, not installed.

## Building and diagnosing a gate

Build the required foundation, pad, pylons, arches, lenses and cores using the [tier guide](gate-building-tiers-1.21.1.md). Its C/E positions are examples, not fixed sockets.

At one block above the pad, place exactly one controller and the tier's minimum Gate Energy Ports: **1, 1, 2, 2, 4, 4** for tiers 1–6. A legal position has `max(abs(x),abs(z))` between 2 and `tier+1`, measured from the pad centre, and does not replace a required structural block. Any horizontal side is allowed. Terminal facing is cosmetic; geometry determines the structural orientation.

Ports share the controller buffer and combined per-tick intake limit. Additional legal ports do not multiply the intake budget. Generic apiary ports are not gate ports. Two controllers in one service row, ambiguous overlapping formations and a port shared by complete gates are rejected.

Open **Preview** for missing blocks grouped by structural section. **Ghost** draws a temporary wireframe; its suggested missing-port positions may be replaced with other legal service positions. **Align** rechecks without rotating the terminal or placing blocks. A complete lower tier is valid even if an optional higher-tier upgrade is unfinished.

## Safety and persistence

- Ordinary formation and capability checks inspect loaded chunks only, with bounded candidate searches.
- Cached energy handlers revalidate formation; removed ports and replaced controller entities cannot receive stale transfers.
- Ownership, FE, selected destination, upgrade inventory and return bindings retain their existing saved format. Breaking and placing a new controller does **not** automatically migrate the old controller's saved contents.
- Remote travel explicitly loads a bounded footprint. Bound landing lookup searches its service area rather than one fixed controller column. A damaged existing return gate blocks travel without overwriting player changes or charging a failed launch.
- Admin travel remains restricted to designated hub controllers and their bound returns; arbitrary relocated terminals do not gain admin privileges.

## Verification record

The test-first legacy run failed relocated Tier-1 formation (`20261008_210911_runWorkflowTests.log`). An earlier incorrectly filtered run discovered zero tests and is not passing evidence.

The corrected formation/power suite passed **16 required tests**, including the **384-case** six-tier/orientation/controller-side/port-side matrix, opposite-side generator/conduit charging, duplicate/shared-service rejection and save/reload/stale-handler checks (`20261008_212014_runWorkflowTests.log`). One old fixed-coordinate assertion was updated because missing-port sockets are now flexible; its charging and handler-revocation checks remain.

The pure saved-world audit mirror passed **96 synthetic layouts**. These do not certify an actual player save or client rendering.

Three isolated optional-absence tests passed relocated co-op return travel, one-time FE charging, non-owner controls, preserved-data bound-return reuse and damaged-landing non-overwrite (`20261008_212300_runWorkflowTests.log`).

Four focused tests also passed with Productive Bees 13.14.0, Productive Lib 0.2.0 and ZeroG Orbital-Bees 1.0.0 present (`20261008_212359_runWorkflowTests.log`), including the full 384-case relocation matrix. The focused namespace now owns its own fixture, so it can run without the mock-player tests. All disposable servers saved and stopped normally.

Clean production build passed (`20261008_212614_clean.log`). The packaged asset audit checked 7,977 models, 1,528 blockstates, 3,962 PNGs and 129 animation metadata files with **zero errors**, including no workflow test classes in the production archive. This is an asset-binding check, not visual approval.

Candidate: [same-version flexible-gates JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-flexible-gates-20261009.jar).
SHA-256: `e1426e0ce40d74fd703294b018f19a2792276f37b1ea6284467c9f340f52d622`.
Code commit `4e799a27`; editable Design generator `ee18a527`. The installed JAR
remains `83e80cedb9414f95d8577a9c2f9f4d3553ba81a34b31b8aef4c49fc5612b1020`.

## Still pending

Client visual approval of Ghost/Preview, actual player-built service layouts and existing-world travel remains required. No installed JAR, hub or planetary terrain is changed by this batch.

Next: remaining machine recipe/combination pages and upgrade support. Exact survival crafting costs, undefined advanced bee research rules and deferred artwork remain separate TODOs; this gate change does not claim they are implemented.
