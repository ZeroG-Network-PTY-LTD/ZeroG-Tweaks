# Upgrade-card doubling and 100 FE recipe floor

Owner-approved upgrade contract: tiers double relative to T1; Energy Coil affects
whole-recipe consumption, not the machine's storage buffer. Higher-tier recipes
retain their existing higher base costs. Cards do not multiply output yield.

| Card tier | Relative to T1 | Default speed versus no card | Example FE for a 2,000 FE recipe |
| --- | --- | --- | --- |
| T1 | 1 | 1.25× | 1,900 |
| T2 | 2 | 2.5× | 950 |
| T3 | 4 | 5× | 475 |
| T4 | 8 | 10× | 238 |
| T5 | 16 | 20× | 119 |
| T6 | 32 | 40× | 100 |

The existing T1 defaults are retained: 25% speed bonus and 5% recipe-energy
saving. From T2 onwards, speed doubles and the unrounded T1 FE cost is divided
by 2/4/8/16/32. Round up once, then enforce **100 FE minimum per powered recipe**.
This is not a 100 FE charge each tick. Acceleration alone shortens the same
recipe's duration and raises its per-tick energy demand; it does not reduce
whole-job FE. Installing a Coil separately reduces that whole-job cost.

The shared calculation covers native processors (including Industrial Compressor),
Water Separator, powered legacy processing and genetics jobs. Recipe catalogues
and synchronized menu values use the same exact calculation. Rounded percentage
labels are not used to calculate charges. Server configuration keeps the old
key names for compatibility, now interpreted as T1 baselines.

One card per supported family remains the limit. Item Compact and Void behaviour,
machine storage capacities, genetics traits, splice success and unpowered Geno
hand-cranking remain unchanged. Changed pricing fingerprints conservatively
cancel old partially paid jobs rather than granting unpaid completion.

## Play-test

1. Compare the same recipe with T1 through T6 in its Recipes view.
2. Use Acceleration alone, Coil alone, then both. Check job duration and exact
   total FE debit against the displayed recipe values.
3. Test Industrial Compressor with 2 Copper ingots plus reusable Plate Press,
   and 4 Copper ingots plus Cog Press. Verify the die remains and the outputs
   keep their material colours. Piston/result visual timing remains deferred.
4. Stop power or fill outputs: no input or output should be duplicated.
5. Save/reload midway through a job and remove a card. Inventory must remain
   recoverable; a changed configuration may safely reset progress.

The revised water/hot/ice NBTs remain included. The existing three prepared
structure regions, hub, player inventory and explored terrain are not replaced
by this card update. See [structure commands and inspection guide](structure-revision-playtest-2026-10-14.md).

## Verification boundary

Six native/legacy card checks passed, as did all six genetics checks, eleven
native/separator checks and a final 26-check compressor/owner regression run.
These test tier arithmetic, 100 FE minimum, whole-job accounting, reload, filters,
simulation, recipe pages and output conservation. The final run explicitly
executes Copper pressing with all six card tiers and verifies the die remains.
Production delivery receipt follows below.
No client play-test appearance or performance claim follows from server tests.

Production build passed and its JAR contains the new shared calculations and all
three exact revised NBTs. Optional test classes/fixtures are excluded. Same
`1.0.12-dev` version, SHA256:
`fb2979571840ebe770f7b2f8258a7a670f4b0f3058c2a7db5179f448b6b5fb99`.
Installation replaces only the ZeroG JAR and retains an old-JAR backup; no hub,
dimension, inventory or other mod files are replaced in this card batch.
