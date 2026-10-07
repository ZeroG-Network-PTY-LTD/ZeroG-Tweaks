# Usage-window workflow — 7 October 2026

Owner direction: continue approved TODO work with disposable tests, switch to
light verification and publication at10% remaining usage, then install one verified
same-version JAR near the end. Do not repeatedly replace the installed build.
The account reset is15:30 Bangkok; the configured follow-up is15:35.

## Repairs completed in this batch

- Galaxy2–5 moons now follow their respective survival gate tiers instead of
  requiringT6. Lower-tier exclusions, self-route exclusions and admin hub travel
  remain intact. A real formed-gate regression failed before the fix and passed
  afterward, including downgrade and reload.
- The approved temporary Cerulon template fallback adds Cobaltium, Cyrrium and
  Aurelion templates to uncommon Concord Vault chests. Loaded loot rolls and the
  forge/library template bindings pass. This is not proof of a natural encounter;
  Prism Spire construction remains pending.
- GuideME'sT2 page describes those routes and the temporary chest source honestly.
- Glacial Ice uses approved0.98 friction and glass sounds; strength is unchanged.
- Vent Rock emits cosmetic, unobstructed campfire smoke through client animation;
  it adds no damage, persistent ticker or shared server random access. On-screen
  particle appearance still requires client approval.
- Transport layout changes now revoke same-tick cached networks across affected
  neighbors. The five-hazard/six-tier sweep exposed stale topology after pipe
  replacement; invalidate on placement/removal, neighboring changes and validated
  side/redstone commands. Rejoined edges must invalidate both cached components.
  The descending-tier sweep checks60 simulated/actual fill boundaries; the final
  integrated rerun must also pass the disconnected/rejoined-edge regression.

## Evidence and its limits

Final integrated run `20261007_045235_runWorkflowTests.log` passed all26 required
checks. It includes the final reconnect invalidation repair, the60 hazardous
fill boundaries, previous Codex/loot/gate regressions and the bounded native
ecology report. The failed pre-repair tier sweep remains recorded separately in
`20261007_044832_runWorkflowTests.log`; do not count it as a passing suite.

`20261007_043441_runWorkflowTests.log`: all6 required progression/loot/Codex/ice
checks passed. The later Vent Rock change is not covered by that test run.

`20261007_043935_runWorkflowTests.log`: all23 required combined checks passed,
including open/covered Vent Rock callback behavior, all36 junction direction
combinations, committed/blocked power delivery and existing gas/network boundaries.
The callback/axis checks do not certify on-screen smoke or ribbon appearance.

The static machine GUI profile audit checked37 profiles without errors. It cannot
certify font rendering, real screen scaling, shaders or overlap in the player's
client.

`20261007_043115_runWorkflowTests.log`: the independent native ecology test passed.
It generated108 native chunks at two sampled sites per Sol planet, finding ores
and distinct sampled heightmaps. Reports retain actual blocks, sampled biomes and
structure starts. Zero structure starts in this small sample does not establish
that rare structures are missing. Natural mob spawning, village distribution,
all-biome coverage and GPU appearance remain unverified.

The native Vault locator experiment failed. Inspection of the actual1.21.1
GameTestServer source established why: its WorldOptions are `(0,false,false)`,
disabling natural structures even with a native planetary noise generator.
Therefore zero observed structure starts are a harness limitation, **not evidence
of a production worldgen defect**. The unsupported experimental test was removed;
natural Vault acquisition must be checked in an isolated ordinary dedicated world.
Do not count the failed experiment as a pass or weaken production generation to
satisfy this harness. The ecology report now records structures-enabled explicitly.

The earlier combined ecology/hub test failed because the isolated no-addon world
could not complete the bee gallery. Do not report that entire run as passed; the
independent ecology rerun is the valid evidence. No player saves were accessed.

The final scoped ecology run `20261007_044541_runWorkflowTests.log` passed.
Its [report](native-planet-ecology-audit-20261007.json) also lists loaded spawn and
feature settings for all24 possible biomes of the six Sol generators. These are
configuration observations, not proof that a mob spawned or every biome was
sampled. [Static progression provenance](progression-source-audit-20261007.json)
separately identifies22 reward items, four configured structures and four chest
families without shipped template bindings. Java references alone remain unproven.

## Explicitly pending

- Owner deferred the per-trait Codex research map. Productivity, endurance, temper,
  behavior and weather tolerance must not get invented milestone assignments.
- Higher-galaxy first-template acquisition still needs structures/rewards and
  natural-generation verification, not merely loot files.
- Natural structure/village rarity checks must use an ordinary disposable server
  world with structure generation enabled, not the vanilla GameTest harness.
- The loaded spawn tables include Rust Beetle/Dune Burrower/Dust Grazer on Mars,
  but missing later signature mobs and boss phases remain unfinished. A configured
  spawn is not an observed living mob or a behavior/texture test.
- Seven-wide alvearies and advanced biology need approved layout/module rules.
- Remaining machine recipe adapters and exact survival crafting costs stay last.
- Client GUI/art/transport approval remains separate from server checks.

## Delivery state

Final delivery: installed once at the10% remaining checkpoint, same1.0.12-dev.
SHA256 `054474ddc6013ae9c7a750360a65412b723dd5b8ded71526e64cd46204fe3b5c`.
The previous JAR is recoverably stored in `20261007-045548-UTC`. No hub/save
changes or client launch. Code commit `ebc6e54a`; Design generator commit
`7c281690`. The [delivery receipt](usage-window-delivery-2026-10-07.json) records
the production build, passing26-test suite, asset audit and archived JAR.

### Historical staging policy

Installed build remains the previous Codex/clean-hub checkpoint until the final
delivery receipt says otherwise. A production build or commit alone is not proof
of installation. Preserve the compact hub and all saves in this workflow.
Record final branch commits, build/audit results and installed checksum here or in
a linked receipt before waiting for the reset.

## Repository synchronization caution

This checkout retains a stale fetch specification for the former
`design/v1.2-assets` branch. Fetch current branches explicitly. On Windows, the
historical lowercase remote-tracking path conflicts with `origin/Design`.
Use an alternate local tracking namespace for the current Design branch rather
than deleting or force-updating any remote branch. Fetch checks found no new
contributor commits beyond the already integrated checkpoints in this batch.
