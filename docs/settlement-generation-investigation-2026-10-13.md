# Natural village and mine generation investigation

Owner reports a fresh world with no visible villages and too few/small mines and
structures. This supersedes routine ecology audit priorities. No installed JAR or
player terrain has been changed by this investigation. Ollama/Kimi is not in use.

## Read-only save evidence

The discovered `1_21_1 alpha` world has seed `-323417769491979004`, structures
enabled, 37 dimension definitions, and saved planetary terrain only on Moon.
Owner confirmed this is the reported world.

A bounded region-header/candidate inspection found 12,589 saved Moon chunk
records intersecting eleven 50-chunk candidate regions. Six candidate chunks have
records, but only two are FULL. Neither FULL candidate has a settlement anchor:
`(27,22)` and `(25,66)`. The four STRUCTURE_STARTS records are not failed village
attempts: feature decoration has not completed there. No inventory/player data was
read. Saved records and halo chunks are not all explored/rendered terrain.

Current MOTION_BLOCKING_NO_LEAVES heightmaps across the two 35x35 footprints span
56 and 9 blocks respectively. These are preliminary saved-heightmap observations,
not exact generation-time solid-ground rejection reasons. Flora/logs and later
terrain changes can affect heightmaps; no cause is claimed from them alone.

## Isolated ordinary-world checks

Seed 0 Moon candidate `(24,70)` naturally generated a settlement anchor, with
six ordinary residents and two specialists recorded, native Moon farmland and
Hoarwood doors. The anchor counters record creation, not a current live entity
census or player-visible approval. The 20 FULL chunks inspected also include a
buried-observatory loot chest; this is not a complete mine-size survey.

Seed 0 Cerulon candidate `(32,77)` has 25 inspected FULL chunks, no anchor and no
local farmland/doors. This is a failed candidate, not a global absence claim.

Seed 0 Eidolon `(22,67)` and Solvane `(18,83)` likewise have 25 inspected FULL
chunks each and no village anchor. Their samples contain four and three
buried-observatory chest bindings respectively, consistent with mines generating
in those samples; exact corridor sizes and rolled loot remain unverified.
Total: four candidate sites, 95 FULL chunks in their inspection windows, one
settlement anchor. These fixed samples are not a population-density estimate.

The read-only missing-village check was run against the discovered fresh save:

```sh
python3 tools/audit_settlement_candidates.py --world '/mnt/c/Users/jakem/curseforge/minecraft/Instances/ZeroG/saves/1_21_1 alpha' --dimension moon --require-settlement
```

It returns exit 1: `FAIL: no village anchor at any saved FULL candidate`.
The three deterministic candidate reproduction/negative-region tests pass.
This provides a repeatable symptom check, not a verified root cause or repair.

## Original limits and follow-up work

- Villages try one seed-selected chunk per 50x50-chunk region. They rejected wet or
  non-solid sites, then required every graded column to stay within four blocks of
  the centre. A rejected site currently has no alternate candidate.
- Mines attempted one in eighteen chunks before validation, with a 30-block main
  corridor and two to four 10/15-block branches. These are deliberately bounded
  small mines, not extensive vanilla-sized networks.
- Audit the exact reported save/seed with an isolated reproduction. Distinguish
  slope, fluid and chunk-write boundary rejections before changing validation.
- Design a bounded alternative-site/terrain-fitting approach that preserves rare
  village spacing, native palettes, containers and arrival protection.
- Extend mine layout scale and structure distribution only after real footprint,
  underground-fluid and loaded-boundary regression tests. Keep no-rails policy.
- Do not mark this bug fixed, reset saves, re-enable weather, or lower rarity
  blindly. Current build still needs these generation fixes.

Diagnostic tool: code branch `tools/audit_settlement_candidates.py`, with three
candidate reproduction/spacing tests. It writes reports to stdout only and reads
no accounts, player records or inventories.

## Same-seed reproduction and bounded repair

A fresh isolated ordinary server with the owner's exact seed reproduced both
rejections. The actual worldgen path reported dry solid terrain, but candidate
`(27,22)` had a -53 height delta and `(25,66)` had -5 at the first sampled corner.
The first is an appropriate cliff rejection; the second is a gentle slope
rejected by the previous four-block bound. Temporary tracing is removed.

A controlled gentle-slope gameplay regression failed before the repair. The
repair allows up to six blocks of smooth grading, while rejecting any adjacent
column step above four blocks. Container/gate preflight now covers all six blocks
of foundation depth and eleven blocks of clearance. Foundations extend seven
layers, so accepted low columns do not float. Region spacing, candidate RNG,
native palettes, water rejection and arrival protection are unchanged.

All eight required `zerog_planet_generation` gameplay checks passed in
`run-local-village-grade-green-20261013`, including the new gentle slope and
deep-controller checks, original ravine/obstruction checks and existing mines.
Natural same-seed verification passed: the previously empty candidate `(25,66)`
now produces an anchor at `(408,67,1064)`, recording six residents and two
specialists, with 60 Moon farmland blocks and six Hoarwood door block halves in
the inspected 25 FULL chunks. No manual placement, showcase hub or demo-colony
fixture was used. The read-only `--require-settlement` check now passes on this
fresh disposable world. This does not fix the correctly rejected cliff site,
certify village density on all planets, or retrofit existing chunks.

## Expanded bounded mines

The new mine-size regression first failed on the original thirty-block spine.
Mine plans now use a44-block spine and4–6 staggered workings of15/20 blocks:
104–164 combined corridor length, with intersections meaning this is not unique
walkable distance. The immediate-neighbour feature write envelope is checked for
128 seeds. No rails are added. Existing dry floor/roof, fluid/container, inhabited
chunk and gate checks remain, and arrival protection covers the larger footprint.

All nine required generation gameplay checks pass in
`run-local-expanded-mine-green-20261013`, including actual timber/chest placement,
protected rejection, and the previous village slope/ravine regressions. This is
an expanded bounded feature, not an unlimited multi-chunk mine network. Natural
mine frequency and broader ruin distribution remain separate follow-ups. The
one-in-eighteen attempt rate has not been increased blindly.

Both isolated ordinary servers and test servers stopped normally. Forced chunks
added for this work were removed. The same-version normal production build must
exclude test classes/presets before installation. Existing player chunks remain
unchanged; review these changes in new terrain or a separate future test world.

## Local delivery checkpoint

- Code commit on `1.21.x`: `0d3cdc6e` (seven files: settlement/mine runtime,
  gameplay regressions, candidate audit/tests, source contract and AGENTS notes).
- Normal same-version `1.0.12-dev` build passed; candidate SHA256:
  `aeca7d74a457200b3c37e32c0fb7ca428117d2963c087b03ae6402b5337ba493`.
- JAR checked for both runtime classes and absence of gameplay test classes and
  equipment fixtures. Nine gameplay tests and eleven local Python checks pass;
  one Python check belongs to the preserved opt-in, unactivated terrain work.
- Candidate is built locally, not installed or published yet. Preserve the
  owner's deferred combined-install workflow and closed-client requirement.
- Unactivated terrain compiler/test edits and unrelated local survey files remain
  unstaged. No new art was required; Design branch has no change for this repair.
