---
navigation:
  title: 13. Alveary Recipes
  icon: zerog_tweaks:concord_codex
  position: 130
  parent: index.md
---

# Alveary Production Recipes

Open the controller's Recipes button for Items, Recipes and Upgrades. Hover
shortened lines and scroll for all details. Items lists accepted frames; the bee
still goes in the main input slot. Browsing is read-only: it cannot start a job,
autofill inventory, sort outputs or toggle void.

## Bee inputs and products

Use one supported orbital bee or a captured Productive Bees specimen with five
saved valid traits. Production retains the specimen. Orbital species produce
their registered comb; Productive Bees outputs are resolved from the server's
loaded advanced-beehive recipes, including item components, quantity ranges and
chances. Saved bee productivity is included in the displayed ranges.

The recipe snapshot updates about once per second while the controller menu is
valid. Removing or changing the specimen updates its products. More than 32
product entries are explicitly marked truncated rather than silently hidden.

## Frames and cycle time

Existing controller tiers 1-7 unlock 3, 4, 6, 8, 12, 18 and 27 frame slots.
Honeyed, Starlit and Starmetal frames each add 15% cycle-speed productivity;
Proven and Impregnated add 10%; Restraint and Oblivion subtract 5%; other
supported frames add 5%. The total multiplier is bounded from x0.25 to x4.
Frames shorten or lengthen the cycle; they do not multiply output quantities.

The page shows the current runtime cycle. Tier 3 and above consume 20 times the
tier in FE per active tick; tiers 1-2 require no FE. The displayed full-cycle
budget assumes unchanged frames and catalyst availability throughout the job.
Day/night behavior, rain tolerance, formation, blocked products or honey storage
may pause progress; paused ticks do not represent productive work.

## Honey and optional Starlight

Tier 3 and above produce 250 mB of local Sol-planet honey alongside products on
every completed cycle. Other dimensions use Moon Honey. The honey tank holds
8,000 mB and cannot mix honey types. Use the honey/output service port to drain it.

Tier 6 and above have a 4,000 mB Liquid Starlight catalyst tank. At least 25 mB
gives x1.2 cycle speed; 25 mB is consumed when the cycle completes. This boost is
optional. Service ports handle power, item and fluid automation; the controller
is the interaction terminal, not a cable shortcut.

## Existing limits

Acceleration, Energy Coil, Compact and Void cards are unsupported here. Existing
eject and void buttons remain independent controls, not card upgrades. Native
lifespan/territory alleles, additional climate/module rules and the Codex research
milestone map remain pending specifications. This chapter does not introduce
seven-wide layouts or survival crafting costs.
