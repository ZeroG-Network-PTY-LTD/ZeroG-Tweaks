# Village terrain selection and natural footprint

This follows the confirmed `1_21_1 alpha` generation report. Player saves and the
installed JAR remain unchanged while this batch is verified locally.

## Reproduced issues

The original one-candidate selection discarded its attempt when terrain was bad.
A deterministic alternative selector now considers up to five positions, all
inside the original16..33 chunk offsets of each50x50-chunk region. Exactly one
site is selected from immutable base terrain, independent of chunk-generation
order. It retains a suitable original site, tries alternatives otherwise, and
retains the guarded original attempt if no predicted site is suitable. Full final
fluid, grading, cliff and protected-block checks are still authoritative.

The first ordinary-server check exposed a second issue: suitable terrain was
still rejected because the builder checked and flattened an entire square lawn.
An unused edge fluid pocket blocked the selected Moon site, and a protected block
outside the used layout blocked Cerulon's. Both actual rejection traces were
captured in a disposable seed-zero server; temporary debug logging is removed.

The builder now protects/checks/grades only the actual homes, paths, farms,
Mars shrine and garden. Unused edge ponds, natural terrain and block entities
remain intact. Every written column still has a protected preflight, dry solid
ground, at most six blocks of grading and no neighbouring used-column step over
four blocks. A ravine beneath farmland remains a rejection, not an accepted fill.

## Verification so far

- Alternative-selection gameplay regression failed before the selector change.
- Unused pond/beehive gameplay regression failed before the footprint change.
- All12 required `zerog_planet_generation` checks now pass, including both fixes,
  critical-column ravines, deep buried controllers, foundations and expanded mines.
  The blocked-home regression first failed, then passed after adding at most four
  existing-layout attempts at the same selected site. Failed preflight attempts
  write nothing; the first successful layout stops further attempts.
- The dedicated native selector check passed with real native planet generators,
  repeated choices and unchanged loaded-chunk counts.12 sites across the six fixed named
  planets took787ms for two evaluations each in that test; this is not a client
  performance guarantee or a frequency estimate.
- Four Python candidate/spacing/pool tests pass. Existing source contracts pass
  locally; the unactivated experimental terrain changes are preserved separately.
- Both the sparse-footprint-only and final layout-retry ordinary rechecks found
  no settlement at the selected seed-zero Moon(22,18)/Cerulon(31,16) sites,
  each with25 saved FULL chunks. Broader natural placement remains unresolved;
  selection proof is not counted as actual village/population evidence. Temporary
  force-load tickets were removed and the disposable server stopped normally.
- The normal same-version build passes. This candidate is not installed yet.

For offline saved-world inspection use `--search-alternatives` with
`tools/audit_settlement_candidates.py`. This enumerates possible sites; it cannot
reproduce runtime noise selection. No observed village in alternative mode is
labelled inconclusive, rather than falsely asserting the chosen site failed.

## Moon ruins

No current natural ruin biome tags include Moon biomes. That explains why visiting
Moon cannot show those later-world ruins; increasing their chance would not fix
the binding, and moving their rewards there could break progression.

Owner requested a lunar survey-outpost draft for approval. It is saved only on
Design at `docs/lunar-survey-outpost-draft-2026-10-13.md`: three proposed small
layouts, existing Moon materials, ordinary loot only. No new structure registry,
loot table or natural spawning has been activated. Later-story keys/templates,
Wisp/Codex/Console loot and the separate Maw impact-wreck plan remain untouched.

## Still pending

- Physical village coverage across more seeds, regions and planets.
- Ruin/mine frequency and walking-distance surveys, not only `/place` success.
- Moon-outpost layout/loot/settings approval and later editable schematic images.
- Actual player/simulation-boundary natural mob-density checks.
- Existing client GUI/art approval and unspecified biology/research/crafting costs.
