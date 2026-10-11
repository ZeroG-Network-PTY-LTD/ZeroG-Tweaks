# Frozen and barren wildlife — implementation receipt

This same-version batch wires three previously illustrated but unregistered creatures into gameplay. Existing approved geometry, textures, animations, spawn eggs and death loot are retained; no new appearance is claimed approved.

## Rime Stalker

- 24 health, 5 attack damage, 0.8 × 1.0 block hitbox.
- Glaciers, Ice Spike Forest and Frozen Canyons: configured spawn weight 50, groups 1–2.
- Approaches behind a watched target, then attacks. A successful bite adds 100 frozen ticks; the creature itself cannot freeze.
- Existing walk, attack and eye-blink animation bindings are used.
- Snowstorm concealment remains pending. Custom weather stays disabled.

## Crater Drifter

- Neutral floating scavenger: 20 health, 4 attack damage, 0.8 × 1.4 block hitbox.
- Cratered Plains, Dust Badlands and Canyon Scars: configured spawn weight 50, groups 1–3.
- Does not acquire nearby players as attack targets; retaliates when hurt. Uses vanilla-style timed neutral anger.
- Wanders above loaded terrain without gravity. Produces one Meteorite Fragment every 6,000 ticking server ticks, preserving the countdown through save/reload.
- No Broken Console drops, explosions or automatic terrain damage.

## Ash Strider

- Neutral lava mount: 30 health, 6 attack damage, 1.0 × 1.9 block hitbox; fire immunity and vanilla lava buoyancy.
- Basalt Fields, Ash Plains and Lava Lakes: configured weight 50, groups 1–3, lava placement.
- Cinder Caps are its breeding food; offspring retain the custom species. Vanilla saddle/mount/steering interactions are inherited. No piglin or vanilla Strider jockeys are generated.
- Vanilla Warped Fungus on a Stick is the current steering tool; dedicated cinder steering and bespoke stomp animation remain pending. Existing attack animation is used.

## Codex

Two generated pages explain Water Separator connections, safe gas handling and these creatures. Hydrogen/oxygen are fluid identities, not invented inventory items. Page illustration references use registered items only.

## Verification boundaries

The initial isolated server run passed all 19 required tests. The combined run `20261011_143827_runWorkflowTests.log` passed all 21 required tests: real Rime Stalker egg interaction, frozen bite, Drifter neutral/gravity state, fragment timer/reload, Ash Strider saddle/mount/food/offspring/reload, exact loaded biome lists, Codex parsing and existing gate/gas/transport regressions. Clean production build `20261011_144023_clean.log` passed. Asset audit checked 8,023 models, 1,530 blockstates, 4,005 PNGs and 130 animation metadata files with zero errors.

Final same-version JAR SHA256: `56e7f123279b9f9ca8da1ca94ac269a2bd776caeeb0cfb6bb1ab11e284f44270`. See [asset audit](reports/wasteland-signatures-assets-20261011.json), [installation receipt](reports/wasteland-signatures-install-20261011.json) and [archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-wasteland-signatures-20261011.jar). Installation preserves dependencies and backs up the old ZeroG JAR outside the mods folder.

Configured biome eligibility is not proof of natural spawn density. Render quality, stalking presentation, long flight paths and client GUI layout still need in-game review. No existing save, hub, weather configuration or material costs were changed.

## Current pending work

1. Bog Lurker gameplay using its existing approved design specifications; Ash Strider bespoke stomp and steering artwork.
2. Broader natural ecology sampling across seeds and later galaxies; actual mob populations and flight paths.
3. Advanced bee biology and research milestone mapping; larger alveary layouts require authoritative rules.
4. Remaining machine catalogue/upgrade contracts, client layout and transport visual approval.
5. Dedicated gas art, remaining localization and holographic diagnostics.
6. Exact story-aligned survival costs, last. Moon wrecks remain pending without Broken Console mob drops.
