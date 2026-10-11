---
navigation:
  title: 15. Stardust Smelter
  icon: zerog_tweaks:concord_codex
  position: 150
  parent: index.md
---

# Stardust Smelting

Put a supported comb in slot 0 and furnace fuel in slot 1. Slot 2 holds dust.
Open Recipes, then click a comb, dust or fuel in Items to inspect the combinations.

- One Meteor Comb produces two Stardust.
- One Nebula Comb produces three Stardust.
- One Molten Comb produces one Stardust.

Each job takes 201 hot ticks. Fuel uses Minecraft's smelting burn duration,
not one fuel item per comb. One coal supplies 1,600 hot ticks: seven consecutive
jobs with 193 ticks left for the next job. Coal blocks last 16,000 ticks.
The Items tab shows each accepted fuel; selecting one displays its actual budget.

Fuel is consumed when the fire starts. Container fuels return their container.
A cold blocked machine does not ignite fuel; an already lit fire continues to
burn while idle or blocked, like a furnace. Inputs are consumed only on successful
completion. Running out of heat resets incomplete work without consuming the comb.
Remaining fire and progress survive save/reload. Changing comb type resets work.

No FE or upgrade cards are required or supported here. This repair does not set
survival crafting costs, change combustion-generator fuels or alter comb yields.
