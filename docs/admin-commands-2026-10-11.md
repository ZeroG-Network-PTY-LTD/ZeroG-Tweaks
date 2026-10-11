# ZeroG administrator commands

Minecraft Java 1.21.1 / NeoForge; operator permission level 2 or higher. These are administrative inspection tools, not survival gate recipes. `/zero help` lists them in game. Existing `/zerog` commands remain available.

## Travel

| Command | Purpose |
| --- | --- |
| `/zero dimensions` | List every fixed destination alias and full dimension ID. |
| `/zero tp moon` | Travel near the Moon's spawn, searching for clear dry footing. |
| `/zero tp mars` | Equivalent Mars shortcut. |
| `/zero tp <planet> x y z` | Travel to explicit coordinates. Ordinary players cannot arrive inside solid blocks; spectator inspection can. |
| `/zero home` | Return near the Overworld's world spawn—not your bed or the hub specifically. |

Fixed aliases: `overworld`, `moon`, `mars`, `cerulon`, `skarn`, `eidolon`, `solvane`; for each galaxy 2–5, `g2_p1` through `g2_p6` and `g2_moons` (replace 2 with 3, 4 or 5). That is 35 destinations including the Overworld. Unloaded/unavailable dimensions are reported rather than created.

Automatic travel checks nine bounded columns near spawn. It refuses when no suitable dry footing is found. It does not build landing pads or retain forced-chunk tickets. Explicit coordinates may be underwater, airborne or hazardous: use spectator mode for ocean ruins. Relative coordinates refer to the command source. Travel spends no gate FE and grants no keys; normal dimension-arrival Codex milestones may still unlock. Loading an ungenerated destination can take time.

## Structures and diagnostics

| Command | Purpose |
| --- | --- |
| `/zero structures` | List the 13 registered structure shortcuts. |
| `/zero locate sunken_relay g2_p1` | Run the real structure locator in the specified dimension. |
| `/zero locate sunken_lab g2_p5` | Locate a laboratory in its ocean dimension. |
| `/zero locate buried_observatory g2_p2` | Locate a desert observatory. |
| `/zero locate frozen_outpost eidolon` | Locate a cold outpost. |
| `/zero locate impact_site g2_moons` | Locate a static crater ruin, not a scheduled comet event. |
| `/zero status` | Current dimension and world time; custom weather remains paused. |
| `/zero gate x y z` | Loaded controller formation, tier, energy, port count and countdown/error. |
| `/zero machine x y z` | Read-only item-slot, fluid-tank and energy-capability summaries for all six faces. |
| `/zero hub status` | Existing hub status report. |

All structure shortcuts: `buried_observatory`, `collapsed_forge`, `concord_vault`, `derelict_wreck`, `frozen_outpost`, `impact_site`, `mars_aresite_shrine`, `mars_crash_site`, `prism_sentinel_arena`, `prism_spire`, `solar_shrine`, `sunken_lab`, `sunken_relay`. Omit the destination to search your current dimension. A registered structure is not guaranteed to generate in every dimension or near every spawn; the locator may report none found. Locate can generate/search chunks and is not instantaneous.

Machine summaries report currently exposed capabilities, not recipes or guaranteed transfer: side settings, formation and operating state still matter. Gate/machine diagnostics require an already loaded block.

## Existing tools and safety

`/zerog hub workshop` and `/zerog hub exhibits` place showcase blocks: use only in a designated test hub. They are deliberately not automatic teleport side effects. `/zerog inspection 1` and `/zerog inspection 2` depend on the inspection hub records. Legacy `/zerog gate bind` is not the flexible tier-1–6 player-gate builder.

Useful vanilla tools remain `/gamemode spectator`, `/gamemode creative`, and `/locate structure zerog_tweaks:<structure>`. No dimension deletion, terrain reset, mass inventory refill or forced-chunk cleanup command was added.

## Verification and remaining work

Three required isolated server tests passed: all 35 literals and operator permissions; real explicit travel with collision/water/fire/magma checks; and an actual Moon/Overworld round trip. Transcript: `20261011_095452_runWorkflowTests.log`. The earlier two-test run also passed. Servers stopped normally. This is not visual client approval or a natural locator audit for every structure.

Normal production clean build passed (`20261011_095626_clean.log`), without test classes or fixtures. Asset audit: 8,021 models, 1,529 blockstates, 4,005 PNGs, 130 animation metadata files; zero binding errors. Three manufacturing regressions also passed. [Asset receipt](reports/admin-commands-assets-20261011.json) · [Installation/backup receipt](reports/admin-commands-install-20261011.json) · [Same-version JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-admin-commands-20261011.jar). SHA-256: `1efad66bfb7b202667964f913902ce5fb434e495467ea6c1db17e2838c446f79`.

Client transition presentation, automatic footing across all planetary terrain, and broader natural structure coverage still require review. Undefined biology/research mappings, story bosses and exact survival costs remain separate TODOs—not completed by administrator access.
