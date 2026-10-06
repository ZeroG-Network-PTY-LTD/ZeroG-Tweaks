# Sol lore gaps and next workflow

Minecraft Java1.21.1 / NeoForge; candidate remains1.0.12-dev.
Lore source: [Design lore guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/lore/README.md).

## Immediate lore batch

- Add a single hand-cut Aresite core shrine to each of the four Rustborn settlement
  layouts. Reuse the existing Aresite block and Martian brick artwork on a low
  ground-level pedestal, clear of houses, crop fields and the resident anchor.
  The existing large standalone shrine and its loot must remain untouched.
- Move Moon Relay and Mars Waystation Codex page text into language keys without
  changing the approved English story. Pages remain arrival-gated; no premature
  reveal of the Concord/Splinter identity or later acts.
- Test actual settlement construction for all four layouts and the Codex's item
  interaction before claiming these implemented. The Codex test uses real Moon/Mars
  level contexts, not a portal/network simulation. Isolated tests do not certify
  visual composition or physical player travel.

New generation only: existing player villages are not retrofitted. The owner later
explicitly requested a no-backup planetary reset in the Cardinal Hub save. All34
ZeroG planetary terrain folders were removed, planetary gate preparation was reset,
and the Overworld hub, player inventories, Nether and End were preserved. Terrain
and return gates regenerate on the next world load; no client was launched here.

## Installed checkpoint — 7 October 2026

The four-layout shrine check passed through actual settlement construction. The
independent required shrine test passed in20261006_233803_runWorkflowTests.log;
the earlier mixed Codex/shrine run failed and is not reported as a full-suite pass.
Runtime commit:e21c82be; Design tracker/lore commit:216a5659.
Installed JAR SHA256:
`1ec1545cc4348dea623fd39f6f5b71338c59852f118e16a6748e7c262ba1eeb2`.
See the [delivery receipt](sol-shrine-delivery-2026-10-07.json) and
[same-version archive](jars/zerog-tweaks-1.21.1-1.0.12-dev-sol-shrine-20261007.jar).

The production build passed and the asset audit found zero errors across7949 models,
1522 blockstates,3932 PNGs and118 animation metadata files. The same-version JAR
was installed with its predecessor backed up before publication.

Codex localization remains **pending**. Its initial item-interaction test could
not reach the arrival assertions because the disposable world lacked Moon/Mars
levels. This is not a successful arrival test or an implemented translation fix.
The current release retains the existing approved English page wording and gating.
The pending test must load a planetary preset before testing localization and
arrival; the published shrine regression is independently runnable.

## Meteor Maw debris — owner decision7October

No Broken Console mob drop. Consoles are important Courier/Eidolon story blocks,
not generic whole-block loot from a beast. Existing Star Map Fragments are the
interim lore carrier. Future small Moon impact wrecks may contain approved crater,
meteorite fragments, pod-shell and chest pieces, but **no Dormant Wisp, Codex or
console**. This future wreck is pending, not a completed structure or a Sol blocker.
No additional loot or new story logs are authored in this batch.

## Machine recipe tabs explicitly deferred

Only Alloy Forge, Ore Refinery, Crystal Growth Chamber and Salvage Station currently
have the shared exact recipe/combination browser. Accepted-item lists on other
machines do not count as recipe pages. The owner requested the remaining adapters
later, so they are retained in the TODO ledger rather than dropped or claimed done.

Audit Silk Weaver, Starmetal Smelter, centrifuge, genetics, generators and bee
machines. Show actual combinations, alternatives, counts, catalysts, outputs and
FE/time from each machine's true operating rules, not invented generic recipes.
Generators need truthful fuel/output/environment pages appropriate to their purpose.
Preserve input slots and server contracts; leave client layout approval separate.

## Following this lore batch

Continue safe Compact storage, selective Void filtering, remaining machine
contracts, transport visuals, Codex research/biology and ecology in verified slices.
Deferred impact-wreck design, remaining recipe adapters and exact survival costs
are not blockers for work with existing approved specifications. Undefined gases,
hidden coordinates, later-act text and biology rules still require specifications;
do not invent them to make a tracker appear complete.

Install a backed-up verified same-version JAR before publishing code, Design and
Docs separately. The final delivery receipt records tests, asset audit and checksum.
