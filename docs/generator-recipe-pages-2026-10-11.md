# Generator recipe pages — 11 October 2026

Same-version 1.0.12-dev continuation: Combustion Generator, Solar Array and
Fusion Reactor now have Items / Recipes / Upgrades panels outside player slots.
Fuel browsing is categorized and alphabetical. Full text is available by hover
and scrolling. Panels are read-only and intercept inventory/outside-drop gestures.

## Actual machine rules

- Combustion: accepted wood, coal forms and planetary fuel items; no dust.
  One item ignites a burn. Duration, FE/t and fresh-burn FE budget share runtime
  rules. Fractional carry can add one FE between burns. Automatic push is
  1,000 FE/t shared across enabled faces, not a universal cable/pull limit.
- Fusion: Fusion Dust only. New burns use server-configured base rate/duration;
  already ignited fuel retains its saved base rate. No gas/liquid catalyst route.
- Solar: no fuel input; daylight, skylight and visible sky required. Roof/thunder
  stop output, rain reduces it, planet multipliers apply. Displayed live rate is
  limited by free buffer space in actual generation.
- All three: up to three Flux Modules, each +25% rate and +100% base buffer.
  These are not Acceleration, Energy Coil, Compact or Void cards. Solar/Fusion
  module removal cannot discard excess stored FE. Full fuel-generator buffers
  pause burns. Power faces output only; browsing does not change face settings.

The Solar/Fusion menu appends six 16-bit data fields for authoritative configured
rate, burn duration and transfer limit; original values and face indices remain.
The Concord Codex generator chapter is matched to its Design source generator.

## Verification and delivery

All three isolated generator tests passed in
`20261010_232520_runWorkflowTests.log`: 16 complete Combustion burns (coal,
planks, sticks and Emberite, each at modules 0-3), four complete Fusion burns
(modules 0-3), configured menu values, full-buffer ignition refusal, dust/wrong
fuel rejection, roofed Solar output and preserved side-control commands.
The isolated world had no orbital addon or Productive Bees installed; these are
native-generator checks, not optional-addon or all-machine certification.
An initial test-source compile used an incorrect method name; corrected before
the successful run. Clean production build passed in 46 seconds
(`20261010_232707_clean.log`). Asset audit: 7,979 models, 1,529 blockstates,
3,963 PNGs and 130 animation metadata files, zero errors; no test classes ship.
Code commit: `35b32780`.

Installed into the exact ZeroG CurseForge mods folder while the client was closed.
SHA256: `1014fb1faad7ca5f952c4d8219b57b2cc007cb3822d43d151b3626a75da87fc6`.
Previous JAR is recoverable in `ZeroG/zerog-mod-backups/20261010-232814-UTC`.
The matching JAR and checksum are archived on Docs. Other mods, saves, gates,
hub terrain and the custom-weather pause remain unchanged.
Server checks do not establish client layout approval.

## Player review

1. Open each generator and its Recipes button. Check Items, Recipes and Upgrades
   do not overlap inventory; scroll/hover long lines.
2. Choose coal, wood and a planetary fuel in Combustion; compare live burn/output.
   Confirm dust remains rejected. Fusion accepts only Fusion Dust.
3. Cover Solar with an opaque block; check output stops and no fuel slot appears.
4. Add/remove Flux Modules and check buffer/rate information updates. Keep excess
   stored energy safe when removing modules.
5. With a cursor stack held, click/drag/release over the read-only panel; it must
   neither drop nor consume the stack. Test narrow GUI scales too.

## Still pending

Alveary combination pages must explain verified live bee products, frame effects,
honey and catalyst usage rather than guessing Productive Bees outputs client-side.
Advanced biology/research mappings, exact survival costs and broader ecology
remain separate tasks. Gates/power/pipes/wrench/transitions retain owner approval.
