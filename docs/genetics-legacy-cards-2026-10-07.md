# Genetics and legacy processing cards

Minecraft 1.21.1 / NeoForge, same **1.0.12-dev**. This batch extends the existing original ZeroG cards; it does not add a dependency or change recipes, artwork, the hub or saves.

## Supported machines

Geno Station, Genetic Splicer, Centrifuge and Starmetal Smelter each receive two independent sockets: **A — Acceleration** and **E — Energy Coil**, tiers 1–6, one card per family. They sit to the right of the player inventory. Existing operating, recovery and player slot indices remain unchanged. Specimens, serums, jelly and smelting flux remain recipe inputs, not upgrades. Compact and Void are deliberately unsupported on these four machines until their storage/output contracts are approved.

The existing server configuration applies: default +25% speed and 5% total-job energy saving per card tier, bounded at **2.5× speed / 30% FE saving**. Speed concentrates the remaining job energy over fewer work ticks; it is not free throughput. Insufficient power and blocked output slots pause without consuming ingredients or FE. Geno Station retains its original quarter-speed unpowered mode, which cards do not accelerate. Card effects do not modify bee traits or the 75% Royal / 100% Cosmic Jelly splicing chance.

| Job | No cards: work ticks / total FE | Tier-6 A + E: work ticks / total FE |
| --- | --- | --- |
| Geno analysis | 100 / 2,000 | 40 / 1,400 |
| Geno sampling | 300 / 6,000 | 120 / 4,200 |
| Genetic splicing | 400 / 24,000 | 160 / 16,800 |
| Centrifuge | 201 / 4,020 | 81 / 2,814 |
| Starmetal Smelter | 201 / 16,080 | 81 / 11,256 |

Numbers assume default settings and continuous power. The addon's actual legacy job includes 200 progress increments plus a completion call. Those original recipe functions remain authoritative; no replacement recipe table, output quantities or yield bonuses were introduced. Integer cumulative charging rounds conservatively across the complete job.

## Recovery and automation

- Cards have separate saved storage, with filtered menu sockets and shift-click insertion/removal.
- Unchanged paid jobs resume on reload. Card/config/input changes invalidate progress conservatively without destroying recipe inputs or refunding already-used energy.
- An in-flight genetics job saved by the previous build may cancel once when its fingerprint is upgraded; restart it in the menu. Its inputs remain intact.
- Taking existing Centrifuge outputs does not invalidate its input fingerprint.
- Breaking an affected machine refunds its stored cards once, alongside existing inventory recovery.
- Unsupported Compact/Void cards cannot enter these sockets. Upgrade sockets are managed through the menu, not incidental input/output pipe slots.

## Verification and remaining review

Regressions exercise real placed block entities, menus, original addon dispatch, Productive Bees cage traits, output backpressure, exact FE, interruption, reload and drop recovery. The focused tests first reproduced inert cards before the processing implementation. A combined test-fixture duplication was repaired in the opt-in build configuration; test classes are excluded from normal builds.

Final build, asset audit, installation and successful server evidence are recorded in [the delivery receipt](genetics-legacy-cards-delivery-2026-10-07.json). This is not client visual approval. Verify socket visibility, shift-click and progress displays in the supplied workshop; current original filter-card icons are temporary, not new dedicated card artwork.

Final combined run `20261007_020802_runWorkflowTests.log`: **118 required tests passed**, including real block destruction returning the stored card exactly once. Optional-absence run `20261007_020620_runGeneticsTests.log`: **2 required tests passed** without Productive Bees or the orbital addon. The test-first failing processing cases are retained in local logs `20261007_015010_runWorkflowTests.log` and `20261007_020252_runWorkflowTests.log`; failed fixture setup launches are not passing evidence.

Clean production build: `20261007_020945_clean.log`. Asset binding audit: zero errors across 7,977 models, 1,528 blockstates, 3,943 PNGs and 120 animation metadata files. Installed with a backup before publication; SHA256 `0a23b7be2a217045ca9757724c174501bc7472404ded1cc9a7c4c3350a56bce1`. [Archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-genetics-legacy-cards-20261007.jar). Earlier JAR archives and all 37 checksums are preserved.

Still pending: other machine-specific upgrade contracts; Compact/Void rules for these machines; broader recipe/combination adapters; advanced alveary biology/research and seven-wide layouts; ecology/progression audit; dedicated card/jelly/port artwork. Exact survival recipe costs remain deferred as requested. See [the full TODO ledger](storage-and-machinery-todo.json).
