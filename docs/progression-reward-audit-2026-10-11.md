# Survival reward and story-route audit — 11 October

## Evidence and scope

Read-only shipped-source audit of runtime `c128a2dd`, plus the approved Design document's wasteland rewards, gear ladder and Acts III–V. The audit now uses the repository's existing standard-library NBT reader instead of requiring an unavailable `nbtlib` installation. Its legacy `--nbt-library` argument remains accepted but is no longer necessary.

[Machine-readable provenance](reports/progression-sources-20261011.json) lists 22 key/template items, their defined loot tables, authored chest bindings and Java chest call sites. This is not a natural-generation or successful survival-journey test. Duplication recipes are not a first-acquisition source, and entity loot files do not register a boss.

## Confirmed later-tier acquisition blockers

| Intended source | Templates dependent on it | Current boundary |
| --- | --- | --- |
| Collapsed Forge | Ruskite, Pyrium, Tectium, Skarnite | No authored chest binding; Skarnite's alternate Rift Tyrant loot is not a live registered boss. |
| Derelict Wreck | Salvium, Palladine, Wraithsteel, Eidolite | No authored chest binding; Eidolite's alternate Eidolon Captain loot is not a live registered boss. |
| Solar Shrine | Photium, Radiantine, Astrium, Solvanite | No authored chest binding; Solvanite's Dying Star/Sun Colossus alternatives are not live registered entities. |

These twelve templates have loot definitions, not verified obtainable routes. No fallback recipes, unrelated chest rewards or creative supplies were added to hide the missing content.

Earlier routes remain separate: Mars Crash Site templates have authored bindings; Concord Vault uncommon loot carries Cobaltium/Cyrrium/Aurelion; Prism Spire has an implemented structure route. Their earlier tests and bounded natural-placement evidence are retained, not rerun here. Chest chances and a full survival journey still require gameplay checks.

## Story implementation versus story data

- Prism Sentinel is registered. Galaxy 3 key loot is defined; keep the existing four Concord Vault key/lock sequence and approved gates unchanged.
- Rift Tyrant, Eidolon Captain and Dying Star have eggs/loot data but no matching `EntityInit` registrations in the reviewed code.
- `codex/captain` triggers on obtaining `galaxy_5_gate_key`; `codex/heart_of_solvane` triggers on obtaining the Heart item. These milestones and unlocked text are not the Captain's final-log peaceful encounter or the per-player Rekindle/Fade ending mechanic.
- The six missing wasteland ruins have approved habitat/reward purposes in the Design document. This review found no dedicated authored layouts for them. Existing Concord Vault rooms must not silently be presented as the missing surface/water ruins.
- Do not make Broken Consoles common mob drops or invent final logs, hidden-planet coordinates, encounter balance or research rules. The owner-approved small Moon impact-wreck plan remains deferred.

## Implementation order

1. Complete approved geometry/placement specifications for Collapsed Forge, Derelict Wreck and Solar Shrine, keeping original textures and lore rewards. Then verify ordinary natural starts, accessible chests and first-acquisition loot.
2. Build the missing boss encounters from verified entity/arena specifications; test combat, reload, rewards and the Captain's alternative route separately.
3. Implement the Heart choice with explicit per-player persistence and approved outcomes; test both paths without changing the approved gate flow.
4. Finish the other dedicated wasteland ruins and signature mobs, then test additional biome/seed coverage and the complete survival ladder.

No runtime game behavior, installed JAR, player saves, hub, weather or approved gates changed in this batch. Audit-tool tests and a successful Gradle build are not gameplay or client approval.

Verification: both audit regression tests passed (41.874 seconds), comparing every reported template binding with the independent jigsaw reader and checking legacy command compatibility. Gradle `build --offline` passed in 11 seconds, transcript `20261011_015211_build.log`. Tool repair published on `1.21.x` as `147bbcd0`; production Java/resources and the installed JAR are unchanged. No Design assets were modified.
