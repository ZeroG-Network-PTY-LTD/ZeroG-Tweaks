# Progression repair source notes — 7 October 2026

This directory contains design-owned generator updates, not game code.

Run `apply_vault_template_fallback.py` against the code checkout's
`src/main/resources` after older full-data generators. It adds the approved
temporary Cobaltium/Cyrrium/Aurelion first-template source to uncommon Concord
Vault loot. It does not rename items, change template duplication costs, guarantee
a roll or create the unfinished Prism Spire.

The corresponding GuideME generator is `../codex-guide-v1/write_guide.py`.
ItsT2 page describes ordinary galaxy-tier moon access and the temporary chest
source. Authoritative runtime remains on1.21.x; tests distinguish authored chest
bindings from actual natural-generation proof.

## Tracker reconciliation

The original galaxy trackers are historical audit snapshots and are preserved.
This repair closes the documentedT6-only moon restriction in ordinary formed
gates. Glacial Ice's approved0.98 friction and glass sound are implemented without
changing strength. Vent Rock's cosmetic smoke is implemented but requires client
appearance approval. Acid resistance, missing signature mobs, missing ruins,
seven-wide alvearies and advanced bee research remain separate tasks.

The owner deferred the bee-trait/Codex milestone mapping on7October. Do not invent
that map. The three Vault fallback templates use the tracker's explicit temporary
fallback option; natural encounter testing and higher-galaxy first-template
acquisition remain unfinished.

The7October checkpoint was installed once at the owner's10% usage threshold,
after a clean production build, zero-error asset audit and26 required checks.
See Docs `usage-window-workflow-2026-10-07.md` and
`usage-window-delivery-2026-10-07.json` for the installed checksum and remaining
boundaries. Models/generators being present alone never prove local installation.
