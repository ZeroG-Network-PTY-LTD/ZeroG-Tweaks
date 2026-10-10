---
navigation:
  title: 11. Genetics Recipes
  icon: zerog_tweaks:concord_codex
  position: 110
  parent: index.md
---

# Genetics Recipes

The orbital addon supplies the Geno Station and Genetic Splicer. Their **Recipes**
button opens three read-only tabs: Items, Recipes and Upgrades. Hover shortened
lines for the full text and scroll for all details. The Geno Station recipe page
switches between Analyse and Sample using its bottom button. Browsing does not
start a job or move items; use the machine's normal operation buttons to work.

## Analysis and sampling

Insert one filled Productive Bees cage with five saved valid traits. Analysis
returns an analysed cage without changing its traits. Sampling requires that
analysed specimen, one serum vial and a selected gene; it returns the cage and
one serum carrying that gene's value.

Each job consumes either one Honey Drop, one Honey Bottle, or 250 mB of supported
honey from the tank. A valid item catalyst takes priority over the tank. Analysis
returns an empty Honey Bottle container to output slot 4; sampling returns it to
a free recovery slot 5-15 because slot 4 contains the serum. Fluid and Honey Drop
routes return no bottle.

## Splicing

Use an analysed specimen and one valid serum. Royal Jelly gives 75% success;
Cosmic Jelly gives 100%. Each may be supplied as one item or 250 mB from the tank.
The serum and catalyst are consumed on either outcome. Success returns a cage
with only that gene changed; failure returns the original cage. Both outcomes
return one empty serum vial. Leave room for both outputs before starting.

## Power and cards

Base powered analysis is 100 ticks / 2,000 FE, sampling 300 ticks / 6,000 FE, and
splicing 400 ticks / 24,000 FE. The Geno Station works four times slower without
power; the Splicer requires power. Mixed-power jobs vary with powered work.

Acceleration and Energy Coil cards have separate sockets and tiers 1-6, capped
at 2.5x speed and 30% total FE savings. The pages use server-synced current effects.
Cards do not improve splice chance or traits. Compact and Void are unsupported.
Exact crafting costs and advanced Codex research rules remain pending.
