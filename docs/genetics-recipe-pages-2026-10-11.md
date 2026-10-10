# Genetics recipe and combination pages — 11 October 2026

## Implemented scope

Geno Station and Genetic Splicer now expose a separate **Recipes** panel with
Items, Recipes and Upgrades tabs. This is a read-only catalogue of the existing
server-owned jobs, not a crafting recipe, autofill mechanism or new biology rule.
The Geno Station footer switches between analysis and sampling descriptions.
Scroll for additional rows and hover shortened lines to read full text.

The pages identify operating slots, counts and prerequisites, item OR fluid
catalyst alternatives, item-before-tank priority, specimen/serum outputs, bottle
return slots and Royal/Cosmic Jelly success chances. Failed splices still consume
their reagents and return a specimen and vial. Both possible specimen outputs
must fit before the job begins.

Fully powered time/total FE are calculated from the actual runtime base duration,
cost and server-synchronized Acceleration/Energy Coil effects. Geno Station's
zero-power four-times-slower path is separate; mixed-power jobs do not promise a
fixed final cost/time. Splicer has no unpowered processing path.

The two new menu data fields append to existing fields; operating, recovery,
player and card slot indices do not move. Compact and Void remain unsupported in
genetics. One card per supported family, tiers 1-6, existing 2.5x speed and 30%
total-energy-saving caps are unchanged. Page navigation consumes external-panel
clicks and cancels inventory drag distribution; browsing cannot start a job.

## Verification and delivery

All **six required isolated genetics tests passed** in a fresh disposable world
with Productive Bees 13.14.0 and orbital addon 1.0.0. Transcript:
`20261010_231412_runGeneticsTests.log` (UTC filename; 11 October in Bangkok).
The new test completes **21 real jobs**: analysis, sampling and splicing, each
without cards and with both cards at every tier 1-6. It verifies advertised time,
exact paid FE, synchronized effects, bottle/vial return slots and read-only state.
Five existing regressions cover real Productive Bees gene attachment/splicing,
backpressure, input replacement, unpowered work, reload, menus/automation,
upgrades and placeholder suppression/power capability.

These 21 jobs use Honey Bottles and Cosmic Jelly items; this batch does not claim
new exhaustive fluid-route or probabilistic Royal Jelly outcome testing. Fluid
alternatives and dose/chance descriptions are traced to existing GeneticsTank
and GeneticsRuntime logic. No optional-absence launch was rerun this batch.
Client appearance/click review remains distinct from headless verification.
The production build must exclude opt-in test classes.

Clean normal production build passed in 51 seconds:
`20261010_231605_clean.log`. Asset audit reports **zero errors** across 7,979 models,
1,529 blockstates, 3,963 PNGs and 130 animation metadata files; no test classes or
fixtures ship. [Asset report](reports/genetics-recipe-assets-20261011.json).
The same-version **1.0.12-dev** JAR was installed with Minecraft confirmed closed.
Its previous JAR is in the instance's recoverable `zerog-mod-backups/20261010-231722-UTC`
folder. Saves, hub, other mods, approved gates and weather pause are unchanged.

[Archived production JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-genetics-recipes-20261011.jar)
SHA256: `c96b7fdac8f66aa45348e86ac85f917ad56149c37ad0369e73caa4af5b4eae8a`.
The runtime Codex chapter `11_genetics.md` has matching editable source on Design
in `docs/codex-guide-v1/write_guide.py`.

The first regression run exposed reused block-entity state in the new multi-job
test fixture. The fixture now clears the test position between jobs; production
processing was not changed to hide the failure. The fresh-world rerun passed.

## Manual review

1. Open each terminal, choose Recipes and inspect all three tabs at the usual GUI scale.
2. In Geno Station Recipes, switch Analyse/Sample and scroll through every row.
3. Hover truncated descriptions; confirm no overlap with machine/player slots.
4. Insert/remove Acceleration and Energy Coil cards: page FE/time should refresh.
5. Browse with an item on the cursor, right-click, shift-click and drag near the panel.
   Navigation must not drop, transfer, duplicate or consume inventory items.
6. Run analysis/sampling with Honey Bottles; inspect slot 4 and recovery slots 5-15.
7. Compare Royal/Cosmic item and 250 mB tank routes; ensure results follow page rules.

## Remaining queue

- Generator and alveary full combination pages and other unsupported adapters.
- Machine-specific further upgrade contracts; no invented Compact/Void semantics.
- Broader planetary ecology/client review and later structures/progression audits.
- Undefined advanced bee research/biology assignments and gas production rules.
- Exact survival crafting costs remain deferred to owner-provided balance.

Approved gates and custom-weather pause remain unchanged. No hub or dimensions
are reset by this batch.
