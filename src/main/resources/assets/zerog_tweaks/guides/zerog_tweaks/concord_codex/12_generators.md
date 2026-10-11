---
navigation:
  title: 12. Generator Recipes
  icon: zerog_tweaks:combustion_generator
  position: 120
  parent: index.md
---

# Generator Recipes

Combustion Generator, Solar Array and Fusion Reactor have read-only Items,
Recipes and Upgrades tabs. Select a fuel in Items, then scroll or hover shortened
recipe lines for full details. Browsing never starts a job or moves items.

## Combustion

Wood items, coal forms and supported planetary fuels burn; dusts are rejected.
One fuel item is consumed on ignition. The page shows its actual active burn
ticks, production rate and fresh-burn FE budget. Saved fractional carry may add
one FE across burns. A full buffer pauses burning rather than wasting paid fuel.

## Fusion

Only Fusion Dust is accepted. Its duration and base output come from the server
configuration. The page describes a future burn using that configuration;
already ignited fuel retains its saved base rate. There is no gas or liquid fuel
route, catalyst or item byproduct.

## Solar

There is no fuel slot. Generation requires daytime, skylight and visible sky.
An opaque roof or thunder stops generation; rain reduces it. Moon, Eidolon and
Solvane have configured multipliers. The current environment rate is displayed;
free buffer space limits the actual FE generated.

## Modules and routing

All three generators accept up to three Flux Modules, each adding 25% production
rate and one base buffer capacity. Modules do not shorten fuel duration.
Acceleration, Energy Coil, Compact and Void cards are unsupported here.
Solar/Fusion module removal is blocked if the smaller buffer would lose stored FE.

Power faces are Output or Off, never FE input. Automatic push is shared across
enabled faces: Combustion uses 1,000 FE/t, Solar/Fusion use the server transfer
setting. Production rate is not a cable transfer guarantee. Exact survival
crafting costs and client layout approval remain separate.
