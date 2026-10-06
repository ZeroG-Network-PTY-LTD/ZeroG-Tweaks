# Processing machine item faces

Minecraft Java **1.21.1 / NeoForge**, same-version **1.0.12-dev** extension.
Applies to Ore Refinery, Alloy Forge, Crystal Growth Chamber and Salvage Station.

## Using the panel

Open a processing terminal and select **Show items** beside the slots. The existing
six-world-face matrix switches from power controls to item routing. Click a face
to cycle **Auto → Input → Catalyst → Output → Off → Auto**. Select **Show power**
to return to FE settings. Item and power choices are independent.

| Item mode | Automation access |
| --- | --- |
| Auto (violet) | Original layout: top/side reagents, back catalyst, front/bottom products |
| Input (red) | Recipe-filtered reagent slots; insertion only |
| Catalyst (cyan) | Recipe-filtered catalyst slot; insertion only |
| Output (green) | Product slots; extraction only |
| Off (grey) | No item slots or transfers on this face |

These are world directions: Down, Up, North, South, West and East. Auto uses the
machine's facing for its original front/back roles. Explicit roles let you route
items from any face. No role exposes upgrades or bypasses the recipe filters.
Machines without an applicable catalyst reject catalyst items rather than treating
the slot as a generic inventory. Manual inventory recovery remains possible.

## Safety and persistence

Faces synchronize through the real processing menu. The server validates the
button range, player distance and machine identity. Changing a role invalidates
capabilities and permanently revokes handlers created before the change, even if
the face later returns to the previous role. Old handlers cannot gain access to
different slots. Simulated extraction does not consume products.

Saved item modes use a separate NBT field. Missing/invalid entries default to Auto,
preserving existing worlds and the prior FE switches. Changing item mode does not
change power, recipes, processing costs, inventories or existing registry IDs.

## Verification limits and remaining work

Server regression evidence covers all six faces on all four machines, real recipe
input/catalyst filters, output conservation, simulated transfers, saved Output
roles, remote/forged commands and stale-handler revocation. A separate disposable
world check uses an actual vanilla hopper feeding the refinery and then verifies
that Off stops it without losing items. Client sizing/colour/readability approval
remains a player check, not something established by compilation.

These four processing machines have no fluid tanks: there is no decorative fluid
control. Remaining generator/genetics/legacy machine side modes, directional energy
pulses and fluid waves, defined gas types/units, advanced alveary research/biology,
progression and ecology remain pending. Survival recipes remain last, awaiting exact
user costs. No textures or player saves are changed, and no Design/Released commit
is needed for this code/UI extension.

## Delivery

All **79 required isolated server tests passed**. The clean production build passed,
contains no GameTest classes/fixtures and has zero runtime asset-binding errors.
The client was closed for replacement. The installed predecessor was backed up to
`ZeroG/zerog-mod-backups/20261006-164409-UTC`; other mods and all saves are preserved.
Installation preceded GitHub publication. [The delivery receipt](item-faces-delivery-2026-10-06.json)
records the exact candidate SHA256, archive, code commit and test/build logs.
