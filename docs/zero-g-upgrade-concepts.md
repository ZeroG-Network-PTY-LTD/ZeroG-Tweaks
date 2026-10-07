# Original ZeroG machine upgrades

Owner direction, 7 October 2026: take functional inspiration from reference mods,
not their names, assets, machine identities, factory tiers or numerical rules.
No Mekanism dependency or copied implementation is part of this design.

## Current native processor contract

Acceleration and Energy Coil retain their verified six-tier rules: configured
speed capped at 2.5x and total-job energy saving capped at 30%. Item Compact adds
safe input reserves, never oversized ItemStacks. These apply to Alloy Forge, Ore
Refinery, Crystal Growth Chamber and Salvage Station. Other machines need separate
compatibility and balance contracts, not decorative nonfunctional sockets.

The next implementation is a **Void Card** with its own socket and a saved,
scrollable list of selected output item types. It suppresses only new matching
recipe products. It never disposes existing storage, inputs, catalysts, fluids,
player cursor items or unselected products. No card means no disposal. An empty
filter means no disposal. These safeguards take priority over cosmetic effects.

## Future original concepts — not implemented by this document

- **Resonance Dampener:** reduces operating sound; define supported sound sources.
- **Buffer Capacitor:** independent internal energy-storage expansion. Keep it
  separate from Energy Coil processing-efficiency rules until capacity limits,
  removal behavior and recovery are approved.
- **Phase Anchor:** bounded server-controlled chunk activity. Requires owner/team
  authorization, per-world/per-player limits and unload/removal checks first.
- **Concord Parallel Matrix:** story-unlocked concurrent recipe lanes, each with
  atomic ingredients, output capacity and conserved power. Lane counts and costs
  remain undecided; do not import another mod's 3/5/7/9 factory system.
- **Atmospheric Recovery Card:** future conservation for defined ZeroG gases.
  Gas IDs, units, limits and recipes are prerequisite specifications.

No 10x speed, eight-module stacking, hidden chunk loading or factory conversion
is authorized by these concepts. Survival recipe costs remain last in the workflow.
Dedicated card sprites await a supplied/approved reference; retain approved icons
temporarily and follow docs/art-direction-lock.md for any later artwork.
