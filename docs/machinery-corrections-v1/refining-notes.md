# Powered Ore Refinery migration

The code branch retains `zerog_tweaks:ore_refinery` for the block, item and
block entity. It uses the shared processing terminal and registered `refining`
recipe serializer, not a hidden five-entry table or unpaid timer.

`generate_refining.py <code-worktree>` translates all 39 authored pending recipes
to the modern counted-input/output schema. Ore outputs follow the authored data:
metal ores produce raw material, while gems and dust ores retain their own product.
Existing raw-metal smelting recipes supply the raw-to-ingot routes. Registered raw
storage blocks represent nine raw units: 18 base ingots or 27 with a casing upgrade,
with nine times the raw-item energy cost. The generator does not delete recipes.

The standard casing upgrade selects each recipe's authored upgraded count. Casing,
Cryo Core and energy-dust slots remain independently bounded to one item each;
existing processing speed/efficiency rules apply. Output capacity is checked using
the upgraded count before FE is spent. There is no imaginary fluid catalyst route.

The Aresite boost consumes one real ZeroG Stardust. A separate conditioned recipe
preserves optional `aeroapiary:stardust` compatibility without requiring that mod.

Save migration keeps physical slots 0=input, 1=catalyst and 2=output, expands the
legacy three-slot inventory to six and discards old unpaid progress. Paid modern
jobs, FE, inventory and upgrades retain their normal processing save data. The old
menu registry remains registered for compatibility; new interactions open the shared
six-slot powered terminal.

Automation: top/left/right feed reagents, rear feeds catalysts, front/bottom expose
outputs only. Energy is accepted through the real FE capability. Upgrade insertion
is through the player's machine terminal, not incidental automation slots.

Native artwork is unchanged. GUI visual approval and optional recipe-guide support
are separate from isolated gameplay tests.
