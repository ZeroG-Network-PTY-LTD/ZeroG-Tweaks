# Progression tracker reconciliation

Compared the historical Design Sol/Galaxy trackers with runtime `7723225c` and the latest independent structure tests. Older open counts and HTML snapshots are not a current completion ledger.

## Superseded blockers

- Cobaltium/Cyrrium/Aurelion templates: Concord Vault fallback plus authored Prism Spire routes already exist; natural Spire evidence is recorded separately.
- Ruskite/Tectium/Pyrium/Skarnite templates: Collapsed Forge has two authored layouts, real-loot regressions and one naturally generated seed-zero chest on Skarn.
- Salvium/Wraithsteel/Palladine/Eidolite templates: Derelict Wreck has two authored layouts, real-loot regressions and one naturally generated seed-zero chest on Eidolon.
- Photium/Radiantine/Astrium/Solvanite templates: Solar Shrine has two authored layouts, real-loot regressions and one naturally generated seed-zero chest on Solvane.

[Static provenance report](reports/progression-reconciliation-20261011.json) tracks 22 progression items and eight configured structures. Its reported unbound template chest sources are empty; that scope does **not** mean every planned ruin, mob or story reward is implemented. [Ordinary generation evidence](three-ruins-natural-audit-2026-10-11.md) is separate from source definitions and test placements.

## Keys: two systems, not one

The four **Concord Vault keys** are implemented: altars supply `concord_vault_key`; `ConcordLockBlock` consumes each key to construct three chamber stages and form the Concord Prism on key four. Preserve this owner-confirmed sequence.

The separate `galaxy_3_gate_key`, `galaxy_4_gate_key` and `galaxy_5_gate_key` are registered items. Source search finds no recipe or live gate-controller requirement for them. The Galaxy 5 key can satisfy a Captain journal milestone; that does not enforce gate travel. `SurvivalGateBlockEntity.canReach` uses formed tier, admin override, destination galaxy and current-dimension checks—not these boss keys.

This is a confirmed **lore/runtime gap**, not a reason to replace the approved gate system or confuse it with the working four-key Vault. Exact installation/consumption rules for boss keys should be agreed before changing survival access. No permanent player unlock, new slot or consumption rule is invented here.

## Remaining true blockers

Rift Tyrant, Eidolon Captain, Dying Star and Sun Colossus lack registered encounter implementations; art/loot alone does not constitute a fight. Captain peaceful resolution and Heart of Solvane ending mechanics remain unfinished. Missing dedicated ruins/signature species remain tracked separately.

Full survival reward acquisition, every variant/habitat, rarity across seeds, client navigation and gear/GUI appearance still require testing. Exact manufacturing/survival costs and advanced bee milestone rules remain pending. No code, JAR, hub or player save changed in this audit.
