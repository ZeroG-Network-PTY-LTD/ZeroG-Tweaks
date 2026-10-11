---
navigation:
  title: 14. Frame Recipes
  icon: zerog_tweaks:concord_codex
  position: 140
  parent: index.md
---

# Frame Production Recipes

Open Items, Recipes and Upgrades on the Frame Assembler, Frame Component
Assembler or either Infusion Altar. Clicking an ingredient or output lists
its exact combinations. Both inputs are consumed, one each; output is certain.

## Assembly

Put an Untreated Frame in slot 0 and one material in slot 1:

- Honeycomb makes an Impregnated Frame.
- Starmetal Ingot makes a Starmetal Frame.
- Woven Silk makes an Aero Silk Frame.

## Infusion

Put an Impregnated Frame in slot 0 and one reagent in slot 1:

- Amethyst Shard makes a Proven Frame.
- Cosmic Jelly item makes a Cosmic Vigor Frame.
- Stardust makes a Starlit Frame.

The result uses slot 2, except Frame Infusion Altar, which uses slot 3.
Its old slot 2 is recovery-only. A blocked output pauses processing without
consuming ingredients. Completion takes 201 processing ticks in the current
runtime. These machines now require cable power: the default is 20 FE per work
tick, or 4,020 FE per base job. Their six faces have independent power/input
controls, and Acceleration/Energy Coil cards use the existing 2.5x/30% caps.

## Silk and centrifuges

Silk Weaver consumes one Silk Thread and produces one Woven Silk in slot 3.
Slots 1 and 2 remain recovery-only, not pattern or catalyst inputs. Its base job
is 200 ticks and 4,000 FE by default. Gravitational Centrifuge shares the normal
Centrifuge's comb recipes and default 20 FE per work tick. Unpowered or blocked
jobs consume no ingredients or processing FE.

The Recipes button opens a separate read-only view within the current menu, so
Items, Recipes and Upgrades remain usable without squeezing inventory or side
controls. Back or Escape returns to the machine; browsing never moves items.

Browsing does not autofill or start jobs. Survival crafting costs remain deferred;
these are the existing processing combinations, not new crafting recipes.
