# ZeroG: Gases — creative storage inspection

Minecraft 1.21.1 / NeoForge, same-version 1.0.12-dev update.

The **ZeroG: Gases** creative tab contains an empty gas canister, full Oxygen and
Hydrogen canisters, and both gases in each of the six existing tank tiers.
Capacity ranges from 5,000 to 5,000,000 mB. These are existing tank items carrying
saved contents, not new incompatible block IDs.

## How to check

1. Open Creative inventory and select ZeroG: Gases.
2. Hover a filled tank: confirm its tier, capacity, gas name and amount.
3. Place it: the gauge should be full. Right-click for the Gas Storage Tank screen.
4. Connect a gas tube to an output-enabled tank face and another tank's input face.
   The front-face behavior of other machines is unchanged; use the tank's own
   colour-coded side settings.
5. Pick up/break the tank, place it again, then save/reload: contents should remain.
6. Oxygen, Hydrogen and water must not mix in one tank.

The inventory shell artwork is reused. The in-world renderer already supports gas
wisps. GPU appearance, inventory chamber artwork and human visual approval remain
pending; isolated server tests do not establish visual approval.

Owner approved the displayed Oxygen/Hydrogen canister and Copper tank-face artwork
on13October. This is artwork approval, not a claim that every tier was inspected
in the running client.

No new gases, production balance, terrain regeneration or survival crafting costs
are introduced. Existing pending work remains pending.

## Verification

18 required isolated NeoForge tests passed in the owner-followup batch. New gas
checks cover the real creative catalogue, actual BlockItem placement of every
filled variant, native block-entity reload and loot drops, non-mixing with water,
5-million-mB menu quantities and a conserved 250-mB Copper gas-tube transfer.
Existing equipment/manufacturing/port checks in this batch also passed.

The initial RED check reported the missing Gases tab. A subsequent check exposed
the nested FluidTank NBT format in the tooltip reader; that reader and the test
inspection now follow the real nested format. The final batch passed.

## Delivery

Clean production build passed; asset audit reported zero errors and88 unchanged
approved manufacturing texture bindings. Installed in the ZeroG CurseForge mods
folder with the previous JAR in `zerog-mod-backups/20261013-013826-UTC`.
No existing saves, other mods or weather settings were changed.

Archived build: `docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-gas-creative-storage.jar`.
SHA256: `b10e627a60fbe1171a0618b22d9830966413970343dd6d78c3c03ad8dafaebda`.
