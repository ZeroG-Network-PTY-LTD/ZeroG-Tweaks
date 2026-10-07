# Progression follow-up — 8 October 2026

This batch extends verification after the delivered four-altar Vault repair.
The installed same-version JAR, hub and client saves are not replaced or edited.
Code, Design and Docs were fetched first; reviewed heads were `8fe807fa`,
`5da88178` and `5c7cba3a`, respectively.

## Interaction checks

The new isolated tests exercise public block interactions, rather than directly
granting items or setting a completed lock. They check four separate altar claims,
one key per claim, three room guardians and no repeated rewards from empty altars.
The chamber test inserts four survival keys into each of the four horizontal
lock orientations. Each of the first three stages is compared against the
authored template's transformed block positions; the fourth must create an idle
Concord Prism with a real encounter block entity. Wrong items must not advance
the lock or be consumed.

The final revision passed all seven required tests in
`20261007_173420_runWorkflowTests.log`, including Prism clicking and
authoritative summon-delay work. In each orientation the idle Prism became
active, rejected a second start and summoned a real first-challenge Sentinel.
The ticker work was invoked directly; this does not certify real-time combat.
The earlier altar/stage revision also passed seven tests in
`20261007_172909_runWorkflowTests.log`; these are repeated checks, not14 distinct
tests. The first
launch (`20261007_172253_runWorkflowTests.log`) selected no tests because the
namespace did not match the template namespace. Although Gradle exited
successfully, this is **not** gameplay-test evidence. The corrected launch uses
the shared namespace and native-dimension fixture alongside earlier regressions.

These fixtures do not certify natural room traversal, Sentinel combat, boss loot,
the later guardian keys, save/reload of an active fight or graphical approval.

Clean production build `20261007_173907_clean.log` passed without test flags.
The rebuilt JAR contains no GameTest classes and is byte-identical to the installed
Vault repair (`ccea0e94cf91e1adc9ff1c74a9978de07f599caf5bbc50a806f26e9c61313295`).
Asset bindings passed with zero errors across7977 models,1528 blockstates,
3962 PNGs and129 animation metadata files. This audit-only batch therefore does
not replace the installed JAR or add a duplicate archive. Evidence hashes and
scope are recorded in `vault-progression-checks-20261008.json`.

## Structure/reward source graph

`tools/audit_structure_routes.py` reads the shipped compressed NBT templates and
follows start pools, fallback pools and jigsaw connectors, including nested list
elements. Three small unit checks cover cycles, missing references and exclusion
of zero-weight/feature elements. It does not touch saves or generate terrain.

The current graph contains four configured jigsaw structures: Concord Vault,
Mars Aresite Shrine, Mars Crash Site and Prism Sentinel Arena. Their referenced
pools/templates are present. The Vault has potential common/uncommon/rare chest
routes. Possible source reachability is not proof a particular room was selected,
placed or accessible, nor that a reward rolled.

The graph does **not** provide generating structures for Sunken Relay, Buried
Observatory, Collapsed Forge, Frozen Outpost, Sunken Lab, Prism Spire, Impact Site,
Derelict Wreck or Solar Shrine. See `structure-routes-20261008.json`.

Important exceptions: Java places the Courier and chamber stages directly.
Planet Mineshafts already use the Buried Observatory loot table; that is not an
implemented Buried Observatory structure. Loot tables and preview exhibits are
not a substitute for each missing ruin, its intended habitat and player access.
Processors, external datapacks and hidden-world coordinates require separate
checks. No story text, dimensions or new reward routes were invented here.

## Existing-save limitation

The shipped Vault structure set uses one concentric-ring placement (`count: 1`).
If an old world has already generated that Vault, simply exploring more Cerulon
chunks must not be advertised as producing a replacement Vault. The repair does
not retrofit its saved structure. A separate approved world-reset or migration
would be needed to repair that existing encounter; this batch performs neither.

## Remaining order

1. Reconcile missing ruin geometry/habitats/rewards with the Design/lore trackers.
2. Broaden ordinary-world village, cave, vegetation and natural-spawn sampling.
3. Verify chest rolls, natural encounter traversal, combat and active-fight reload.
4. Audit later guardian encounters, templates and gate-key usage without changing
   the owner's existing four-loot-room-key sequence.
5. Keep undefined biology, seven-wide layouts and exact survival costs pending.
   Remaining machine recipe pages remain deferred; client approval remains yours.
