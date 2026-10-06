# Alloy Forge bugs and machine upgrade-card requirements

Reported 7 October 2026. Candidate version remains **1.0.12-dev**.
This report separates player-reported defects from requested, unimplemented features.

## AF-01 — Ingredient and catalyst insertion

**Reported:** recipe inputs are problematic and no catalyst can be placed.
The active alloying recipes require Stardust for Abyssal Pearl, Heatproof Plating,
Cryo Core and Neutralizer; those catalysts are reusable. Other alloying recipes
do not require a catalyst. The existing input catalogue is a union of accepted
items, not a recipe page with quantities and catalyst requirements.

**Confirmed input defect:** the actual menu shift-click path installed Pulsar Dust
in the efficiency socket before attempting a recipe input. Existing direct-storage
processing checks could not catch this menu-routing error. The corrected-player
red run `20261006_215533_runWorkflowTests.log` failed with “Recipe dust was diverted
to an upgrade socket”; the other 76 required tests passed. The first test attempt
had an out-of-reach mock player and is not evidence of this routing cause.

**Repair server-verified:** operating catalyst/input slots take priority over
legacy upgrades. Full operating slots must leave the item in player inventory,
not silently install it. Materials overlapping upgrade requirements can still be
installed deliberately by dragging into an upgrade socket until the card migration.

**Catalyst finding:** registered Stardust was accepted by the actual menu slot and
handler. This does not reproduce the player's catalyst rejection. Need the actual
attempted catalyst item and failing recipe/client menu to diagnose that symptom.
Do not mark the entire report fixed from one passing test.

The green run `20261006_215850_runWorkflowTests.log` passed all **77 required
workflow tests**, including actual menu ingredient/catalyst routing, full-input
preservation and existing exact-energy, reusable-catalyst and reload checks.
Client-specific catalyst rejection remains open; this does not certify every GUI.

## Installed repair checkpoint

Runtime commit `ea5d3563` changes only `ProcessingMenu.java` and its gameplay
regression. Clean production build `20261006_220131_clean.log` passed; the
asset-binding audit checked 7,937 models, 1,522 blockstates, 3,893 PNGs and 96
animation metadata files with zero errors. No test classes ship in the archived
production JAR. The verified repair was installed before publication as
`zerog-tweaks-1.21.1-1.0.12-dev.jar` with SHA256
`faa4a3fb18a4ee5d150daec83fa023d36114cceb6f731e15e181cdd5abc2f45f`.
The predecessor is recoverable in `zerog-mod-backups/20261006-220321-UTC/`.
Dependencies, hub and planetary saves are unchanged.

[Delivery receipt](alloy-menu-delivery-2026-10-07.json) ·
[Archived matching JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-alloy-menu-20261007.jar).

## UC-01 — Replace direct-material upgrades with cards

**Requested, not implemented:** dedicated machine cards; casings and materials
become crafting ingredients, rather than being installed directly as upgrades.
Preserve recoverable old installed items and registry IDs. Define compatibility
per machine; an unsupported card must be rejected, never accepted without effect.

- Acceleration cards, tiers 1–6. Bounded speed and corresponding power demand;
  percentages, stacking rules and maximum compatible tier still need approval.
- Energy Coil cards, tiers 1–6. Bounded efficiency without free-energy loops;
  define whether savings apply to total job FE, instantaneous FE/t, or both.
  Processing costs must follow approved story/material tiers, not arbitrary
  blanket energy values. Current recipes remain authoritative until balanced.
- Item Compact cards, tiers 1–6, input slots only. Clarify “64 + 148 per tier”:
  proposed interpretation is 212/360/508/656/804/952 items per slot. Do not deploy
  this interpretation before confirmation. Use safe bulk-count storage and
  synchronization; merely increasing a slot limit is not sufficient. Normal
  player extraction must produce legal stacks. Removing a card must not destroy
  overflow; retain extraction-only excess or reject removal until it fits.
- Void card. Only explicitly selected machine products may be discarded while
  the card is installed. Nonmatching blocked outputs must still pause processing.
  Never void player inventory, reserved inputs, catalysts or stored fluids.

## UC-02 — Upgrades and void-filter GUI

**Requested, not implemented:** an Upgrades tab with actual sockets, installed
effects and compatible tiers. With a Void card installed, expose a scrollable
drag/drop ghost filter: selecting an item does not consume it. Validate all edits
on the server against the currently open machine/menu. Bound filter size, reject
forged commands, persist filters and provide clear disabled/active status.
Exact item-only versus component-sensitive matching remains to be agreed.

## Required regression boundaries

1. Real menu and hopper/pipe ingredient/catalyst insertion, counts and remainders.
2. Recipe completion, blocked-output pause, reusable catalysts and exact energy.
3. Each card tier's bounds, incompatible machines and combined-card effects.
4. Bulk input insertion/extraction, reload, packets, break drops and card removal.
5. Void simulation versus execution, matching/nonmatching outputs, removal of
   the card, save/reload, remote/forged filter edits and inventory conservation.

## Delivery boundaries

No new card artwork, balancing values or survival crafting costs are approved by
this report. Exact survival costs remain deferred. Implement and test confirmed
defects first; install a backed-up, same-version verified JAR before publishing
runtime changes. Code belongs on `1.21.x`, editable card artwork on `Design`, and
this report/evidence/JAR archive on `Docs`. Preserve hub and planetary saves.
