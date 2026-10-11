# Recipe browsing, diagnostics and acid habitats — 12 October 2026

Same-version 1.0.12-dev delivery; no hub/save reset and custom weather remains paused.

Installed into the CurseForge ZeroG mods folder after confirming the client was
closed. Previous JAR is recoverable in `zerog-mod-backups/20261011-233730-UTC`.
Archived build: [JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-browser-ecology-20261012.jar).
SHA256: `753bd72774559631a8304dd85df0c869afbdb2819a3001ccae872bf12db1ceb2`.
Clean build transcript20261011_233601_clean.log; asset audit zero errors,
8,023models/1,530blockstates/4,005PNGs, and zero shipped GameTest classes.

Player review: open each machine's Recipes button, browse tabs/scroll, then
Back/Escape with a carried item; the cursor must remain intact. Configure-mode
Flux Wrench right-click displays the six-face snapshot without modifying modes.
Verify acid-immersed Bog Lurkers and ocean Tidewraith presentation in game.

## Changes

- Shared scaled read-only recipe browser across workbench, genetics, processing,
  generator, combustion, alveary and Water Separator screens. Back/Escape preserve
  the live menu; hidden inventory clicks and the closing click's release are blocked.
- Separator pages use synchronized recipe amounts and card-adjusted FE/time.
  Container icons are examples rather than whole-container recipe costs.
- Configure-mode Flux Wrench clicks on supported machines show a 15-second
  read-only holographic snapshot: six actual item/fluid/power faces and energy.
  No persistent entities, chunk tickets, inventory contents or automatic refresh.
- Regular ocean Tidewraith habitat placement, configurable chance/local population
  cap; no new natural boss spawning.
- Bog Lurkers remain acid/poison immune. Idle AI seeks loaded nearby acid pools,
  rests at their surface, and permits unobstructed dim-light acid habitat spawning.
  Ordinary water and exposed daytime acid spawning remain restricted.

## Server verification

- 25 combined required tests passed: transcript20261011_232959_runWorkflowTests.log.
- Dedicated AI habitat test passed: transcript20261011_232525_runWorkflowTests.log.
- Eight addon-present recipe/Codex tests passed, including loaded page parsing:
  transcript20261011_233401_runWorkflowTests.log.
-37 machine GUI source profiles: zero errors, not a client rendering certificate.
- Ocean generator/runtime byte comparison passed.

An overlapping cleanup interrupted one launch and left partial generated output.
Resources were fully rebuilt; the final eight-test rerun passed. No failed
candidate was installed. Server tests do not establish graphical approval.

## Review still needed

Client layout/visual approval is distinct from server tests. Broader natural
encounter density and seed surveys remain pending. Dedicated separator and
swim/spit art, remaining bosses/story rules, exact survival costs, research
milestone mapping, seven-wide shells and Moon impact wrecks remain outstanding.
Existing inactive proposals have not been activated.

The structure/progression source reports cover 13 configured routes and 22
progression items without missing bindings; they do not prove a full survival
journey, boss implementation or natural generation across all seeds.
