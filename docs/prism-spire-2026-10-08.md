# Prism Spire — crystal-wasteland ruin

First implementation of one of the seven pending wasteland ruins. It uses the
existing approved Prismstone family and Pulsar Lamps, not new texture placeholders.
No new story logs, hidden coordinates or bosses are invented. The Design generator
and its generated resource copies are kept separate from runtime data on1.21.x.

## Finding and exploring it

The Spire is eligible in Wasteland Prism Fields and Crystal Caverns, including
the default Galaxy2 crystal slot (`g2_p6`). It is not an admin-hub exhibit.
Initial placement spacing is40 chunks with20-chunk separation; wet and excessively
uneven sites are rejected. This does not guarantee a Spire in every placement
region. Existing chunks are not rebuilt, so explore fresh terrain.

The15×23×15 ruin has three floors, a broad ground-floor entrance, a continuous
backed ladder through the floor openings, damaged windows and a fractured crown.
The top chamber contains one real chest with open lid clearance. Its unchanged
`chests/prism_spire` loot guarantees a Refracting Lens and can yield Cobaltium,
Cyrrium and Aurelion upgrade templates, alongside its existing supplies.
Those three templates also already have the earlier Concord Vault uncommon-loot
fallback; the old Galaxy2 tracker incorrectly described that fallback as absent.

## Evidence boundaries

All9 required isolated tests passed in `20261007_182046_runWorkflowTests.log`.
Two new tests cover four placed-template rotations, a real chest's guaranteed
lens, sampled template rewards, backed ladder clearance and at least one valid
dry crystal-terrain generation start in a bounded64-candidate search.
The seven existing Vault/access regressions also passed. The server stopped
cleanly. These are9 tests, not9 new tests.

The initial run failed before delivery: depth0 produced no jigsaw pieces, and
the initial ladder assertion incorrectly rejected floor landings. Depth1 is
now used in both generator and runtime settings, with correct floor-exit checks.
The original failing transcript is retained separately. No debug logging was
added to production, and no installed build ever contained the invalid setting.

Scripted template placement, loaded loot rolls and terrain-generation calls are
not proof of natural chunk placement, survival navigation, client appearance or
final rarity balance. No hub or player save is reset for this change.

## Same-version delivery

The subsequent ordinary seed0 server had structures enabled and no GameTests.
`/locate` found a natural Spire at [96,~,48] in `g2_p6` (start chunk6,3).
A saved49-full-chunk window contains its valid one-piece jigsaw start and one
actual unopened chest bound to `chests/prism_spire`; see
[saved-chunk evidence](ordinary-prism-spire-20261008.json).
Two mineshaft chests in that window use Buried Observatory loot; they are not
proof of an Observatory structure. This is one natural sample, not rarity
balance, broad-seed ecology or player-navigation approval.
All81 temporary crystal-dimension force loads were removed and the disposable
server was stopped after inspection. No client save was used.

Clean production build `20261007_182754_clean.log` passed without test flags or
GameTest classes in the JAR. Asset audit reports0 errors across7977 models,
1528 blockstates,3962 PNGs and129 animation metadata files.
The installed and archived JAR SHA256 is
`3fe1deb13ca89bd3bb2e1ed1107cfe612a2a44a537f10959ce375f393be4450f`.
The prior installed JAR was moved into `zerog-mod-backups/20261007-183107-UTC`
outside the mods folder. Other mod JARs are unchanged. See
[delivery evidence](prism-spire-delivery-2026-10-08.json) and
[the matching archive](jars/zerog-tweaks-1.21.1-1.0.12-dev-prism-spire-20261008.jar).
The isolated workflow server shut down cleanly after its successful run.

## Next

Implement the six other wasteland ruins plus Eidolon wrecks and Solar Shrine.
Keep their appropriate habitat/reward contracts separate from the presence of
loot JSON. Undefined story text, hidden coordinates, bee biology and final
survival costs remain pending owner approval.
