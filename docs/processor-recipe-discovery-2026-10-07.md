# Exact processor recipes in the Items panel

Minecraft Java 1.21.1 / NeoForge; candidate remains **1.0.12-dev**.

## Supported machines

Alloy Forge (10 authored recipes), Ore Refinery (79), Crystal Growth Chamber (4)
and Salvage Station (5) now share a
read-only recipe panel backed by their **live registered recipes**, rather than
an invented list of combinations. This first delivery does not add full recipe
pages to legacy addon machines, genetics, generators or alvearies.

## How to browse

Open the machine and press its **Inputs** button. The panel stays on the opposite
side of the player inventory. It has three tabs:

- **Items:** alphabetical names within item categories, including recipe inputs,
  catalysts and products. Click a row to show every recipe involving that item.
- **Recipes:** browse matching combinations with previous/next controls. **All**
  clears the item filter and shows all recipes for this machine. Mouse-wheel
  scrolling reveals the remaining details on longer pages.
- **Upgrades:** current installed sockets, supported legacy upgrade materials,
  effects and bounds. New upgrade cards are labelled pending, not presented as
  functional inventory items.

Each recipe page shows its registered ID, required count for each ingredient,
consumed versus reusable ingredients, catalyst or “none required”, all output
counts and probabilities, base job FE/ticks and current upgraded FE/ticks. The
refinery's upgraded product yield uses the same rule as actual processing.
Ingredient alternatives are **OR choices per slot**, not extra required inputs.
Icons cycle through alternatives and tooltips list them. Current recipes are
shapeless with one operating slot per required ingredient; quantities are not
silently combined across different slots.

Browsing never autofills, consumes items, spends FE or produces outputs. Machine
controls and operating slots remain unchanged. Narrow windows disable opening
this panel below 120 scaled pixels of side space; reduce GUI scale to read it.
Player/client click, tooltip and layout approval remains separate from server tests.

## Verification

The first red checkpoint failed compilation because the catalogue API did not
exist (`20261006_223350_runWorkflowTests.log`), not because a pre-existing recipe
was defective. The first implementation passed all78 workflow tests in
`20261006_223543_runWorkflowTests.log`.

Tests use real loaded recipes: all10 alloy combinations, Abyssal Pearl quantities
2/4/2, reusable Stardust and its four uses, exact40000FE/400ticks versus upgraded
24000FE/160ticks, and read-only browsing. Follow-up coverage checks crystal
seed/feed preservation, salvage's actual multiple products and refinery yield.
These tests cover the shared catalogue boundary, **not GPU rendering or physical
mouse clicks**. Final production/install evidence is recorded separately below.

The final extended catalogue run `20261006_223717_runWorkflowTests.log` passed
all **79 required workflow tests**, including crystal reusable seed/feed,
meteor-fragment salvage products and Nullifite refinery's2→3 upgraded yield.
Alternative ingredients are preserved from the live Ingredient definitions;
exhaustive client cycling/tooltip coverage is not claimed by these server tests.

## Installed production checkpoint

Runtime commit `48271c1f`. Final clean build `20261006_223923_clean.log` passed
after aligning footer click zones with their rendered buttons. Zero-error asset
audit: 7,937 models, 1,522 blockstates, 3,893 PNGs and96 animation metadata files.
No GameTest classes ship. Installed same-version JAR SHA256:
`f3455e9bf22bde4bb82014321304f26ea13e6ddfc2abbc007b48f8eb43e33ed4`.
Previous build backed up in `zerog-mod-backups/20261006-224040-UTC/`;
dependencies, hub and planetary saves are unchanged. Installation preceded push.

[Delivery receipt](recipe-discovery-delivery-2026-10-07.json) ·
[Matching archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-recipe-discovery-20261007.jar).

## Continuing queue — not included in this recipe-panel delivery

1. Verified recipe adapters for remaining machine families, including their real
   catalysts, fluid requirements, outputs, fuel and power contracts.
2. Six-tier Acceleration, Energy Coil and Item Compact cards, per-machine
   compatibility and lossless migration from legacy materials. Capacity formula,
   card stacking and bounded effect values still require approval. Avoid invalid
   oversized ordinary ItemStacks or loss when removing compact cards.
3. Installed Void card's server-validated Upgrades-tab ghost filter and selective
   output disposal; never void player inventory, input ingredients or catalysts.
4. Real directional energy pulses/fluid waves, transfer regressions and defined
   gases/units before gas-network implementation.
5. Verified alveary biology, Codex research mapping and authored seven-wide layouts.
6. Progression/ecology audits, remaining approved art and diagnostics. Undefined
   cooling/solar-plasma amounts remain specifications, not fabricated functionality.
7. Exact survival crafting costs last, after story-aligned workshop review.

The [TODO ledger](storage-and-machinery-todo.json) preserves the broader queue and
the [Forge/card report](alloy-forge-upgrade-card-issues-2026-10-07.md) preserves the
unresolved player-specific catalyst report. No world regeneration is included.
