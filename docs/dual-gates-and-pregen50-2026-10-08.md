# Compact dual-gate hub and 50-chunk planetary reset

Minecraft Java1.21.1 / NeoForge, same1.0.12-dev version. This replaces the exact
`ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0` test save, installed8October after verification;
unrelated saves are not reset. The former compact hub is recoverably archived
outside Minecraft's saves list. The replacement starts with fresh inventory and
fresh custom planetary terrain, using seed0 and the current generators.

## What the earlier save showed

The player controller at(-33,65,-15) faced East while its blocks matched West,
and lacked the required energy port at(-31,65,-17). The former admin T1
controller at(-22,65,-24) faced South while its blocks matched North and lacked
the energy port at(-20,65,-22). Both were unformed and stored0FE. Five other
authored gates were formed and charged. An unformed gate intentionally cannot
accept power; this is not bypassed to make a damaged layout appear operational.

## Twelve northern gates

All controllers face North; gate part requirements and survival costs are unchanged.

| Tier | Admin controller | Player controller |
| --- | --- | --- |
| 1 | -22,65,-24 | -22,65,-68 |
| 2 | 0,65,-24 | 0,65,-68 |
| 3 | 22,65,-24 | 22,65,-68 |
| 4 | -22,65,-46 | -22,65,-90 |
| 5 | 0,65,-46 | 0,65,-90 |
| 6 | 22,65,-46 | 22,65,-90 |

Admin gates retain unrestricted/free hub travel. Player gates are not marked
admin: claim the terminal, select a tier-supported destination and pay normal FE.
Each player gate has a coal-fired generator and a finite, tier-matched cell feeding
a configured conduit into its **gate_energy_port**, not an unrelated machine port.
The cell is a finite test supply; it is not an infinite generator. Removing the
cell lets the player check charging from the coal generator alone.

The chart retains exact stored/maxFE text and tooltip and now has a charge bar.
An unformed terminal explicitly says **UNFORMED — use Align / Preview**.
Neither path paving nor district floors may replace required gate ring frames.
Landing-platform blocks are limited to gate footprints.

South: existing bee shells and external genetics references. West: supplied
machines, tank/port demonstrations and six-tier power/item/fluid lanes. East:
the existing ten inspection schematics. No new recipe costs or unseen artwork
are invented for this hub reset.

## Pre-generation scope

The corrected owner request is **50 total chunks per custom dimension**, not a
50x50 area. For each of34 dimensions, the requested10x5 rectangle is chunkX29–38,
chunkZ32–36: **1,700 requested FULL chunks** in total. Each contains a compact
cluster of twelve distinct return pads, corresponding to the twelve northern
controllers. Admin return pads remain free; player return pads preserve their
home binding and normal costs. Return pad ownership follows the claimed home.
The isolated hub preparation supplies each player return terminal with a finite
full buffer once, so its first return does not require waiting for the crystal
trickle charge. This is a test-world supply, not a change to survival generation.

Vanilla feature dependencies can also save neighboring chunks outside the exact
requested rectangle. That generation halo is not a promise of exactly50 physical
saved chunks. No permanent forced-chunk tickets are exported. Normal survival
gates outside this authored hub keep their previous landing-location algorithm.
This bounded GameTest preparation verifies terrain and return pads, not natural
structure distribution: GameTest disables structure starts while generating its
sample. The playable export enables ordinary structure generation for newly
explored chunks. Villages and rare structures are therefore not guaranteed
inside these fifty pre-generated chunks; their natural-generation audit remains
separate.

## Player checks

1. Open the rebuilt compact hub through CurseForge with shaders off initially.
2. Inspect a PLAYER terminal: formed tier, increasing exactFE and charge bar.
   Remove its overhead cell and check the coal generator and conduit charging
   its required energy port. Check generator output and conduit face modes.
3. Stand on that gate's central pad, select an available destination, Engage
   and Ready. Verify travel and use that gate's own bound return terminal.
4. Repeat with the ADMIN counterpart: its screen should say free admin travel,
   not require coal or consume player-gate energy.
5. Inspect the remaining five pairs, machine GUIs, ports and lanes. Use the
   [existing tier-by-tier building guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/gate-building-tiers-1.21.1.md)
   for exact part counts; the geometry was not redesigned.

Server formation, transfer, menu-data and saved-chunk checks are distinct from
client GUI/graphics approval and real player travel. Those remain owner checks.
Custom weather remains paused. Undefined research rules and exact survival
recipe costs remain pending, not supplied by this reset.

## Verified delivery

The final four required tests passed with Productive Bees13.14.0 and the orbital
addon1.0.0 present, followed by a successful clean production build and zero-error
asset audit. The installed save contains twelve formed, charged controllers;
all1,700 requested FULL chunks were read back before export. The test server
saved every dimension and stopped cleanly. The installed JAR has SHA256
`83e80cedb9414f95d8577a9c2f9f4d3553ba81a34b31b8aef4c49fc5612b1020`.

[Delivery receipt and test limitations](dual-hub-pregen50-delivery-2026-10-08.json).
The first wider attempt hit Productive Bees' simulated-client payload limitation;
interrupted pre-generation attempts were discarded, not installed. Final testing
uses non-login mock players and a fresh disposable world. Real client travel and
GUI readability still require the player's inspection.
