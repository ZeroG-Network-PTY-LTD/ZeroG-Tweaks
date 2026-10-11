# Selected backlog: 1, 3, 4, 7 and 8

## Implemented: Bog Lurker

Existing approved model, textures, glowmask, animations, egg and loot now bind to a registered hostile creature. Stats: 28 HP, 5 melee damage, 1×0.7 hitbox; configured toxic-biome weight 50, groups 1–2. Minecraft entity hitboxes are square horizontally: the design's 1.4-length silhouette remains geometry, not a fabricated rectangular collision box.

Acid/poison immunity also prevents acid-block armour corrosion. The amphibious creature breathes underwater, moves at 2.5× its travel input speed in acid, and rests near its fluid surface. Acid spit is an actual collision projectile with 5 damage and Poison II for 80 ticks, bounded to 10 blocks and line of sight. Projectiles expire after 100 ticks and do not damage terrain. They reuse the original Venom Gland sprite; dedicated spit/swim artwork is still pending.

Verification: `20261011_145255_runWorkflowTests.log` passed all **23 required tests**, including a moving spit colliding with a real target, poison amplifier, immunity, range, egg resolution and loaded biome lists, plus earlier gas/gate/transport/Codex checks. Natural encounter density, complex amphibious pathfinding and client presentation are not certified by these tests.

## Drafts requiring approval: 3, 7 and 8

The owner authorized **draft for approval, do not activate**. [Review proposal on Design](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/review-proposals/selected-backlog-2026-10-11.md) contains:

- Personal Codex milestone mapping for the five available trait families; no invented native lifespan/territory/mutation alleles.
- Optional T5–T7 7×5×7 shells, exact 195-cell layout count, existing frame capacities retained, ownership and migration acceptance checks.
- A small Moon impact wreck with no Broken Console, Wisp, Codex or guardian-key rewards; proposed rarity and terrain protection remain inactive.
- Exact initial cost proposals for genetics, separator, controller/frame/jelly and tiered cards; broader shell/casing bills of materials remain separate.

No new recipes or research gates activate in this JAR. No hidden-world coordinates, boss endings or story rewards were invented. Existing manufacturing recipes are unchanged.

## Machine scope: 4

Rechecked current catalogue source: four native processing recipe families, generators, genetics mode/catalyst rules, centrifuges, Starmetal/Stardust Smelters, Silk Weaver and paired frame/infusion recipes already have discovery adapters. These facts supersede blanket historical claims that none has recipe pages; they do not certify every registered block or client layout.

Compact/Void remain supported only where implemented with component-aware reserves and selective newly-produced outputs. Genetics/legacy extension needs explicit exclusions for cages, gene samples, sera and returned containers; those exclusions are proposed, not installed. Unsupported catalogue/upgrade families must not receive fabricated outputs or generic accepted-item pages claiming to be exact recipes. New machine contracts and client approval remain TODOs.

## Delivery boundaries

Same version 1.0.12-dev. Production builds exclude workflow tests. Asset and installation receipts are under `docs/reports/`. No hub, saves, weather or third-party dependencies are changed. Old JAR backups remain recoverable outside the mods folder.

Clean production build `20261011_145518_clean.log` passed. Asset audit: 8,023 models, 1,530 blockstates, 4,005 PNGs and 130 animation metadata files; zero missing references. Same-version SHA256: `834f7d2ac4b188d786f259ae9c6c29aa0d9d4ce56d1009ff6b77ea8feece41e3`. [Installation receipt](reports/bog-lurker-install-20261011.json), [asset audit](reports/bog-lurker-assets-20261011.json), [archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-bog-lurker-20261011.jar).
