# Connected deposits and natural settlements

This batch uses disposable Java/NeoForge worlds, not the CurseForge client's saves.
No terrain profile, weather or boss/research rule is activated by these audits.

## Actual ore deposits

`tools/audit_saved_ore_deposits.py` reads exactly the108 saved FULL Sol sample
chunks from the native survey. It groups identical ore blocks by face adjacency,
reports boundary-touching groups separately and checks complete block accounting.
31,328 observed ore blocks match the independent native runtime report exactly.

Sampled mean interior deposit sizes show the intended common-to-rare trend:

| Planet | Common / standard / precious / lore / rare examples |
| --- | --- |
| Mars | Ferrox7.50; Olympium4.92; Aresite1.00 |
| Cerulon | Cobaltium7.26; Cyrrium5.82; Aurelion4.69; Starlite2.86; Cerulite not observed |
| Skarn | Ruskite7.81; Tectium5.79; Pyrium4.55; Rift Opal2.84; Skarnite1.00 |
| Eidolon | Salvium7.97; Wraithsteel5.82; Palladine4.69; Remnant Shard2.84; Eidolite1.00 |
| Solvane | Photium7.72; Astrium5.80; Radiantine4.60; Nova Pearl2.84; Solvanite1.00 |

Fuel deposits are larger in these samples; for example Regolith's mean is15.71.
This does not identify individual feature attempts: neighbouring veins can merge,
diagonal cells separate and boundary deposits are lower bounds. Different hosts,
depths and biomes affect observed density. No absence in a small sample proves an
ore is unavailable; do not change the approved tool/story gates to inflate samples.

[Connected deposit report](reports/connected-ore-deposits-2026-10-13.json).

The same saved chunks show planet cave vines, glowing mushrooms and pointed
dripstone on Moon, Mars, Skarn and Solvane; Cerulon/Eidolon samples have local
kelp. Charwood, Hoarwood and Gildwood logs/leaves are observed in appropriate
samples. No rail blocks were found in these108 sampled chunks. These are
observations, not proof of every biome's ecology or a guarantee of tree density.
Counts agree exactly with the independently collected native runtime block report.

## Natural villages: seed0

One candidate in each Sol planet's region0 was generated normally, with structures
enabled. Four additional Mars regions were sampled.10 sites,49 FULL chunks each:
490 sampled chunks, not a global frequency survey. No village was manually placed.

- Skarn candidate chunk24,22: settlement anchor at392,47,360; actual RCON query
  found8 Ashwrights and no vanilla villagers. Saved sample has60 Skarn farmland
  blocks and6 Charwood door blocks (three two-block doors).
- Mars candidate chunk67,28: settlement anchor at1080,37,456; actual RCON query
  found8 Rustborn and no vanilla villagers. Saved sample has one Aresite core,
  60 Mars farmland blocks and6 Charwood door blocks.
- The other eight sampled candidates had no settlement anchor. Candidate selection
  is not a guarantee that terrain permits placement. This batch does not relax
  spacing or replace rejected sites with manual demonstration villages.

Saved door/farmland totals refer to the bounded sample, not an exclusive geometric
association assertion. Reports retain empty sites too.

All seed0 temporary chunk force-load tickets were removed; server exited normally
with a successful Gradle result. Existing player worlds remain untouched.

## Second seed:17

Six region0 candidate sites add294 saved FULL sample chunks. Skarn produced a
settlement at392,67,456: actual query found8 Ashwrights and no vanilla villagers;
the saved sample has60 Skarn farmland blocks and6 Charwood door blocks. The other
five sites had no settlement anchor. In total,16 sites/784 sampled chunks across
two seeds yielded three observed settlements; candidate-targeted sampling is not
an estimate of per-chunk village frequency. Moon/Cerulon/Eidolon/Solvane natural
settlement coverage remains pending.

All seed17 force-load tickets were removed and its server exited normally too.
The audit CLI now takes an explicit expected `--seed`, default0, and validates
the saved world rather than labelling every report seed0.

## Codex follow-through

Gas Separation now documents non-front FE connections, the dedicated Gases tab,
creative-only full-tank test supplies, all six exact capacities and preserved
contents. The matching Design generator is updated. Only the gas chapter was
copied from isolated staged generation, leaving unrelated guide pages untouched.
The19 combined Codex/gas/material/port tests passed; full client reading remains
distinct from successful parser and server checks.

## Addon-present machine verification

The7 required `zerog_recipe_legacy` checks passed with the installed Orbital Bees
addon and Productive Bees copied into the disposable test run. This includes the
coverage test for all11 live machine IDs: real valid-input transfers on six faces,
Off/restore and stale-handler rejection, supported power/fluid families, card
contracts and precise legacy recipe handling. It is not in-game layout approval.

An additional run using the holder name rather than the template namespace
discovered zero functions and returned Gradle success. It is explicitly excluded
from successful-test evidence. Use the configured template namespace and check
the actual discovered/pass count, not just Gradle's exit code.

The final no-addon `zerog_workflow_optional` batch passed24 required checks,
including gas chemistry/FE/full-output boundaries and cached-face controls.
This is50 total required checks across the three successful batches (19+7+24),
not counting the zero-discovery run or static source checks.

## Progression and machines

The fresh source audits resolve13 structure routes, zero missing references and
zero unbound authored chest sources for22 tracked progression items.37 machine
GUI profiles have zero source-layout errors. Two progression reader tests,
three ore source tests and eight generation source tests passed. These are not
client GUI, boss encounter, loot-roll or survival journey approval.

Old tracker boxes are reconciled in Design's
`docs/tracker-runtime-reconciliation-2026-10-13.md` without deleting old lore.
Unspecified biology/research, boss outcomes, exact costs and visual review remain
pending.

## Final delivery

One same-version1.0.12-dev build was installed after all test servers stopped and
Minecraft was confirmed closed. Clean production build and asset audits passed:
zero binding errors,88 manufacturing texture bindings and48 gas source files.
Old JAR backed up; other installed mods, player saves and weather settings retained.

Archived build: `docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-ecology-codex-20261013.jar`.
SHA256: `803e9b0912e96222437d0e5f6d8c500b19550e771c69c6212f7e0da7c0382b7d`.
This JAR updates the gas Codex chapter; measured villages/ores are existing
generation verified in disposable worlds, not a new terrain profile or save reset.
