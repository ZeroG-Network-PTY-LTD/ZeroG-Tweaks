# Independent processor upgrade cards

Candidate version stays **1.0.12-dev**, Minecraft Java 1.21.1 / NeoForge.
This vertical slice covers Alloy Forge, Ore Refinery, Crystal Growth Chamber and
Salvage Station. It does not invent compatibility for generators, genetics or
legacy addon machines with no card sockets.

## Approved limits

| Tier | Acceleration default | Energy Coil total job saving | Compact capacity approved, not implemented |
| --- | --- | --- | --- |
| 1 | 1.25x | 5% | 212 |
| 2 | 1.50x | 10% | 360 |
| 3 | 1.75x | 15% | 508 |
| 4 | 2.00x | 20% | 656 |
| 5 | 2.25x | 25% | 804 |
| 6 | 2.50x | 30% | 952 |

There is one installed card per family, not additive stacks of cards. Server
configuration `zerog-machine-upgrades-server.toml` may reduce the per-tier effects
but cannot exceed the approved caps. Acceleration shortens the duration without
discounting total energy; a faster job therefore draws more FE per tick. Energy
Coil discounts **total job FE**, not generated energy or storage capacity.
Integer durations/costs round upward; every job still costs at least one FE.

Example: the 8,000 FE / 200 tick Cyrrium casing job becomes **5,600 FE / 80 ticks**
with both tier-six cards. Its ingredients and two-casing output remain unchanged.
The refinery cards do not secretly grant a yield multiplier.

## Installation and recovery

The first physical upgrade socket accepts Acceleration cards; the third accepts
Energy Coil cards. The middle socket is **legacy take-out recovery**, not a working
Compact socket. New casing, dust and cooling-core insertion is rejected. The
Items/Recipes/Upgrades panel and hover tips explain supported cards and limits.
The main screen receives the precise speed percentage, including reduced server
settings, rather than displaying only quarter-speed steps.

Existing saved upgrade ingredients remain recoverable. Until a card is installed,
their original bounded effects remain. Installing either new family disables **all**
legacy bonuses, including the old refinery casing yield bonus; no compound legacy
plus-card discount. Removing the card restores retained legacy effects. Nothing
automatically consumes old casings or converts them to free cards.

Changing upgrade/configuration state resets the current job, as before. Energy
already spent is not refunded; this conservative rule prevents upgrade switching
from granting unpaid outputs. A save/reload of an unchanged card job preserves
its progress and paid FE. Blocked outputs do not spend power.

## Artwork and deferred features

The twelve functional cards reuse the existing original `item_filter_card` icon;
their inventory names identify family and tier. This is **not** a new approved
unique card-art rollout. Dedicated artwork is paused because the required asset
production CLI is unavailable; no paid provider or substitute images were used.

Compact storage, selective Void filters and additional machine compatibility
remain outstanding. Do not raise ItemStack counts above vanilla packet limits.
Compact needs separate bulk storage, legal extraction, saved counts and conserved
break drops. Its approved capacities are requirements, not shipped behaviour.
Survival crafting remains deferred until exact storyline costs are agreed; cards
are currently available through the Storage & Transport creative category.

## Verification and contributor reconciliation

The initial upgrade regression failed because the cards were unregistered
(`20261006_224518_runWorkflowTests.log`). After implementation that test passed;
the reconciled suite exposed a superseded all-flat-armour expectation. The test
now independently requires exactly the four approved Sol shell sets and sixteen
vanilla-fit sets, retaining material and slot assertions for all eighty pieces.

[Contributor reconciliation](contributor-reconciliation-2026-10-07.md) identifies
the fourteen pulled code commits and the Sol tracker's new lore tasks. Successful
server checks are not client visual approval of those models or the recipe GUI.
The delivery receipt records the final test count, asset audit, installed hash and
recoverable old-JAR backup after verification. Hub and planets are left untouched.

Final isolated run `20261006_230110_runWorkflowTests.log`: **all82 required tests
passed**. The card-specific boundaries cover both family filters and rejection of
second cards, all six tier defaults in all four native processor menus/catalogues,
exact tier-six processing FE/output, blocked-output conservation, recoverable old
items, disabled mixed legacy bonuses and paid save/reload. A test-fixture reload
initially lacked its level attachment; it was corrected before this final pass.
No client visual/gameplay approval is claimed from the isolated run.
