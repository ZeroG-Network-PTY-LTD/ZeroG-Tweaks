# Gate auto-build and launch-lift repair

Minecraft 1.21.1 / NeoForge / unchanged 1.0.12-dev version.

## Use the builder

1. Place your Gate Controller and open it with an empty main hand.
2. Choose **Plans → Plan T1** to inspect the standing layout.
3. Carry the missing blocks in your inventory. A fresh Tier 1 build needs
   16 Nullifite Gate Frames, 9 Gate Pad Plates, 12 Gate Pylons and 1 Gate Energy
   Port, in addition to the already placed controller.
4. Choose **Build T1**. Matching blocks already placed are credited. The builder
   retains your controller, checks all missing materials before construction,
   and consumes only those missing blocks. Creative players also supply them.
5. For upgrades, inspect **Plan T2–T6** and use the matching **Build** button.
   Block requirements come from the actual gate geometry, not a separate recipe.

The builder refuses unloaded/out-of-border positions, blocked cells, another
block entity, a failed permission check or a conflicting final formation.
Failed formation restores the newly placed cells and consumes no materials.
It does not excavate, overwrite other buildings or create another controller.
Vanilla permission checks do not certify arbitrary third-party claim protection.

## Launch and travel

1. Connect power to a **Gate Energy Port** and watch the controller's shared FE.
2. Choose **Worlds** and select Moon or Mars for Tier 1. The selection gets a
   visible `>` marker; the current dimension is not a travel destination.
3. Stand on the pad and press **Engage**. The initiator is already Ready;
   other passengers must confirm Ready before the countdown finishes.
4. Stay horizontally over the pad during the lift. Confirmed passengers now
   remain in the launch sequence when raised above the ordinary pad ceiling.
   Leaving sideways, changing the group or breaking the gate still cancels.
5. Successful travel sends the ZeroG destination/transition message and deducts
   the fee once. The console also records a successful-travel receipt.

Refused engagement now explains incomplete structure, pad position, passengers,
insufficient FE or invalid selection. Cancelled countdowns explain changed
structure, group or destination. Failed launch preparation reports that no fee
was deducted. A refusal is not represented as a successful teleport.

## Tier reach and fees

| Tier | Newly reachable worlds | FE per successful group jump |
| --- | --- | ---: |
| 1 | Moon and Mars | 100,000 |
| 2 | Cerulon and Galaxy 2 planets/moons | 200,000 |
| 3 | Skarn and Galaxy 3 planets/moons | 400,000 |
| 4 | Eidolon and Galaxy 4 planets/moons | 800,000 |
| 5 | Solvane and Galaxy 5 planets/moons | 1,600,000 |
| 6 | All already unlocked galaxy destinations | 3,200,000 |

Higher tiers retain earlier destinations. Admin hub permissions and free travel
are unchanged. The previous client-only Tier 6 restriction on galaxy moons was
inconsistent with both the server and approved Codex; it has been removed.

## Verification and remaining approval

A red regression reproduced cancellation when a passenger rose above the old
pad ceiling during the actual countdown. After the repair, all eight required
`zerog_gate_display` / `zerog_workflow_optional` tests passed, including all six
inventory-funded build tiers, exact consumption, missing supplies, obstruction
conservation, co-op return travel, and the lifted passenger's actual travel/debit.
Transcript: `20261008_231448_runWorkflowTests.log` (UTC filename).

The initial Tier 6 build-test failure was caused by the disposable fixture's
barrier ceiling, not production geometry. The test clears its construction
envelope; the production builder continues to refuse barriers and obstructions.

Two actual outbound tests also passed: Tier1 reached both Moon and Mars,
created/reused bound Tier1 return gates and deducted exactly100000FE per jump.
The destination payload codec retained its fields. Transcript:
`20261008_231556_runWorkflowTests.log` (UTC filename).
The final delivery checksum is recorded below when completed.
Installed-client appearance of the transition,
buttons and hologram still needs player approval; server tests do not verify it.
No hub reset, dimension regeneration or save modification is part of this repair.

Survival crafting balance, third-party claims, and the broader machine/alveary
TODO remain separate pending work.

## Delivery

Clean production build passed (`20261008_231740_clean.log`). The production
archive contains no isolated test fixtures/classes; 7979 models,1529 blockstates,
3963 PNGs and130 animation metadata files passed the asset audit with zero errors.

Installed into the existing ZeroG CurseForge mods directory, with the prior
JAR backed up outside mods. Published candidate:
`docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-gate-autobuild-lift-20261009.jar`.
SHA256: `59a37824b15e1bdf86856ef8eca1245af498de4ec252e4aa9e8056520a0f3c94`.
Backup: `ZeroG/zerog-jar-backups/zerog-tweaks-before-autobuild-20261009-b6125e58.jar`.
Its SHA256 is `b6125e58ed4e36cb10d9e6bfa65c01696fb414c2e41d836310d4393881354d31`.
Only the main Tweaks JAR was replaced; the Binnie addon and other mods were kept.
Saves, hub, shaders and instance settings were untouched.
