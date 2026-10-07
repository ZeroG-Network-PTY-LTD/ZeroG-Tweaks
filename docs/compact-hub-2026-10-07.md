# Compact hub and on-demand planets

Minecraft 1.21.1 · NeoForge · same **1.0.12-dev**, without a version bump.

Open **ZeroG Compact Hub 1.0.12 — Seed 0** (`ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0`). Seed: **0**. Spawn: **0,65,0**.

## What changed

The previous hub's client log recorded **66.536 seconds** from “Stopping server” to “All dimensions are saved”. It also recorded substantial gameplay stalls while the hub prepared arrival platforms and inspection villages across all 34 planets. These observations support background generation and permanently loaded showcases as contributors; they do not prove that landing-pad textures caused the delay.

The new hub is smaller, with ordinary stone-brick floors and paths. **Landing Platform blocks are confined to gate footprints**. Its workshop, transport lanes and galleries no longer force chunks to stay loaded. The old automatic 34-destination arrival/village sweep is disabled for compact hubs.

Planets are still registered and reachable. No old planetary terrain was copied into this new save: a destination generates from its normal world-generation settings when visited. The bound return gate is created on real travel. This is intentionally **not** pre-generation of every planet while the player inspects the hub. Natural village generation remains enabled; removal of the old inspection-village sweep does not delete natural villages.

## Layout

```text
                    NORTH
           tier 4   tier 5   tier 6
           tier 1   tier 2   tier 3
    transport             central spawn
    machines / tanks       |        ten structure exhibits
            WEST           |                EAST
                      bee designs
                    formed alvearies
                         SOUTH
```

- **North:** six real gate tiers in two rows of three. Tier 1–3 centres: `(-22,64,-22)`, `(0,64,-22)`, `(22,64,-22)`; tier 4–6: the same X positions at Z=`-44`.
- **West:** 13 supplied machine stations; inventories contain test recipe materials and catalysts. Power/service examples and six-tier transport/tank lanes remain available. Supplies are not automatically replenished.
- **South:** eight apiary/alveary design displays and four formed multiblock examples.
- **East:** ten structure/arena exhibits, retained for inspection.

Gate travel is **admin/free** in this hub, as requested. The physical tier is still validated. Ordinary survival gates elsewhere retain ownership, energy, passenger and destination restrictions. See the [complete tier 1–6 construction guide](gate-building-tiers-1.21.1.md) for counts, layers, coordinates and current activation behaviour; its [machine-readable manifest](gate-build-layouts-1.21.1.json) supports future Codex work.

## Save handling

Only the previous named Cardinal Hub was moved into the instance's `zerog-hub-archives` folder. Its terrain, player inventory and progression remain recoverable there. The new save starts fresh; it does not migrate those player inventories. Unrelated saves are untouched. Test players, distant GameTest structures, test planetary regions and forced-chunk tickets are not exported.

The same-version installed JAR has an old-JAR backup. Published JARs and earlier documentation remain archived rather than overwritten. The [delivery receipt](compact-hub-delivery-2026-10-07.json) records installed bytes, test evidence and save export hashes.

## Verification and remaining review

Two isolated server tests passed: all six gates form at their exact tiers, retain admin state on reload, reuse return platforms, and preserve edits on repeat build; the compact hub has all supplied workshop machines, gate-only landing floors, no forced hub chunks and no background planetary sweep.

The isolated server saved in **3 seconds**, at one-second log resolution. It differs from a full client session, loaded terrain and rendering workload; **this is not a measured client performance improvement**. The next real playtest should time save/quit again using `tools/measure_shutdown.py` on the code branch.

Still pending: client appearance/travel/GUI approval; broad natural-world ecology checks; migration of the old 34-outbound-gate audit/export assumptions; advanced alveary research/biology and larger authored layouts; remaining recipe pages; exact survival crafting costs. This delivery does not claim those are complete.
