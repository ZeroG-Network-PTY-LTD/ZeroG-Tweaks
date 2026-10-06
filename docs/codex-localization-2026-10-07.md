# Concord Codex localization — 7 October2026

Same Minecraft Java1.21.1 / NeoForge development version: **1.0.12-dev**.

## Implemented and tested

Moon Relay and Mars Waystation page bodies moved from hardcoded components to
`codex.zerog_tweaks.moon_relay` and `codex.zerog_tweaks.mars_waystation` in
`assets/zerog_tweaks/lang/en_us.json`. The approved English text is unchanged.
No IDs, recipe costs, lore events or arrival flags were renamed.

Actual Codex item interaction in disposable, loaded Moon/Mars server levels verifies:

- Before visiting either planet: three Prologue pages only.
- Visiting Mars first: its translated page only; no Moon page.
- Visiting Moon afterward: both Act I pages, in the original display order.
- Returning to the Overworld: both pages remain unlocked.
- Saving and reloading the player: both arrival unlocks persist.

The regression first failed at the missing Mars language key in
`20261006_234543_runWorkflowTests.log`, then both required lore tests passed in
`20261006_234711_runWorkflowTests.log`. The second test covers the shrine in all
four Rustborn layouts. Earlier setup failures are not counted as gameplay evidence.

The opt-in `workflowPlanetPreset` loads real Moon/Mars definitions beside a plain
test Overworld. It avoids duplicate hub fixtures and does not construct a hub.
This resource source is excluded from normal production builds. Tests use a mock
server player at the connection boundary and real level contexts/item use; they do
not certify physical gate travel, client book layout or optional Productive Bees
login payloads. No player save or terrain is modified by these isolated tests.

## Next approved storage slice

Compact tiers target total input capacities212/360/508/656/804/952. Use separate
bounded storage, never oversized network ItemStacks. Verify actual menu and pipe
transfers, processing, card removal, save/reload and block breaking. Stored inputs
must remain recoverable after removing or downgrading a card.

Then add an installed-Void-card-only scrollable ghost filter. Validate and persist
commands on the server; discard only selected machine products, never player
items, inputs, catalysts or fluids. Nonmatching full outputs must still pause.
The owner approved these test boundaries; implementation is not claimed complete.

All other queued controls, visuals, biology, progression and ecology remain in the
[live TODO ledger](storage-and-machinery-todo.json). Remaining recipe adapters,
small Moon impact wrecks and exact survival costs remain deferred. No Broken
Console mob loot, gases, later-act text or unapproved biology rules are invented.
