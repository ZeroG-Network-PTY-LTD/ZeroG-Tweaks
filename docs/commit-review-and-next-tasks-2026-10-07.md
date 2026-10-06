# Commit review and next tasks — 7 October 2026

Minecraft Java 1.21.1 / NeoForge, unchanged candidate **1.0.12-dev**.

Live GitHub branch heads were fetched and checked directly. No newer remote
commits were found beyond the last delivery. Stale local remote references were
not used as evidence; no branches or tags were deleted or force-pushed.

| Branch | Reviewed head | Latest delivery |
| --- | --- | --- |
| 1.21.x | `9a58cea2` | Supplied machine workshop and safe copied-hub export |
| Design | `d37440fb` | Retained refining generator and blocker-repair reconciliation |
| Docs | `b2475cdd` | Workshop guide, installation receipts and archived same-version JAR |

## Completed implementation, with limited verification

- **Supplied workshop:** 13 machine stations and alveary supplies in a copy of the
  existing ServicePorts hub, using real recipe materials, valid bee cages/catalysts,
  fuel and configured power. Five isolated checks passed (`20261006_171606`).
  Original save hashes were unchanged. Rebuilding preserves player edits and stock.
  Unattended distant ticking and actual client inspection remain unverified.
- **Processing side controls:** `ea1ce7df` adds independent recipe-filtered item
  faces to refinery, alloy forge, crystal growth chamber and salvage station.
  Power faces were added in `9b3b2c56`. The 79-check run (`20261006_163644`) covered
  all faces, saved settings, rejected invalid commands and actual hopper access.
  This does not complete side controls for generators, genetics or legacy machines.
- **Honey alongside combs:** `9b3b2c56` adds 250 mB per completed T3+ cycle,
  planetary honey with Moon fallback, tank blocking and physical honey-port access.
  The 77-check run (`20261006_162309`) used an actual Productive Bees iron bee.
  Production with every native orbital species and in every planet remains unverified.
- Previous refinery, mining, mixed-tier fluid safety, jelly bucket, genetics,
  hive discovery and controller-routing repairs retain their ledger evidence.
  They are not reclassified as new work or newly tested by this documentation audit.

## Outstanding work, in priority order

1. **Inspect the supplied hub in the client:** machine inputs/outputs, power,
   controller GUI readability, worn armour, inventory art and transport appearance.
   Server tests and concept sheets do not replace this approval.
2. **Finish remaining side controls:** generators, genetics and legacy machines;
   supported fluid faces, saved roles, server validation and automation boundaries.
3. **Finish upgrade contracts:** catalogue compatible upgrades and bounded effects
   for remaining legacy machines; preserve item/fluid/energy conservation.
4. **Transport:** test existing transient movement under successful and blocked
   transfers; implement committed-transfer energy pulses and directional fluid waves.
   Gas IDs, units, storage and limits need specification before gas networks.
5. **Alveary:** map Concord Codex advancements to approved trait unlocks/caps;
   verify climate, lifespan, territory and module rules against supported APIs.
   Seven-wide layouts still need approved geometry and formation implementation.
6. **Recipe discovery and progression:** in-game guide or optional JEI/EMI support;
   reconcile Design trackers with runtime for guardian keys, templates, structure
   loot, signature mobs, later chapters, professions, perks and seeded catalogues.
7. **Broad planetary ecology:** generated terrain samples covering appropriate
   trees, cave vegetation, liquids, settlements, ores, structures and natural mobs;
   small isolated samples are insufficient.
8. **Survival crafting last:** after workshop inspection, agree exact ingredients,
   quantities and unlocks from hardest to easiest along the Concord story. Bee
   machines, multiblock parts, frames, consumables and jelly synthesis remain paused.

Also retained: dedicated jelly/port artwork review, holographic diagnostics,
solar-plasma/cooling quantities, claim/team adapters and unfinished boss mechanics.
No unsupported gameplay values or APIs are invented to mark these complete.

This update changes documentation only. It does not rebuild or replace the installed
JAR, change version, launch Minecraft, regenerate dimensions or modify saves.
The [TODO ledger](storage-and-machinery-todo.json) retains individual acceptance
criteria and distinguishes implementation, server verification and client approval.
